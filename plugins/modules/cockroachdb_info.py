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
    """Execute a query and return a dict of fetched rows.

    The module argument is an Ansible module object.
    Within this function it's used to tell Ansible
    that we want the task to fail and show a user a certain error message.
    """
    res = None

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
    """Take version string and return version dictionary.

    The ver_str argument can look like 'CockroachDB CCL v21.1.6 ...'.
    The function extracts values from the argument and return a dictionary.

    Example of return value:
    {
        'raw': 'CockroachDB CCL v21.1.6 ...',
        'year': 21,
        'release': 1,
        'patch': 6,
    }
    """
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
    """Get a server version from a server and return version dict.

    The module argument is an Ansible module object.
    Within this function it's used to tell Ansible
    that we want the task to fail and show a user a certain error message.

    Example of return value:
    {
        'raw': 'CockroachDB CCL v21.1.6 ...',
        'year': 21,
        'release': 1,
        'patch': 6,
    }
    """
    res = exec_query(module, cursor, 'SELECT VERSION() AS version')

    v_info, ok = extract_server_ver(res[0]['version'])
    if not ok:
        msg = ('Cannot fetch version from '
               '"%s": %s' % (v_info['raw'], v_info['error']))
        module.fail_json(msg)

    return v_info


def get_info(module, cursor, query, root_key, fields):
    """Get info from a server.

    As the rows returned by exec_query are a list of dictionaries,
    for example, [{'user_name': 'Bob', 'member_of': [], 'options': None}],
    you want to get user info you need pass 'SHOW USERS'
    as the query argument, 'user_name' as the root_key argument,
    and ['member_of', 'options'] as the fields argument, so that
    you'll get the {'Bob': {'member_of': [], 'options': None}} dict
    as a return value.

    Args:
        module (AnsibleModule) - AnsibleModule class object
        cursor (psycopg2.Cursor) - psycopg2.Cursor class object
        query (string) - query to pass to the exec_query function
        root_key (string) - key that should be a root key of the ret dict
        fields (list) - list of strings that represents fields
            we wanna get

    Return a dictionary containing info.
    """
    res = exec_query(module, cursor, query)

    if not res:
        return {}

    info = {}
    for row in res:
        root = row[root_key]
        info[root] = {}

        for field in fields:
            if field in row:
                info[root][field] = row[field]

    return info


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
    server_info = {}

    # Collect info
    server_info['version'] = get_server_version(module, cursor)
    server_info['databases'] = get_info(module, cursor,
                                        'SHOW DATABASES WITH COMMENT',
                                        'database_name',
                                        ['comment', 'owner', 'primary_region',
                                         'regions', 'survival_goal'])
    server_info['users'] = get_info(module, cursor, 'SHOW USERS', 'username',
                                    ['member_of', 'options'])
    server_info['settings'] = get_info(module, cursor, 'SHOW ALL CLUSTER SETTINGS',
                                       'variable', ['value', 'setting_type'])
    server_info['regions'] = get_info(module, cursor, 'SHOW REGIONS FROM CLUSTER',
                                      'region', ['zones'])

    # Close cursor and conn
    cursor.close()
    conn.close()

    module.exit_json(changed=False, **server_info)


if __name__ == '__main__':
    main()
