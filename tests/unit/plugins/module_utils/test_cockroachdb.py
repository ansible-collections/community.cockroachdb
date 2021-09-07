# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest

from ansible_collections.community.cockroachdb.plugins.module_utils.cockroachdb import (
    common_argument_spec,
    get_conn_params,
    get_params_map,
)


def test_common_argument_spec():
    EXPECTED = {
        'login_db': {'type': 'str'},
        'login_port': {'default': 26257, 'type': 'int'},
        'login_user': {'default': 'root', 'type': 'str'},
        'login_host': {'default': 'localhost', 'type': 'str'},
        'login_unix_socket': {'type': 'path'},
        'login_password': {'type': 'str', 'no_log': True},
        'ssl_mode': {
            'type': 'str',
            'default': 'prefer',
            'choices': [
                'allow',
                'disable',
                'prefer',
                'require',
                'verify-ca',
                'verify-full',
            ],
        },
        'ssl_root_cert': {'type': 'path'},
        'ssl_key': {'type': 'path'},
        'ssl_cert': {'type': 'path'},
    }

    assert common_argument_spec() == EXPECTED


def test_get_params_map():
    EXPECTED = {
        'login_db': 'database',
        'login_host': 'host',
        'login_user': 'user',
        'login_password': 'password',
        'login_port': 'port',
        'ssl_mode': 'sslmode',
        'ssl_root_cert': 'sslrootcert',
        'ssl_cert': 'sslcert',
        'ssl_key': 'sslkey',
    }

    assert get_params_map() == EXPECTED


@pytest.mark.parametrize(
    'input_,expected',
    [
        (   # input dict
            {'login_host': 'localhost',
             'login_db': 'test',
             'login_unix_socket': None,
             'login_user': 'root',
             'login_password': 'blah',
             'login_port': 1234,
             'ssl_mode': 'verify-full',
             'ssl_root_cert': '/path',
             'ssl_cert': '/path',
             'ssl_key': '/path'},
            # expected dict
            {'host': 'localhost',
             'database': 'test',
             'user': 'root',
             'password': 'blah',
             'port': 1234,
             'sslmode': 'verify-full',
             'sslrootcert': '/path',
             'sslcert': '/path',
             'sslkey': '/path'},
        ),
        (   # input dict
            {'login_unix_socket': '/path',
             'login_user': 'root',
             'login_password': 'blah'},
            # expected dict
            {'host': '/path',
             'user': 'root',
             'password': 'blah'}
        ),
        (   # input dict
            {'login_host': 'localhost',
             'login_unix_socket': '/path',
             'login_user': 'root',
             'login_password': 'blah'},
            # expected dict
            {'host': '/path',
             'user': 'root',
             'password': 'blah'}
        ),
        (   # input dict
            {'login_host': None,
             'login_unix_socket': '/path',
             'login_user': 'root',
             'login_password': 'blah'},
            # expected dict
            {'host': '/path',
             'user': 'root',
             'password': 'blah'}
        ),
        (   # input dict
            {'login_host': '127.0.0.1',
             'login_unix_socket': '/path',
             'login_user': 'root',
             'login_password': 'blah'},
            # expected dict
            {'host': '/path',
             'user': 'root',
             'password': 'blah'}
        ),
        (   # input dict
            {'login_host': '192.168.0.1',
             'login_unix_socket': '/path',  # should be ignored
             'login_user': 'root',
             'login_password': 'blah'},
            # expected dict
            {'host': '192.168.0.1',
             'user': 'root',
             'password': 'blah'}
        )
    ]
)
def test_get_conn_params(input_, expected):
    assert get_conn_params(input_) == expected
