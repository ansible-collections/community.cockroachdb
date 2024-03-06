==============================================
Community CockroachDB Collection Release Notes
==============================================

.. contents:: Topics


v0.3.1
======

Release Summary
---------------

This is a patch release of the community.cockroachdb collection.

Bugfixes
--------

- cockroachdb_db - fix the broken ``owner`` argument.

v0.3.0
======

Release Summary
---------------

This is the minor release of the ``community.cockroachdb`` collection.
This changelog contains all changes to the modules and plugins in this collection
that have been made after the previous release.

Bugfixes
--------

- Collection core functions - change place where the required libs check is invoked to avoid unexpected errors when psycopg2 is missed (https://github.com/ansible-collections/community.cockroachdb/pull/33).
- Collection core functions - use vendored version of ``distutils.version`` instead of the deprecated Python standard library ``distutils``.
- Include ``simplified_bsd.txt`` license file for module utils.

New Modules
-----------

- cockroachdb_db - Create, modify or delete a CockroachDB database

v0.2.0
======

Release Summary
---------------

This is the minor release of the ``community.cockroachdb`` collection.
This changelog contains all changes to the modules and plugins in this collection
that have been made after the previous release.

New Modules
-----------

- cockroachdb_info - Gather information about CockroachDB servers

v0.1.0
======

Release Summary
---------------

This is the first release of the ``community.cockroachdb`` collection.

New Modules
-----------

- cockroachdb_query - Run queries in a CockroachDB database
