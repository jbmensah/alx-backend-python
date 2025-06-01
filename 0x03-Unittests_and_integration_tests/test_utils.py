#!/usr/bin/env python3

import unittest
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize
import requests

class TestAccessNestedMap(unittest.TestCase):
	"""Test cases for access_nested_map function."""

	@parameterized.expand([
		({"a": 1}, ("a",), 1),
		({"a": {"b": 2}}, ("a", "b"), 2),
		({"x": {"y": {"z": 3}}}, ("x", "y", "z"), 3),
	])
	def test_access_nested_map(self, nested_map, path, expected):
		"""Test accessing nested maps."""
		self.assertEqual(access_nested_map(nested_map, path), expected)

	def test_access_nested_map_key_error(self):
		"""Test KeyError when accessing a non-existent key."""
		nested_map = {"a": {}}
		with self.assertRaises(KeyError):
			access_nested_map(nested_map, ("a", "missing_key"))

class TestGetJson(unittest.TestCase):
	"""Test suite for get_json (Milestone 1: mocking HTTP calls)."""

	# You’ll fill in a mock-based test here later (patching requests.get).

class TestMemoize(unittest.TestCase):
	"""Test suite for memoize decorator (Milestone 2)."""

	# You’ll fill in a test that patches a method to confirm memoization.