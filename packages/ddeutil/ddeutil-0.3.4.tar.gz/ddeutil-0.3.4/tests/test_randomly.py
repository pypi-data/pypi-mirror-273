import unittest
from unittest import mock

import ddeutil.core.__base.hash as _hash


class RandomTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.patcher = mock.patch("random.choices", return_value="AA145WQ2")
        self.patcher.start()

    def tearDown(self) -> None:
        self.patcher.stop()

    def test_random_string(self):
        self.assertEqual(_hash.random_str(), "AA145WQ2")
