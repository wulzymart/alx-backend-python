#!/usr/bin/env python3
"""A module for testing the client module.
"""
from unittest import TestCase
from typing import Dict
from unittest.mock import (
    MagicMock,
    Mock,
    PropertyMock,
    patch,
)
from parameterized import parameterized, parameterized_class
from requests import HTTPError
from fixtures import TEST_PAYLOAD
GithubOrgClient = __import__("client").GithubOrgClient


class TestGithubOrgClient(TestCase):
    """test githuborgclient"""

    @parameterized.expand([
        ("google", {"name": "google"}),
        ("abc", {'name': "abc"}),
    ])
    @patch(
        "client.get_json",
    )
    def test_org(self, org: str, res: Dict,
                 mocked_fn: MagicMock) -> None:
        """Test org method"""
        mocked_fn.return_value = MagicMock(
            return_value=res)
        client = GithubOrgClient(org)
        self.assertEqual(client.org(), res)
        mocked_fn.assert_called_once_with(
            f"https://api.github.com/orgs/{org}"
        )

    def test_public_repos_url(self) -> None:
        """test public_repos_url"""
        with patch(
            "client.GithubOrgClient.org",
            new_callable=PropertyMock,
        ) as org:
            org.return_value = {
                'repos_url': "https://api.github.com/users/abc/repos",
            }
            self.assertEqual(
                GithubOrgClient("abc")._public_repos_url,
                "https://api.github.com/users/abc/repos",
            )

    @patch("client.get_json")
    def test_public_repos(self, get_json: MagicMock) -> None:
        """test public_repos"""
        payload = {
            'repos_url': "https://api.github.com/users/google/repos",
            'repos': [
                {
                    "id": 7697149,
                    "name": "episodes.dart",
                    "private": False,
                    "owner": {
                        "login": "google",
                        "id": 1342004,
                    },
                    "fork": False,
                    "url": "https://api.github.com/repos/google/episodes.dart",
                    "created_at": "2013-01-19T00:31:37Z",
                    "updated_at": "2019-09-23T11:53:58Z",
                    "has_issues": True,
                    "forks": 22,
                    "default_branch": "master",
                },
                {
                    "id": 8566972,
                    "name": "kratu",
                    "private": False,
                    "owner": {
                        "login": "google",
                        "id": 1342004,
                    },
                    "fork": False,
                    "url": "https://api.github.com/repos/google/kratu",
                    "created_at": "2013-03-04T22:52:33Z",
                    "updated_at": "2019-11-15T22:22:16Z",
                    "has_issues": True,
                    "forks": 32,
                    "default_branch": "master",
                },
            ]
        }
        get_json.return_value = payload["repos"]
        with patch(
            "client.GithubOrgClient._public_repos_url",
            new_callable=PropertyMock,
        ) as _public_repos_url:
            _public_repos_url.return_value = payload["repos_url"]
            self.assertEqual(
                GithubOrgClient("google").public_repos(),
                [
                    "episodes.dart",
                    "kratu",
                ],
            )
            _public_repos_url.assert_called_once()
        get_json.assert_called_once()

    @parameterized.expand([
        ({'license': {'key': "my_license"}}, "my_license", True),
        ({'license': {'key': "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo: Dict, key: str, output: bool) -> None:
        """Tests has_license."""
        client = GithubOrgClient("google")
        has_licence = client.has_license(repo, key)
        self.assertEqual(has_licence, output)


@parameterized_class([
    {
        'org_payload': TEST_PAYLOAD[0][0],
        'repos_payload': TEST_PAYLOAD[0][1],
        'expected_repos': TEST_PAYLOAD[0][2],
        'apache2_repos': TEST_PAYLOAD[0][3],
    },
])
class TestIntegrationGithubOrgClient(TestCase):
    """Integration test"""
    @classmethod
    def setUpClass(cls) -> None:
        """setup for integration"""
        url_res = {
            'https://api.github.com/orgs/google': cls.org_payload,
            'https://api.github.com/orgs/google/repos': cls.repos_payload,
            'https://api.github.com/orgs/abc': cls.org_payload,
            'https://api.github.com/orgs/abc/repos': cls.repos_payload,
        }

        def get_payload(url):
            if url in url_res:
                response = Mock()
                response.json.return_value = url_res[url]
                return response
            return HTTPError

        cls.get_patcher = patch("requests.get", side_effect=get_payload)
        cls.get_patcher.start()

    def test_public_repos(self) -> None:
        """test public repos"""
        self.assertEqual(
            GithubOrgClient("google").public_repos(),
            self.expected_repos,
        )
        self.assertEqual(
            GithubOrgClient("google").org,
            self.org_payload,
        )
        self.assertEqual(
            GithubOrgClient("abc").public_repos(),
            self.expected_repos,
        )
        self.assertEqual(
            GithubOrgClient("abc").org,
            self.org_payload,
        )

    def test_public_repos_with_license(self) -> None:
        """repos with licese
        """
        self.assertEqual(
            GithubOrgClient("google").public_repos(license="apache-2.0"),
            self.apache2_repos,
        )
        self.assertEqual(
            GithubOrgClient("abc").public_repos(license="apache-2.0"),
            self.apache2_repos,
        )

    @classmethod
    def tearDownClass(cls) -> None:
        """tear down class"""
        cls.get_patcher.stop()
