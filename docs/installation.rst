Installation
============

.. tip::
    Vagrant is the recommended method

Virtualenv
----------

.. code:: bash

    $ virtualenv env
    $ source env/bin/activate
    $ pip install -r requirements/local.txt

Vagrant
-------

- `Install Vagrant <https://docs.vagrantup.com/v2/installation/>`_
- `Install Ansible <https://docs.ansible.com/ansible/intro_installation.html>`_
- `$ ansible-galaxy install bennojoy.openldap_server` to install the Ansible LDAP module:
- `$ vagrant up` to spin the VM, provision will apply
