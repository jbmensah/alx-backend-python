#!/usr/bin/env python3
"""
tests/test_client.py

Unit tests for client.GithubOrgClient:
- test_org (Task 4)
- test_public_repos_url (Task 5)
- test_public_repos (Task 6)
"""

import unittest
from parameterized import parameterized
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient.org (Task 4)."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json", autospec=True)
    def test_org(self, org_name, mock_get_json):
        """
        1) Patch client.get_json so it returns a fake payload.
        2) Call GithubOrgClient(org_name).org().
        3) Assert get_json called once with correct URL.
        4) Assert return value matches fake payload.
        """
        fake_payload = {"payload_for": org_name}
        mock_get_json.return_value = fake_payload

        client = GithubOrgClient(org_name)
        result = client.org()

        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)
        self.assertEqual(result, fake_payload)

    def test_public_repos_url(self):
        """
        1) Patch GithubOrgClient.org so it returns a fake dict with "repos_url".
        2) Access client._public_repos_url.
        3) Assert:
           - org() was called once with client as argument.
           - property returned the fake URL.
        """
        fake_repos_url = "https://api.github.com/orgs/fake-org/repos"
        fake_org_data = {"repos_url": fake_repos_url}

        with patch.object(
            GithubOrgClient, "org", autospec=True, return_value=fake_org_data
        ) as mock_org:
            client = GithubOrgClient("fake-org")
            result = client._public_repos_url

            mock_org.assert_called_once_with(client)
            self.assertEqual(result, fake_repos_url)

    @patch("client.get_json", autospec=True)
    def test_public_repos(self, mock_get_json):
        """
        1) Patch get_json so it returns a fake list of repos.
        2) Patch _public_repos_url to return a fake URL.
        3) Call public_repos() and verify:
           - _public_repos_url was accessed once.
           - get_json was called once with fake URL.
           - Returned list of names matches fake payload.
        """
        fake_url = "https://api.github.com/orgs/fake-org/repos"
        fake_repos_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
        ]
        mock_get_json.return_value = fake_repos_payload

        with patch.object(
            GithubOrgClient, "_public_repos_url", new_callable=PropertyMock
        ) as mock_pub_url:
            mock_pub_url.return_value = fake_url

            client = GithubOrgClient("fake-org")
            result = client.public_repos()

            # PropertyMock is called without arguments; check that
            mock_pub_url.assert_called_once()

            mock_get_json.assert_called_once_with(fake_url)
            self.assertEqual(result, ["repo1", "repo2"])


if __name__ == "__main__":
    unittest.main()
