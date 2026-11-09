"""Offline tests for UCRSearcher."""
from __future__ import annotations

import argparse
import sys
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import ucr_adapter as adapter  # noqa: E402


class FakeHttp:
    def __init__(self, data):
        self.data = data
        self.evidence = []

    def json(self, url, params=None, headers=None):
        return self.data, {
            "source_url": url, "http_status": 200, "content_type": "application/json",
            "bytes": 100, "retrieved_at": "2026-11-09T00:00:00Z", "sha256": "0" * 64,
        }


def args(**kwargs):
    base = dict(limit=2, offset=0, cache=".cache", offline=False, cache_ttl=0, timeout=30)
    base.update(kwargs)
    return argparse.Namespace(**base)


class UcrTests(unittest.TestCase):
    def test_search_filters_recent_filings(self):
        payload = [
            {"documentTitle": "Akayesu decision", "caseNumber": "ICTR-96-4-T", "caseDescription": "Akayesu", "docTypeDesc": "Decision", "docFilingDate": "2020-01-01"},
            {"documentTitle": "Other filing", "caseNumber": "X", "caseDescription": "Other", "docTypeDesc": "Order", "docFilingDate": "2020-01-02"},
        ]
        out = adapter.search("akayesu", args(), FakeHttp(payload))
        self.assertEqual(out["status"], "ok")
        self.assertEqual(out["total"], 1)
        self.assertEqual(out["results"][0]["case_number"], "ICTR-96-4-T")


if __name__ == "__main__":
    unittest.main()
