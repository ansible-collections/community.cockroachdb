#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Andrew Klychkov (@Andersson007) <aaklychkov@mail.ru>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: cockroachdb_info

short_description: Gather information about CockroachDB servers

description:
  - Gather information about CockroachDB servers.

version_added: '0.2.0'

author:
  - Andrew Klychkov (@Andersson007)

extends_documentation_fragment:
  - community.cockroachdb.cockroachdb

notes:
  - Supports C(check_mode).
'''

EXAMPLES = r'''
- name: Fetch information from CockroachDB
  community.cockroachdb.cockroachdb_info:
  register: result

- name: Print information returned from the previous task
  ansible.builtin.debug:
    var: result
    verbosity: 2

- name: Fetch information using non-default credentials and SSL
  community.cockroachdb.cockroachdb_info:
    login_host: 192.168.1.10
    login_db: acme
    login_user: django
    login_password: mysecretpass
    ssl_mode: verify-full
    ssl_root_cert: /tmp/certs/ca.crt
    ssl_cert: /tmp/certs/client.root.crt
    ssl_key: /tmp/certs/client.root.key
  register: result

- name: Print information returned from the previous task
  ansible.builtin.debug:
    var: result
    verbosity: 2
'''

RETURN = r''' # '''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native

from ansible_collections.community.cockroachdb.plugins.module_utils.cockroachdb import (
    common_argument_spec,
    CockroachDB,
    get_conn_params,
)


def exec_query(module, cursor, query):
    try:
        cursor.execute(query)
    except Exception as e:
        module.fail_json('Failed to execute query "%s": %s' % (query, to_native(e)))

    try:
        res = cursor.fetchall()
    except Exception as e:
        module.fail_json('Failed to fetch rows for query "%s" '
                         'from cursor: %s' % (query, to_native(e)))

    return res


def extract_server_ver(ver_str):
    version_info = {}
    version_info['raw'] = ver_str

    try:
        tmp = ver_str.split('.')[:3]
        version_info['year'] = int(tmp[0][-2:])
        version_info['release'] = int(tmp[1])
        version_info['patch'] = int(tmp[2].split(' ')[0])
    except Exception as e:
        version_info['error'] = to_native(e)
        return (version_info, False)

    return (version_info, True)


def get_server_version(module, cursor):
    res = exec_query(module, cursor, 'SELECT VERSION()')

    v_info, ok = extract_server_ver(res[0][0])
    if not ok:
        msg = ('Cannot fetch version from '
               '"%s": %s' % (v_info['raw'], v_info['error']))
        module.fail_json(msg)

    return v_info


def main():
    # Set up arguments
    argument_spec = common_argument_spec()

    # Instantiate an object of module class
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    # Connect to DB, get cursor
    cockroachdb = CockroachDB(module)

    conn = cockroachdb.connect(conn_params=get_conn_params(module.params),
                               autocommit=True)
    cursor = conn.cursor()

    # Dictionary that will contain server information.
    # We will return it to users at the end
    server_info = {
        'version': {},
    }

    # Collect info
    # TODO: implement via loop with filtering
    server_info['version'] = get_server_version(module, cursor)

    # Close cursor and conn
    try:
        cursor.close()
        conn.close()
    except Exception:
        pass

    module.exit_json(changed=False, **server_info)


if __name__ == '__main__':
    main()