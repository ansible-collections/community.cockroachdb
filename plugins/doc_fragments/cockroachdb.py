# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


class ModuleDocFragment(object):
    DOCUMENTATION = r'''
options:
  login_db:
    description:
      - Database name to connect to.
    type: str

  login_user:
    description:
      - User name used to connect to the database.
    type: str
    default: root

  login_password:
    description:
      - The password of the I(login_user).
    type: str

  login_host:
    description:
      - Host running the database.
    type: str
    default: localhost

  login_unix_socket:
    description:
      - Path to a directory containing a Unix domain socket for local connections.
    type: path

  login_port:
    description:
      - Database port to connect to.
    type: int
    default: 26257

  ssl_mode:
    description:
      - Determines whether or with what priority a secure SSL TCP/IP
        connection will be negotiated with the server.
      - Refer to U(https://www.postgresql.org/docs/current/static/libpq-ssl.html)
        for more information on the modes.
      - Default of C(prefer) matches libpq default.
    type: str
    default: prefer
    choices: [ allow, disable, prefer, require, verify-ca, verify-full ]

  ssl_root_cert:
    description:
      - Specifies the name of a file containing SSL certificate
        authority (CA) certificate(s).
      - If the file exists, the server's certificate will be verified
        to be signed by one of these authorities.
    type: path

  ssl_cert:
    description:
      - Specifies the file name of the client SSL certificate.
    type: path

  ssl_key:
    description:
      - Specifies the location for the secret key used for the client certificate.
    type: path

notes:
  - This module uses C(psycopg2), a Python PostgreSQL database driver.
    Be ensure the driver is installed on the target host before using this module.

requirements:
  - psycopg2
'''
