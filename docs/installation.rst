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

- [Install Vagrant](https://docs.vagrantup.com/v2/installation/)
- [Install Ansible](https://docs.ansible.com/ansible/intro_installation.html)
- `$ ansible-galaxy install bennojoy.openldap_server` to install the Ansible LDAP module:
- `$ vagrant up` to spin the VM, provision will apply
- `$ vagrant ssh` to ssh into the VM
- When inside the VM run the app using the command:

PIPELINES='one,two'  \
ENVIRONMENTS='qa-one,qa-two,staging-one,staging-two' \
ENVIRONMENT_qa_one_jenkins_uri=https://wristband:pass@deploy-qa-one.tax.service.gov.uk  \
ENVIRONMENT_qa_two_jenkins_uri=https://deploy-qa-two.tax.service.gov.uk  \
ENVIRONMENT_staging_one_jenkins_uri=https://wristband:pass@deploy-staging-one.tax.service.gov.uk  \
ENVIRONMENT_staging_two_jenkins_uri=https://deploy-staging-two.tax.service.gov.uk  \
PIPELINE_one=qa-one,staging-one \
PIPELINE_two=qa-two,staging-two \
CONFIG_FILE=config/production.py \
python app.py

(SECRET_KEY, PORT, LDAP_URL, LDAP_BASE_DN are set as system wide variable environments, pass them in the previous
command to override the default values)

- Log in the app using admin/password