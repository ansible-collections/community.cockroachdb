# This code is part of Ansible, but is an independent component.
# This particular file snippet, and this file snippet only, is BSD licensed.
# Modules you write using this snippet, which is embedded dynamically by Ansible
# still belong to the author of the module, and may assign their own license
# to the complete work.
#
# Simplified BSD License
# (see licenses/simplified_bsd.txt or https://opensource.org/licenses/BSD-2-Clause)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

psycopg2 = None
try:
    import psycopg2
    HAS_PSYCOPG2 = True
except ImportError:
    HAS_PSYCOPG2 = False

from ansible.module_utils.basic import missing_required_lib
from ansible.module_utils._text import to_native
from ansible.module_utils.six import iteritems
from distutils.version import LooseVersion


def cockroachdb_common_argument_spec():
    """
    Return a dictionary with common options.

    The options are used by most of CockroachDB modules.
    """
    return dict(
        login_user=dict(default='root'),
        login_password=dict(default='', no_log=True),
        login_host=dict(default='localhost'),
        login_unix_socket=dict(default=''),
        login_port=dict(type='int', default=26257),
        ssl_mode=dict(
            default='prefer',
            choices=[
                'allow',
                'disable',
                'prefer',
                'require',
                'verify-ca',
                'verify-full',
            ],
        ),
        ssl_root_cert=dict(type='path'),
        ssl_cert=dict(type='path'),
        ssl_key=dict(type='path'),
    )


def ensure_required_libs(module):
    """Check required libraries.

    Args:
        module (AnsibleModule) -- object of ansible.module_utils.basic.AnsibleModule class
    """
    if not HAS_PSYCOPG2:
        module.fail_json(msg=missing_required_lib('psycopg2'))

    if module.params.get('ca_cert') and LooseVersion(psycopg2.__version__) < LooseVersion('2.4.3'):
        module.fail_json(msg='psycopg2 must be at least 2.4.3 in order to use the ca_cert parameter')


class CockroachDB():
    """Class for working with CockroachDB.

    Args:
        module (AnsibleModule) -- object of ansible.module_utils.basic.AnsibleModule class
    """
    def __init__(self, module):
        self.module = module
        self.connection = None

    def connect(self, conn_params, autocommit=False, fail_on_conn=True):
        """Connect to a CockroachDB database.

        Return psycopg2 connection object.

        Args:
            conn_params (dict) -- dictionary with connection parameters

        Kwargs:
            autocommit (bool) -- commit automatically (default False)
            fail_on_conn (bool) -- fail if connection failed or just warn and return None (default True)
        """
        ensure_required_libs(self.module)

        try:
            self.connection = psycopg2.connect(**conn_params)
            if autocommit:
                if LooseVersion(psycopg2.__version__) >= LooseVersion('2.4.2'):
                    self.connection.set_session(autocommit=True)
                else:
                    self.connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

        except Exception as e:
            if fail_on_conn:
                self.module.fail_json(msg="unable to connect to database: %s" % to_native(e))
            else:
                self.module.warn("CockroachDB server is unavailable: %s" % to_native(e))
                self.connection = None

        return self.connection


def get_params_map():
    """Get params map for mapping collection-related module options
    to psycopg2.connect() arguments.

    Returns dictionary.
    """
    return {
        'login_host': 'host',
        'login_user': 'user',
        'login_password': 'password',
        'login_port': 'port',
        'ssl_mode': 'sslmode',
        'ssl_root_cert': 'sslrootcert',
        'ssl_cert': 'sslcert',
        'ssl_key': 'sslkey',
    }


def get_conn_params(params_dict):
    """Get connection parameters from the passed dictionary.

    Return a dictionary with parameters to connect to CockroachDB server.

    Args:
        params_dict (dict) -- dictionary with variables
    """
    # To use defaults values, keyword arguments must be absent, so
    # check which values are empty and don't include in the return dictionary
    params_map = get_params_map()

    kw = dict((params_map[k], v) for (k, v) in iteritems(params_dict)
              if k in params_map and v != '' and v is not None)

    # If a login_unix_socket is specified, incorporate it here.
    is_localhost = "host" not in kw or kw["host"] is None or kw["host"] == "localhost"
    if is_localhost and params_dict["login_unix_socket"] != "":
        kw["host"] = params_dict["login_unix_socket"]

    return kw