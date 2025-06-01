#!/usr/bin/env python3

import unittest
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize
import requests
from unittest.mock import patch, Mock

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

	@patch('utils.requests.get')
	def test_get_json_success(self, mock_get):
		"""
		If requests.get returns a response whose status is OK and .json() returns data,
		then get_json should return that data.
		"""
		# 1. Create a fake JSON payload
		expected_payload = {"some": "data"}

		# 2. Create a fake response object and configure it:
		fake_response = Mock()
		fake_response.raise_for_status.return_value = None  # No exception raised
		fake_response.json.return_value = expected_payload

		# 3. Tell the mock_get to return this fake response
		mock_get.return_value = fake_response

		# 4. Call get_json with any URL (it won’t be fetched over the network)
		url = "https://example.com/fake-endpoint"
		response = get_json(url)

		# 5. Assert that requests.get was called exactly once with our URL
		mock_get.assert_called_once_with(url)

		# 6. Assert that get_json returned exactly what fake_response.json() gave
		self.assertEqual(response, expected_payload)
		# expected_response = {"login": "google", "id": 1342004, "public_repos": 42}

	@patch('utils.requests.get')
	def test_get_json_error(self, mock_get):
		"""
		If requests.get returns a response whose raise_for_status() raises HTTPError,
		then get_json should let that exception bubble up.
		"""
		# 1. Create a fake response whose .raise_for_status() raises an HTTPError.
		fake_response = Mock()
		fake_response.raise_for_status.side_effect = requests.HTTPError("Not Found")

		# 2. Assign that fake_response to mock_get
		mock_get.return_value = fake_response

		# 3. Call get_json and assert that an HTTPError is raised
		url = "http://example.com/bad-endpoint"
		with self.assertRaises(requests.HTTPError):
			get_json(url)

		# 4. Also verify that requests.get was called once
		mock_get.assert_called_once_with(url)



class TestMemoize(unittest.TestCase):
	"""Test suite for memoize decorator (Milestone 2)."""

	# You’ll fill in a test that patches a method to confirm memoization.