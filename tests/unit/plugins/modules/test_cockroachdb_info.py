# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest

from ansible_collections.community.cockroachdb.plugins.modules.cockroachdb_info import (
    exec_query,
    extract_server_ver,
    get_server_version,
)


@pytest.mark.parametrize('_input,expected', [
    ('CockroachDB CCL v21.1.6 blah', (
        {'raw': 'CockroachDB CCL v21.1.6 blah', 'year': 21, 'release': 1, 'patch': 6}, True
    )),
    ('CockroachDB CCL v22.2.16 blah', (
        {'raw': 'CockroachDB CCL v22.2.16 blah', 'year': 22, 'release': 2, 'patch': 16}, True
    )),
    ('CockroachDB CCL v23.4.0 blah', (
        {'raw': 'CockroachDB CCL v23.4.0 blah', 'year': 23, 'release': 4, 'patch': 0}, True
    )),
])
def test_extract_server_ver(_input, expected):
    assert extract_server_ver(_input) == expected


@pytest.mark.parametrize('_input,expected', [
    ('blah blah',
        ({'raw': 'blah blah', 'error': "invalid literal for int() with base 10: 'ah'"}, False
    )),
    ('CockroachDB CCL v21.1.something wrong', (
        {'raw': 'CockroachDB CCL v21.1.something wrong',
         'year': 21,
         'release': 1,
         'error': "invalid literal for int() with base 10: 'something'"}, False
    )),
    ('', ({'raw': '', 'error': "invalid literal for int() with base 10: ''"}, False)),
])
def test_extract_server_ver_fail_cases(_input, expected):
    assert extract_server_ver(_input) == expected
