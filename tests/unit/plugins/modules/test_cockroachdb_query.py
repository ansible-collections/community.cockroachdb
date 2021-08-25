# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from datetime import timedelta
from decimal import Decimal

import pytest

from ansible_collections.community.cockroachdb.plugins.modules.cockroachdb_query import (
    convert_to_supported,
    fetch_from_cursor,
    get_args,
)


@pytest.mark.parametrize('positional_args,named_args,expected',
    [
        (('not_empty'), None, ('not_empty')),
        (None, ('not_empty'), ('not_empty')),
        (None, None, None),
    ]
)
def test_get_args(positional_args, named_args, expected):
    # We expect that only one or both of them are None
    # as these parameters declared mutually exclusive
    # and this is checked on Ansible engine level.
    # The function returns a parameter that is not None.
    assert get_args(positional_args, named_args) == expected


@pytest.mark.parametrize('input_, expected',
    [
        (timedelta(0, 43200), '12:00:00'),
        (Decimal('1.01'), 1.01),
        ('string', 'string'),
        (None, None),
        (1, 1),
    ]
)
def test_convert_to_supported(input_, expected):
    # The function currently converts decimals to floats
    # and datetime objects to strings. Otherwise,
    # it returns same value without changing it.
    assert convert_to_supported(input_) == expected


@pytest.mark.parametrize('input_, expected',
    [
        ([['first value', timedelta(0, 43200)]], [['first value', '12:00:00']]),
        ([[1, Decimal('1.01')]], [[1, 1.01]]),
        ([['string']], [['string']]),
        ([[None]], [[None]]),
        ([[1], [2], [1, Decimal('1.01')]], [[1], [2], [1, 1.01]]),
        ([[1], [2]], [[1], [2]]),
    ]
)
def test_fetch_from_cursor(input_, expected):
    # fetch_from_cursor function requires an argument
    # of psycopg2 cursor class. In the context
    # of the function, it works as iterator, so we're
    # passing list as input_. It invokes cover_to_support
    # function covered above to convert element
    # of not supported types to appropriate ones.
    assert fetch_from_cursor(input_) == expected
