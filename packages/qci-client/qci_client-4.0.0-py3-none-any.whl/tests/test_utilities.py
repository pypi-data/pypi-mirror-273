# Copyright 2023-2024, Quantum Computing Incorporated
"""Test package-wide utilities."""

import unittest

import pytest
import requests

from qci_client.utilities import raise_for_status


@pytest.mark.offline
class TestUtilities(unittest.TestCase):
    """Utilities-related test suite."""

    def test_raise_for_status_ok(self):
        """Test test_raise_for_status utility."""
        response_bytes = '{"success": true}'.encode("utf-8")
        response = requests.Response()
        response.url = "https://example.com"
        response.status_code = requests.codes.ok  # pylint: disable=no-member
        response.reason = "OK"
        response._content = response_bytes  # pylint: disable=protected-access
        # This should not raise.
        raise_for_status(response=response)

    def test_raise_for_status_not_ok(self):
        """Test test_raise_for_status utility."""
        response_bytes = '{"message": "Field is missing"}'.encode("utf-8")
        response = requests.Response()
        response.url = "https://example.com"
        response.status_code = requests.codes.bad_request  # pylint: disable=no-member
        response.reason = "Bad Request"
        response._content = response_bytes  # pylint: disable=protected-access

        with self.assertRaises(requests.HTTPError) as context:
            raise_for_status(response=response)

        self.assertEqual(
            str(context.exception),
            "400 Client Error: Bad Request for url: https://example.com with response "
            'body: {"message": "Field is missing"}',
        )
