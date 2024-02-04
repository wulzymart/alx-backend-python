#!/usr/bin/env python3
"""Test for nested maps
"""


from unittest import TestCase
from parameterized import parameterized
access_nested_map = __import__("utils").access_nested_map


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
        self.assertEquals(access_nested_map(nested_map, path), expected)

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


