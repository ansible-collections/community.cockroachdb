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

options:
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
from ansible.module_utils.six import iteritems

from ansible_collections.community.cockroachdb.plugins.module_utils.cockroachdb import (
    common_argument_spec,
    CockroachDB,
    get_conn_params,
)


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
                               autocommit=True, rows_type='dict')
    cursor = conn.cursor()

    # Close cursor and conn
    try:
        cursor.close()
        conn.close()
    except Exception:
        pass

    # Users will get this in JSON output after execution
    kw = dict(
        changed=False,
    )

    module.exit_json(**kw)


if __name__ == '__main__':
    main()
