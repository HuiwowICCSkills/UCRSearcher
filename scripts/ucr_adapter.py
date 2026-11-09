#!/usr/bin/env python3
"""IRMCT Unified Court Records public adapter for UCRSearcher."""

from __future__ import annotations

import argparse
from typing import Any

from skillkit import HTTP, RetrievalError, result

PROG = "ucr_search.py"
DESCRIPTION = "Search the public IRMCT Unified Court Records recent-filings endpoint."
CACHE_DEFAULT = ".ucr-cache"

API = "https://ucr.irmct.org/api/Record/GetRecentlyFiled"
UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/155.0.0.0 Safari/537.36"
)
FIELDS = (
    "documentTitle",
    "caseNumber",
    "caseDescription",
    "docTypeDesc",
    "docFilingDate",
    "filingDate",
    "signatureDate",
)


def _headers() -> dict[str, str]:
    return {"User-Agent": UA, "Accept": "application/json"}


def make_http(args: argparse.Namespace) -> HTTP:
    return HTTP(
        args.cache,
        offline=args.offline,
        ttl=args.cache_ttl,
        timeout=args.timeout,
        user_agent=UA,
    )


def add_search_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--limit", type=int, default=10, help="1..50 (default 10)")
    parser.add_argument("--offset", type=int, default=0, help=">= 0 (default 0)")


def search(query: str, args: argparse.Namespace, http: HTTP) -> dict[str, Any]:
    if not query.strip():
        raise ValueError("A non-empty query is required")
    if not 1 <= args.limit <= 50:
        raise ValueError("limit must be 1..50")
    if args.offset < 0:
        raise ValueError("offset must be >= 0")
    data, meta = http.json(API, headers=_headers())
    if not isinstance(data, list):
        raise RetrievalError("UCR public recent-filings schema changed: expected a list")
    query_norm = query.casefold()
    hits: list[dict[str, Any]] = []
    for record in data:
        text = " ".join(str(record.get(key) or "") for key in FIELDS)
        if query_norm not in text.casefold():
            continue
        hits.append(
            result(
                record.get("documentTitle") or "UCR recent filing",
                "https://ucr.irmct.org/",
                "ucr-public-recent",
                text,
                record_id=record.get("recordID"),
                document_id=record.get("documentID"),
                case_number=record.get("caseNumber"),
                case_name=record.get("caseDescription"),
                document_type=record.get("docTypeDesc"),
                date=record.get("docFilingDate") or record.get("filingDate"),
                access="public recent-filings metadata; full UCR search requires an authenticated account",
                content_scope=(
                    "UCR public GetRecentlyFiled record; this is not the whole registry "
                    "and does not include the document text"
                ),
            )
        )
    total = len(hits)
    selected = hits[args.offset : args.offset + args.limit]
    return {
        "status": "ok" if selected or total == 0 else "no-results-in-queried-index",
        "query": query,
        "total": total,
        "results": selected,
        "pagination": {
            "offset": args.offset,
            "limit": args.limit,
            "next_offset": args.offset + len(selected) if selected and args.offset + len(selected) < total else None,
        },
        "scope": (
            "IRMCT Unified Court Records public recent-filings endpoint only; "
            "full UCR search requires a registered account and is not attempted"
        ),
        "evidence": http.evidence,
        "retrieved_at": meta.get("retrieved_at"),
    }


def doctor(args: argparse.Namespace) -> dict[str, Any]:
    checks = [
        {"check": "python", "ok": True, "detail": "Python runtime available"},
        {"check": "requests", "ok": True, "detail": "requests importable"},
    ]
    if args.no_probe:
        return {"ok": True, "status": "ok (probes skipped)", "checks": checks}
    http = make_http(args)
    try:
        data, meta = http.json(API, headers=_headers())
        checks.append(
            {
                "check": "UCR public recent filings",
                "ok": isinstance(data, list),
                "records": len(data) if isinstance(data, list) else None,
                "http_status": meta["http_status"],
                "bytes": meta["bytes"],
            }
        )
        ok = isinstance(data, list) and bool(data)
    except Exception as exc:
        checks.append(
            {
                "check": "UCR public recent filings",
                "ok": False,
                "error": f"{type(exc).__name__}: {exc}",
                "manual_login_required_for_full_search": True,
            }
        )
        ok = False
    return {
        "ok": ok,
        "status": "ok" if ok else "error",
        "checks": checks,
        "catalog": {"api": API, "note": "Full UCR search requires an authenticated account."},
    }
