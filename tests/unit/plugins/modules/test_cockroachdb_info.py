# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.community.cockroachdb.plugins.modules.cockroachdb_info import (
    exec_query,
    extract_server_ver,
    get_databases,
    get_server_version,
)


@pytest.mark.parametrize('_input,expected', [
    (
        'CockroachDB CCL v21.1.6 blah',
        ({'raw': 'CockroachDB CCL v21.1.6 blah', 'year': 21, 'release': 1, 'patch': 6}, True)
    ),
    (
        'CockroachDB CCL v22.2.16 blah',
        ({'raw': 'CockroachDB CCL v22.2.16 blah', 'year': 22, 'release': 2, 'patch': 16}, True)
    ),
    (
        'CockroachDB CCL v23.4.0 blah',
        ({'raw': 'CockroachDB CCL v23.4.0 blah', 'year': 23, 'release': 4, 'patch': 0}, True)
    ),
])
def test_extract_server_ver(_input, expected):
    assert extract_server_ver(_input) == expected


@pytest.mark.parametrize('_input,expected', [
    (
        'blah blah',
        ({'raw': 'blah blah', 'error': "invalid literal for int() with base 10: 'ah'"}, False)
    ),
    (
        'CockroachDB CCL v21.1.something wrong',
        ({'raw': 'CockroachDB CCL v21.1.something wrong', 'year': 21, 'release': 1, 'error': "invalid literal for int() with base 10: 'something'"}, False)
    ),
    ('', ({'raw': '', 'error': "invalid literal for int() with base 10: ''"}, False)),
])
def test_extract_server_ver_fail_cases(_input, expected):
    assert extract_server_ver(_input) == expected


# Installing, importing and monkeypatching psycopg2.Cursor
# would be an extra thing here, so I'll use a dummy class
class Cursor():
    def __init__(self):
        self.query = None

    def execute(self, query):
        pass

    def fetchall(self):
        pass


def raise_(ex):
    """Universal raiser needed for lambdas."""
    raise ex


def test_exec_query(monkeypatch):
    monkeypatch.setattr(Cursor, 'fetchall', lambda self: True)
    monkeypatch.setattr(AnsibleModule, '__init__', lambda self: None)

    module = AnsibleModule()
    cursor = Cursor()
    query = 'SELECT VERSION()'

    assert exec_query(module, cursor, query) is True


# Method for monkeypatching AnsibleModule.__init__ method
def mock__init__(self):
    self.fail_msg = None


# Method for monkeypatching AnsibleModule.fail_json method
def mock_fail_json(self, msg):
    self.fail_msg = msg


def test_exec_query_fail_execute(monkeypatch):
    monkeypatch.setattr(Cursor, 'execute',
                        lambda self, x: raise_(ValueError('Fake cursor.execute() failing.')))
    monkeypatch.setattr(AnsibleModule, '__init__', mock__init__)
    monkeypatch.setattr(AnsibleModule, 'fail_json', mock_fail_json)

    module = AnsibleModule()
    cursor = Cursor()
    query = 'SELECT VERSION()'

    exec_query(module, cursor, query)

    assert module.fail_msg == ('Failed to execute query "SELECT VERSION()": '
                               'Fake cursor.execute() failing.')


def test_exec_query_fail_fetchall(monkeypatch):
    monkeypatch.setattr(Cursor, 'fetchall',
                        lambda self: raise_(ValueError('Fake cursor.fetchall() failing.')))
    monkeypatch.setattr(AnsibleModule, '__init__', mock__init__)
    monkeypatch.setattr(AnsibleModule, 'fail_json', mock_fail_json)

    module = AnsibleModule()
    cursor = Cursor()
    query = 'SELECT VERSION()'

    exec_query(module, cursor, query)

    assert module.fail_msg == ('Failed to fetch rows for query "SELECT VERSION()" '
                               'from cursor: Fake cursor.fetchall() failing.')


@pytest.mark.parametrize('fetchall_out,expected', [
    ([{'database_name': 'postgres', 'comment': None}], {'postgres': {'comment': None}}),
    ([{'database_name': 'postgres', 'comment': 'test'}], {'postgres': {'comment': 'test'}}),
    (
        [
            {'database_name': 'postgres', 'comment': 'test0'},
            {'database_name': 'test', 'comment': 'test1'},
        ],
        {'postgres': {'comment': 'test0'}, 'test': {'comment': 'test1'}},
    )]
)
def test_get_databases(monkeypatch, fetchall_out, expected):
    monkeypatch.setattr(Cursor, 'execute', lambda self, x: None)
    monkeypatch.setattr(Cursor, 'fetchall', lambda self: fetchall_out)
    monkeypatch.setattr(AnsibleModule, '__init__', mock__init__)
    monkeypatch.setattr(AnsibleModule, 'fail_json', mock_fail_json)

    module = AnsibleModule()
    cursor = Cursor()

    assert get_databases(module, cursor) == expected
