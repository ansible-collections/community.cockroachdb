# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from datetime import timedelta
from decimal import Decimal

import pytest

from ansible_collections.community.cockroachdb.plugins.modules.cockroachdb_query import (
    convert_to_supported,
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
