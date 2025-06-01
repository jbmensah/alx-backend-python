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
        # For each tuple: (nested_map, path, missing_key)
        ({}, ("a",), "a"),
        ({"a": {}}, ("a", "b"), "b"),
    ])
    def test_access_nested_map_exception(self, nested_map, path, missing_key):
        """
        Test that access_nested_map raises KeyError when any key in path is missing.
        We use assertRaises as a context manager and then verify that
        the KeyError’s .args[0] matches the missing key.
        """
        with self.assertRaises(KeyError) as ctx:
            access_nested_map(nested_map, path)

        # ctx.exception.args[0] contains the actual key that was not found
        self.assertEqual(ctx.exception.args[0], missing_key)


class TestGetJson(unittest.TestCase):
    """Test suite for utils.get_json using mocked HTTP calls (Milestone 1)."""

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
    """Test suite for the memoize decorator (Milestone 2)."""

    def test_memoize(self):
        """
        Define a small TestClass with:
        - a_method() returning 42
        - a_property() decorated with @memoize, which calls a_method()

        Patch a_method so we can count its calls, then call a_property()
        twice and verify that a_method is invoked only once.
        """

        # 1) Define the class inside the test method so the patch decorator can target it.
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        # 2) Create an instance of TestClass
        test_obj = TestClass()

        # 3) Patch the a_method on our TestClass
        with patch.object(TestClass, "a_method", autospec=True) as mock_a_method:
            # 3a) Configure the mock to return 42 when called
            mock_a_method.return_value = 42

            # 4) First call to a_property() should invoke a_method once
            first_result = test_obj.a_property()
            self.assertEqual(first_result, 42)
            mock_a_method.assert_called_once_with(test_obj)

            # 5) Reset the call count on the mock, so we can measure the second invocation
            mock_a_method.reset_mock()

            # 6) Second call to a_property() (exact same arguments) should NOT invoke a_method again
            second_result = test_obj.a_property()
            self.assertEqual(second_result, 42)

            # Verify that a_method was NOT called this time:
            mock_a_method.assert_not_called()


if __name__ == "__main__":
    unittest.main()
