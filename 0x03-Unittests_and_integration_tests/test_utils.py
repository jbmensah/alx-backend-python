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
	# """Test suite for get_json (Milestone 1: mocking HTTP)."""

	# @patch('utils.requests.get')
	# def test_get_json_success(self, mock_get):
	# 	expected_payload = {"some": "data"}
	# 	fake_response = Mock()
	# 	fake_response.raise_for_status.return_value = None
	# 	fake_response.json.return_value = expected_payload

	# 	mock_get.return_value = fake_response

	# 	url = "http://example.com/fake-endpoint"
	# 	result = get_json(url)

	# 	mock_get.assert_called_once_with(url)
	# 	self.assertEqual(result, expected_payload)

	# @patch('utils.requests.get')
	# def test_get_json_error(self, mock_get):
	# 	fake_response = Mock()
	# 	fake_response.raise_for_status.side_effect = requests.HTTPError("Not Found")

	# 	mock_get.return_value = fake_response

	# 	url = "http://example.com/bad-endpoint"
	# 	with self.assertRaises(requests.HTTPError):
	# 		get_json(url)

	# 	mock_get.assert_called_once_with(url)
	"""Test suite for utils.get_json using mocked HTTP calls."""

	@parameterized.expand([
		("http://example.com", {"payload": True}),
		("http://holberton.io", {"payload": False}),
	])
	@patch("utils.requests.get")
	def test_get_json(self, test_url, test_payload, mock_get):
		"""
		For each (test_url, test_payload):
		- Patch requests.get so it returns a Mock whose .json() gives test_payload.
		- Call get_json(test_url) and verify:
		1) requests.get was called exactly once with test_url.
		2) get_json returned test_payload.
		"""
		# 1. Create a fake response object
		fake_response = Mock()
		# Simulate a successful status (so raise_for_status() does nothing)
		fake_response.raise_for_status.return_value = None
		# When .json() is called, return our test_payload
		fake_response.json.return_value = test_payload

		# 2. Configure the patched requests.get to return our fake_response
		mock_get.return_value = fake_response

		# 3. Call get_json; no real HTTP call is made
		result = get_json(test_url)

		# 4. Verify requests.get was called exactly once with test_url
		mock_get.assert_called_once_with(test_url)

		# 5. Verify the returned value matches test_payload
		self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
	"""Test suite for memoize decorator (Milestone 2)."""
	# (Fill in as you work on Task 2…)
