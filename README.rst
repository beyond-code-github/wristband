Wristband
=========

.. image:: http://img.shields.io/badge/license-Apache-brightgreen.svg
    :target: http://www.apache.org/licenses/LICENSE-2.0.html
    :alt: Apache-2.0 license

.. image:: https://travis-ci.org/hmrc/wristband.svg?branch=master
    :target: https://travis-ci.org/hmrc/wristband
    :alt: Build status

.. image:: http://codecov.io/github/hmrc/wristband/coverage.svg?branch=master
    :target: http://codecov.io/github/hmrc/wristband?branch=master
    :alt: Code coverage

.. image:: https://readthedocs.org/projects/wristband/badge/?version=latest
    :target: https://readthedocs.org/projects/wristband/?badge=latest
    :alt: Documentation Status

A REST API for the Wristband deployment service.

It speaks HTTP and JSON and executes actions defined by you. It is designed to work with `wristband-frontend <https://github.com/hmrc/wristband-frontend>`_, but will work fine without it.


Getting up and running
----------------------

Basics
^^^^^^

The steps below will get you up and running with a local development environment. We assume you have the following installed:

* pip
* virtualenv

First make sure to create and activate a virtualenv_, then open a terminal at the project root and install the requirements for local development::

    $ pip install -r requirements/local.txt


Alternatively you can also use Vagrant and Ansible to get an up and running. We assume you have the following installed:

 * Vagrant
 * Ansible

Install Ansible roles:

    $ ansible-galaxy install -r requirements.yml

Then provision and spin up the Vagrant VM:

    $ vagrant up


Settings
^^^^^^^^

Wristband relies extensively on environment settings which **will not work with Apache/mod_wsgi setups**.
It has been deployed successfully with both Gunicorn/Nginx and even uWSGI/Nginx.

For configuration purposes, the following table maps the 'wristband' environment variables to their Django setting:

===================================== =========================== =================== ==================
Environment Variable                  Django Setting              Development Default Production Default
===================================== =========================== =================== ==================
DJANGO_DEBUG                          DEBUG                       True                False
DJANGO_SECRET_KEY                     SECRET_KEY                  CHANGEME!!!         raises error
DJANGO_SECURE_BROWSER_XSS_FILTER      SECURE_BROWSER_XSS_FILTER   n/a                 True
DJANGO_SECURE_CONTENT_TYPE_NOSNIFF    SECURE_CONTENT_TYPE_NOSNIFF n/a                 True
DJANGO_SECURE_FRAME_DENY              SECURE_FRAME_DENY           n/a                 True
DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS HSTS_INCLUDE_SUBDOMAINS     n/a                 True
DJANGO_SESSION_COOKIE_HTTPONLY        SESSION_COOKIE_HTTPONLY     n/a                 True
DJANGO_SESSION_COOKIE_SECURE          SESSION_COOKIE_SECURE       n/a                 False
MONGO_DB_NAME
===================================== =========================== =================== ==================

App specific environment variables


===================================== ===================================== ======================================== ==================
Environment Variable                  Django Setting                        Development Default                      Production Default
===================================== ===================================== ======================================== ==================
STAGES                                STAGES                                qa,staging                               qa,staging
WEBSTORE_URL                          WEBSTORE_URL                          raises error                             raises error
WRISTBAND_ENV                         WRISTBAND_ENV                         local                                    prod
KIBANA_URL                            KIBANA_URL                            https://{stage}-{security_zone}.test.com raises error
AUTH_LDAP_SERVER_URI                  AUTH_LDAP_SERVER_URI                  ldaps://localhost                        raises error
AUTH_LDAP_BIND_AS_AUTHENTICATING_USER AUTH_LDAP_BIND_AS_AUTHENTICATING_USER True                                     raises error
AUTH_LDAP_USER_SEARCH_DN              AUTH_LDAP_USER_SEARCH_DN              ou=users,dc=example,dc=com               raises error
AUTH_LDAP_GROUP_SEARCH_DN             AUTH_LDAP_GROUP_SEARCH_DN             ou=groups,dc=example,dc=com              raises error
AUTH_LDAP_SUPERUSER_DN                AUTH_LDAP_SUPERUSER_DN                cn=planets,ou=groups,dc=example,dc=com   raises error
DJANGO_LOG_LEVEL                      LOG_LEVEL                             DEBUG                                    raises error
===================================== ===================================== ======================================== ==================



Prepare a config file for the Docktor provider (currently the only Service Provider that can do deployments). Put a
file called `providers.yaml` in the `wristband/providers` directory containing information for the Docktor service in
the environment you are deploying to. A sample file is provided.

To finish preparation, run

    $ manage.py import_apps

Running
^^^^^^^

The VM contains two mock instances of Docktor, they need to be running.

     $ run_docktor

Then run wristband

     $ run_wristband


Authentication
^^^^^^^^^^^^^^

Wristband is capable of authenticating users in two different ways: token and session.

Token authentication should be used in the client-server scenario:

1. POST username and password to /api/token/ to get a new token
2. Include the token in the Authorization HTTP header. The key should be prefixed by the string literal "Token", with whitespace separating the two strings.

Session authentication should be used in the browser scenario:

1. POST username and password to /login/

If using the ldap server in the VM the login credentials are: mars/password
The user mars belongs to the planets group.

LDAPS is exposed to the host machine on port 1636

.. _virtualenv: http://docs.python-guide.org/en/latest/dev/virtualenvs/
