#!/usr/bin/env python3

# tests/test_utils.py

import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock
import requests

from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
	"""Test suite for access_nested_map (Milestone 0)."""

	@parameterized.expand([
		({"a": 1}, ("a",), 1),
		({"a": {"b": 2}}, ("a", "b"), 2),
		({"x": {"y": {"z": 3}}}, ("x", "y", "z"), 3),
	])
	def test_access(self, nested_map, path, expected):
		result = access_nested_map(nested_map, path)
		self.assertEqual(result, expected)

	@parameterized.expand([
		# For each tuple: (nested_map, path, missing_key)
		({}, ("a",), "a"),
		({"a": {}}, ("a", "b"), "b"),
	])
	def test_access_nested_map_exception(self, nested_map, path, missing_key):
		"""
		The function should raise KeyError when any key in `path` is missing.
		We use `assertRaises` as a context manager and then verify that
		the KeyError’s .args[0] matches the missing key.
		"""
		with self.assertRaises(KeyError) as ctx:
			access_nested_map(nested_map, path)

		# ctx.exception.args[0] contains the actual key that was not found
		self.assertEqual(ctx.exception.args[0], missing_key)


class TestGetJson(unittest.TestCase):
	"""Test suite for get_json (Milestone 1: mocking HTTP)."""

	@patch('utils.requests.get')
	def test_get_json_success(self, mock_get):
		expected_payload = {"some": "data"}
		fake_response = Mock()
		fake_response.raise_for_status.return_value = None
		fake_response.json.return_value = expected_payload

		mock_get.return_value = fake_response

		url = "http://example.com/fake-endpoint"
		result = get_json(url)

		mock_get.assert_called_once_with(url)
		self.assertEqual(result, expected_payload)

	@patch('utils.requests.get')
	def test_get_json_error(self, mock_get):
		fake_response = Mock()
		fake_response.raise_for_status.side_effect = requests.HTTPError("Not Found")

		mock_get.return_value = fake_response

		url = "http://example.com/bad-endpoint"
		with self.assertRaises(requests.HTTPError):
			get_json(url)

		mock_get.assert_called_once_with(url)


class TestMemoize(unittest.TestCase):
	"""Test suite for memoize decorator (Milestone 2)."""
	# (Fill in as you work on Task 2…)
