#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2022, Andrew Klychkov (@Andersson007) <aaklychkov@mail.ru>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: cockroachdb_db

short_description: Create, modify or delete a CockroachDB database

description:
  - Creates, modifies or deletes a CockroachDB database.

version_added: '0.3.0'

author:
  - Andrew Klychkov (@Andersson007)

extends_documentation_fragment:
  - community.cockroachdb.cockroachdb

notes:
  - Supports C(check_mode).

options:
  name:
    description: Database name to create, modify or delete.
    type: str
    required: yes
'''

EXAMPLES = r'''
# Connect in the verify-full SSL mode to the acme database
# and create the test_db database
- name: Create test_db database
  community.cockroachdb.cockroachdb_query:
    login_host: 192.168.0.10
    login_db: acme
    ssl_mode: verify-full
    ssl_root_cert: /tmp/certs/ca.crt
    ssl_cert: /tmp/certs/client.root.crt
    ssl_key: /tmp/certs/client.root.key
    name: test_db
'''

RETURN = r'''#'''

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.community.cockroachdb.plugins.module_utils.cockroachdb import (
    common_argument_spec,
    CockroachDB,
    get_conn_params,
)


class CockroachDBDatabase():
    def __init__(self, name):
        self.name = name
        self.exists = True

    def exists(self):
        pass

    def create(self):
        pass

    def drop(self):
        pass

    def modify(self):
        return True


def main():
    # Set up arguments
    argument_spec = common_argument_spec()
    argument_spec.update(
        name=dict(type='str'),
        state=dict(type='str', choices=['absent', 'present'], default='present'),
    )

    # Instantiate an object of module class
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    # Assign passed options to variables
    name = module.params['name']
    state = module.params['state']

    # Set defaults
    changed = False

    # Connect to DB, get cursor
    cockroachdb = CockroachDB(module)

    conn = cockroachdb.connect(conn_params=get_conn_params(module.params),
                               autocommit=True, rows_type='dict')
    cursor = conn.cursor()

    # Instantiate the main object here and do the job
    database = CockroachDBDatabase(name)

    # Do job
    if state == 'present':
        if not database.exists:
            database.create()
            changed = True
        else:
            changed = database.modify()

    else:
        # When state is absent
        if database.exists:
            database.drop()
            changed = True

    # Close cursor and conn
    cursor.close()
    conn.close()

    # Users will get this in JSON output after execution
    kw = dict(
        changed=changed,
    )

    module.exit_json(**kw)


if __name__ == '__main__':
    main()
