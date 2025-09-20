#!/usr/bin/env python3
"""
Unit tests for client.GithubOrgClient
"""

import unittest
from parameterized import parameterized
from unittest.mock import patch

from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """
        Test that GithubOrgClient.org returns the correct value
        and calls get_json with the expected URL.
        """
        fake_payload = {"login": org_name}
        mock_get_json.return_value = fake_payload

        client = GithubOrgClient(org_name)
        result = client.org

        self.assertEqual(result, fake_payload)

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
