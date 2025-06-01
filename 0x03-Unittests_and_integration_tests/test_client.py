#!/usr/bin/env python3
"""

Unit tests for client.GithubOrgClient:
- TestGithubOrgClient.org (Milestone 4)
"""

import unittest
from parameterized import parameterized
from unittest.mock import patch
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient.org (Milestone 4)."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """
        For each org_name:
        1) Patch client.get_json to return a fake payload.
        2) Call GithubOrgClient(org_name).org().
        3) Assert get_json was called once with the correct URL.
        4) Assert the return value matches the fake payload.
        """
        # 1) Define a fake payload that get_json will return:
        fake_payload = {"payload_for": org_name}

        # 2) Configure the patched get_json to return fake_payload:
        mock_get_json.return_value = fake_payload

        # 3) Instantiate the client and call .org():
        client = GithubOrgClient(org_name)
        result = client.org()

        # 4) Build the expected URL:
        expected_url = f"https://api.github.com/orgs/{org_name}"

        # 5) Verify get_json was called once with that URL:
        mock_get_json.assert_called_once_with(expected_url)

        # 6) Verify .org() returned fake_payload:
        self.assertEqual(result, fake_payload)

class TestPublicReposURL(unittest.TestCase):
    """Test suite for mocking the readonly _public_repos_url property."""

    def test_public_repos_url(self):
        """
        1) Patch GithubOrgClient.org to return a fake dict with "repos_url".
        2) Access client._public_repos_url.
        3) Assert:
           - org() was called exactly once.
           - The property returned the fake URL.
        """
        # 1) Create a fake dictionary that org() will return
        fake_repos_url = "https://api.github.com/orgs/fake-org/repos"
        fake_org_data = {"repos_url": fake_repos_url}

        # 2) Patch GithubOrgClient.org so it returns fake_org_data
        with patch.object(GithubOrgClient, "org", return_value=fake_org_data) as mock_org:
            # 3a) Instantiate the client
            client = GithubOrgClient("fake-org")

            # 3b) Access the readonly property
            result = client._public_repos_url

            # 3c) Verify org() was called exactly once
            mock_org.assert_called_once_with(client)

            # 3d) Verify the property returned the fake URL
            self.assertEqual(result, fake_repos_url)


if __name__ == "__main__":
    unittest.main()
