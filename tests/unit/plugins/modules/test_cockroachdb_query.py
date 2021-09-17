# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from datetime import timedelta
from decimal import Decimal

import pytest

from ansible_collections.community.cockroachdb.plugins.modules.cockroachdb_query import (
    convert_to_supported,
    execute,
    fetch_from_cursor_dict,
    fetch_from_cursor_tuple,
    get_args,
)


@pytest.mark.parametrize('positional_args,named_args,expected', [
    (('not_empty'), None, ('not_empty')),
    (None, ('not_empty'), ('not_empty')),
    (None, None, None),
])
def test_get_args(positional_args, named_args, expected):
    # We expect that only one or both of them are None
    # as these parameters declared mutually exclusive
    # and this is checked on Ansible engine level.
    # The function returns a parameter that is not None.
    assert get_args(positional_args, named_args) == expected


@pytest.mark.parametrize('input_, expected', [
    (timedelta(0, 43200), '12:00:00'),
    (Decimal('1.01'), 1.01),
    ('string', 'string'),
    (None, None),
    (1, 1),
])
def test_convert_to_supported(input_, expected):
    # The function currently converts decimals to floats
    # and datetime objects to strings. Otherwise,
    # it returns same value without changing it.
    assert convert_to_supported(input_) == expected


@pytest.mark.parametrize('input_, expected', [
    ([('first value', timedelta(0, 43200))], [('first value', '12:00:00')]),
    ([(1, Decimal('1.01'))], [(1, 1.01)]),
    ([('string')], [('string')]),
    ([(None)], [(None)]),
    ([(1), (2), (1, Decimal('1.01'))], [(1), (2), (1, 1.01)]),
    ([(1), (2)], [(1), (2)]),
])
def test_fetch_from_cursor_tuple(input_, expected):
    # fetch_from_cursor_tuple function requires an argument
    # of psycopg2 cursor class. In the context
    # of the function, it works as iterator, so we're
    # passing lists as input_. It invokes cover_to_support
    # function covered above to convert elements
    # of not supported types to appropriate ones.
    assert fetch_from_cursor_tuple(input_) == expected


@pytest.mark.parametrize('input_, expected', [
    ([{1: 'first value', 2: timedelta(0, 43200)}], [{1: 'first value', 2: '12:00:00'}]),
    ([{1: 1, 2: Decimal('1.01')}], [{1: 1, 2: 1.01)}),
    ([{1: 'string'}], [{2: 'string'}]),
    ([{1: None}], [{2: None}]),
    ([{1: 1}, {2: 2}, {1: 1, 2: Decimal('1.01')}], [{1: 1}, {2: 2}, {1: 1, 2: 1.01}]),
    ([{1: 1}, {2: 2}], [{1: 1}, {2: 2}]),
])
def test_fetch_from_cursor_dict(input_, expected):
    # fetch_from_cursor_dict function requires an argument
    # of psycopg2 cursor class. In the context
    # of the function, it works as iterator, so we're
    # passing lists as input_. It invokes cover_to_support
    # function covered above to convert elements
    # of not supported types to appropriate ones.
    assert fetch_from_cursor_dict(input_) == expected


@pytest.mark.parametrize('sequence,expected', [
    ([('first value', timedelta(0, 43200))], [('first value', '12:00:00')]),
    ([(1, Decimal('1.01'))], [(1, 1.01)]),
    ([('string')], [('string')]),
    ([(None)], [(None)]),
    ([(1), (2), (1, Decimal('1.01'))], [(1), (2), (1, 1.01)]),
    ([(1), (2)], [(1), (2)]),
])
def test_execute(sequence, expected):
    # The execute function invokes a passed fetch_from_cursor function
    # that, in turn, invokes the convert_to_supported function
    # to handle fetched from cursor elements when deeded.
    # So we expect that unsupported elements will be converted,
    # for example those timedelta and Decimal values in
    # @pytest.mark.parametrize arguments
    class Cursor():
        """Fake cursor class"""
        # These are fake results that the cursor will
        # return when iterating through it
        def __init__(self, sequence):
            # Just fillers
            self.sequence = sequence
            self.statusmessage = 'blahblah'
            self.rowcount = len(self.sequence)
            self.query = None
            self.args = None

        def execute(self, query, args):
            self.query = query
            self.args = args

        def mogrify(self, query, args):
            return query, args

        def __iter__(self):
            for item in self.sequence:
                yield item

    class Module():
        """Fake module class"""
        def fail_json(self, msg=None):
            # For debugging. Also comment out PsycopgProgrammingError
            # exception in the module's file
            print(msg)

    module = Module()
    cursor = Cursor(sequence)
    query = 'SELECT 1'
    args = (1, 2, 3)

    # Invoke the function
    statusmessage, rowcount, query, res = execute(module, cursor,
                                                  query, args, fetch_from_cursor_tuple)

    # Check results
    assert statusmessage == 'blahblah'
    assert rowcount == len(sequence)
    assert res == expected
    assert cursor.query == 'SELECT 1'
    assert cursor.args == (1, 2, 3)
    assert query == ('SELECT 1', (1, 2, 3))
