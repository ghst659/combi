#!/usr/bin/env python3

import logging
import unittest
import sys

import combi

class CombiTests(unittest.TestCase):

    def test_basic(self):
        got = list(combi.genit([["a", "b"], ["c", "d"]]))
        self.assertEqual(got, ["ac", "ad", "bc", "bd"])

if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr, level=logging.INFO)
    unittest.main()
