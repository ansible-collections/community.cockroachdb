# CockroachDB collection for Ansible

[![Plugins CI](https://github.com/ansible-collections/community.cockroachdb/workflows/Plugins%20CI/badge.svg?event=push)](https://github.com/ansible-collections/community.cockroachdb/actions?query=workflow%3A"Plugins+CI") [![Codecov](https://img.shields.io/codecov/c/github/ansible-collections/community.cockroachdb)](https://codecov.io/gh/ansible-collections/community.cockroachdb)

## Code of Conduct

We follow the [Ansible Code of Conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html) in all our interactions within this project.

If you encounter abusive behavior violating the [Ansible Code of Conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html), please refer to the [policy violations](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html#policy-violations) section of the Code of Conduct for information on how to raise a complaint.

## Contributing

The content of this collection is made by [people](https://github.com/ansible-collections/community.cockroachdb/blob/main/CONTRIBUTORS) just like you, a community of individuals collaborating on making the world better through developing automation software.

We are actively accepting new contributors.

Any kind of contribution is very welcome.

You don't know how to start? Refer to our [contribution guide](https://github.com/ansible-collections/community.cockroachdb/blob/main/CONTRIBUTING.md)!

## Collection maintenance

The current maintainers (contributors with `write` or higher access) are listed in the [MAINTAINERS](https://github.com/ansible-collections/community.cockroachdb/blob/main/MAINTAINERS) file. If you have questions or need help, feel free to mention them in the proposals.

To learn how to maintain / become a maintainer of this collection, refer to the [Maintainer guidelines](https://github.com/ansible-collections/community.cockroachdb/blob/main/MAINTAINING.md).

It is necessary for maintainers of this collection to be subscribed to:

* The collection itself (the `Watch` button -> `All Activity` in the upper right corner of the repository's homepage).
* The "Changes Impacting Collection Contributors and Maintainers" [issue](https://github.com/ansible-collections/overview/issues/45).

They also should be subscribed to Ansible's [The Bullhorn newsletter](https://docs.ansible.com/ansible/devel/community/communication.html#the-bullhorn).

## Communication

We announce releases and important changes through Ansible's [The Bullhorn newsletter](https://eepurl.com/gZmiEP). Be sure you are subscribed.

Join us in the `#ansible` (general use questions and support), `#ansible-community` (community and collection development questions), and other [IRC channels](https://docs.ansible.com/ansible/devel/community/communication.html#irc-channels) on [Libera.Chat](https://libera.chat).

We take part in the global quarterly [Ansible Contributor Summit](https://github.com/ansible/community/wiki/Contributor-Summit) virtually or in-person. Track [The Bullhorn newsletter](https://eepurl.com/gZmiEP) and join us.

For more information about communication, refer to the [Ansible Communication guide](https://docs.ansible.com/ansible/devel/community/communication.html).

## Governance

The process of decision making in this collection is based on discussing and finding consensus among participants.

Every voice is important and every idea is valuable. If you have something on your mind, create an issue or dedicated discussion and let's discuss it!

## Included content

**Modules**:

- cockroachdb_info: Gather information about CockroachDB servers.
- cockroachdb_query: Run queries in a CockroachDB database.

## Tested with ansible-core

- 2.14 and Python 3.8
- devel and Python 3.8

## External requirements

- psycopg2 connector installed on a target machine.

## Using this collection

### Installing the Collection from Ansible Galaxy

Before using the CockroachDB collection, you need to install it with the Ansible Galaxy CLI:

```bash
ansible-galaxy collection install community.cockroachdb
```

You can also include it in a `requirements.yml` file and install it via `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: community.cockroachdb
```

Note that if you install the collection from Ansible Galaxy, it will not be upgraded automatically if you upgrade the Ansible package. To upgrade the collection to the latest available version, run the following command:

```bash
ansible-galaxy collection install community.cockroachdb --upgrade
```

You can also install a specific version of the collection, for example, if you need to downgrade when something is broken in the latest version (please report an issue in this repository). Use the following syntax:

```bash
ansible-galaxy collection install community.cockroachdb:==0.1.0
```

See [Ansible Using collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html) for more details.

### Usage example

```yaml
- name: Gather server info
  community.cockroachdb.cockroachdb_info:
    ssl_mode: verify-full
    ssl_root_cert: /tmp/certs/ca.crt
    ssl_cert: /tmp/certs/client.root.crt
    ssl_key: /tmp/certs/client.root.key
  register: srv_info

- name: Print information returned from the previous task
  ansible.builtin.debug:
    var: srv_info
    verbosity: 2

- name: Run a query with condition
  community.cockroachdb.cockroachdb_query:
    ssl_mode: verify-full
    ssl_root_cert: /tmp/certs/ca.crt
    ssl_cert: /tmp/certs/client.root.crt
    ssl_key: /tmp/certs/client.root.key
    query: 'CREATE DATABASE root'
  when: srv_info.version.year > 20 and srv_info.version.release > 1
```

## Licensing

<!-- Include the appropriate license information here and a pointer to the full licensing details. If the collection contains modules migrated from the ansible/ansible repo, you must use the same license that existed in the ansible/ansible repo. See the GNU license example below. -->

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.
