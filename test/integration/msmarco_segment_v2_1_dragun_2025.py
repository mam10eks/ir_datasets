import re
import unittest
import ir_datasets
from ir_datasets.datasets.msmarco_segment_v2_1 import MsMarcoV21SegmentedDoc
from ir_datasets.formats import TrecQrel, GenericQuery
from .base import DatasetIntegrationTest


_logger = ir_datasets.log.easy()


class TestMSMarcoV21DocsSegmentedDragun(DatasetIntegrationTest):
    def test_dragun_2025_queries(self):
        ds = ir_datasets.load('msmarco-segment-v2.1/trec-dragun-2025')
        queries = list(ds.queries_iter())

        self.assertEqual(30, len(queries))
        self.assertEqual('msmarco_v2.1_doc_04_420132660', queries[0].query_id)
        self.assertEqual("The Greek-Canadian Origins of the Hawaiian Pizza - Gastro Obscura", queries[0].default_text())

        self.assertEqual('msmarco_v2.1_doc_58_748655897', queries[-1].query_id)
        self.assertEqual("The Area 51 Raid Was the Worst Way to Spot an Alien or UFO | WIRED", queries[-1].default_text())


if __name__ == '__main__':
    unittest.main()
