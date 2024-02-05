#!/usr/bin/env python3
"""Test for nested maps
"""


from unittest import TestCase
from unittest.mock import Mock, patch
from parameterized import parameterized
access_nested_map = __import__("utils").access_nested_map
get_json = __import__("utils").get_json
memoize = __import__("utils").memoize


class TestAccessNestedMap(TestCase):
    """Tests the function access_nested_map"""

    @parameterized.expand(
        [
            ({"a": 1}, ("a",), 1),
            ({"a": {"b": 2}}, ("a",), {"b": 2}),
            ({"a": {"b": 2}}, ("a", "b"), 2)
        ]
    )
    def test_access_nested_map(self, nested_map, path, expected):
        """test access_nested_map"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand(
        [
            ({}, ("a",), KeyError),
            ({"a": 1}, ("a", "b"), KeyError)
        ]
    )
    def test_access_nested_map_exception(self, nested_map, path, expected):
        """Test keyError"""
        print(input)
        with self.assertRaises(expected) as test:
            access_nested_map(nested_map, path)


class TestGetJson(TestCase):
    """Tests the get_json function"""

    @parameterized.expand(
        [
            ('http://example.com', {'payload': True}),
            ('http://holberton.io', {'payload': False})
        ]
    )
    def test_get_json(self, url, output):
        """test get_json"""
        response = Mock()
        response.json.return_value = output
        with patch("requests.get", return_value=response):
            self.assertEqual(get_json(url), output)


class TestMemoize(TestCase):
    """Test memoize"""

    def test_memoize(self):
        """test memoize"""

        class TestClass:
            """_summary_
            """

            def a_method(self):
                """_summary_

                Returns:
                        _type_: _description_
                """
                return 42

            @memoize
            def a_property(self):
                """_summary_

                Returns:
                        _type_: _description_
                """
                return self.a_method()

        subject = TestClass()

        with patch.object(subject, "a_method") as a_method:
            a_method.return_value = 52
            a = subject.a_property
            b = subject.a_property

            self.assertEqual(a, 52)
            self.assertEqual(b, 52)
            a_method.assert_called_once()
