#!/usr/bin/env python3
"""
tests/test_utils.py

Unit tests for utils.py:
- access_nested_map
- get_json
- memoize
"""

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
        """Test that access_nested_map returns the expected value."""
        result = access_nested_map(nested_map, path)
        self.assertEqual(result, expected)

    @parameterized.expand([
        # (nested_map, path, missing_key)
        ({}, ("a",), "a"),
        ({"a": {}}, ("a", "b"), "b"),
    ])
    def test_access_nested_map_exception(self, nested_map, path, missing_key):
        """
        Test that access_nested_map raises KeyError when a key is missing.
        """
        with self.assertRaises(KeyError) as ctx:
            access_nested_map(nested_map, path)

        # ctx.exception.args[0] is the missing key
        self.assertEqual(ctx.exception.args[0], missing_key)


class TestGetJson(unittest.TestCase):
    """Test suite for utils.get_json using mocked HTTP calls."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch("utils.requests.get")
    def test_get_json(self, test_url, test_payload, mock_get):
        """
        For each (test_url, test_payload):
        - Patch requests.get so .json() returns test_payload.
        - Call get_json(test_url) and verify:
          1) requests.get called once with test_url.
          2) get_json returns test_payload.
        """
        # Create a fake response object
        fake_response = Mock()
        # Simulate successful status (raise_for_status does nothing)
        fake_response.raise_for_status.return_value = None
        # When .json() is called, return our payload
        fake_response.json.return_value = test_payload

        # Configure patched requests.get to return fake_response
        mock_get.return_value = fake_response

        # Call get_json; no real HTTP call is made
        result = get_json(test_url)

        # Verify requests.get was called once with test_url
        mock_get.assert_called_once_with(test_url)

        # Verify get_json returned test_payload
        self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Test suite for the memoize decorator."""

    def test_memoize(self):
        """
        Define TestClass with:
        - a_method() returns 42
        - a_property() decorated with @memoize
          that calls a_method()

        Patch a_method to count calls, then call a_property()
        twice, verifying a_method is called only once.
        """

        # Define class inside test method so we can patch a_method
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        # Create an instance of TestClass
        test_obj = TestClass()

        # Patch TestClass.a_method to monitor calls
        with patch.object(TestClass, "a_method", autospec=True) as mock_a_method:
            # Configure mock to return 42
            mock_a_method.return_value = 42

            # First call to a_property(): should call a_method once
            first_result = test_obj.a_property()
            self.assertEqual(first_result, 42)
            mock_a_method.assert_called_once_with(test_obj)

            # Reset call count to test second access
            mock_a_method.reset_mock()

            # Second call to a_property(): should not invoke a_method again
            second_result = test_obj.a_property()
            self.assertEqual(second_result, 42)
            mock_a_method.assert_not_called()


if __name__ == "__main__":
    unittest.main()
