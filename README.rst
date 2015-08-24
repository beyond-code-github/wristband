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

Settings
------------

Wristband relies extensively on environment settings which **will not work with Apache/mod_wsgi setups**.
It has been deployed successfully with both Gunicorn/Nginx and even uWSGI/Nginx.

For configuration purposes, the following table maps the 'wristband' environment variables to their Django setting:

======================================= =========================== ============================================== ======================================================================
Environment Variable                    Django Setting              Development Default                            Production Default
======================================= =========================== ============================================== ======================================================================
DJANGO_DEBUG                            DEBUG                       True                                           False
DJANGO_SECRET_KEY                       SECRET_KEY                  CHANGEME!!!                                    raises error
DJANGO_SECURE_BROWSER_XSS_FILTER        SECURE_BROWSER_XSS_FILTER   n/a                                            True
DJANGO_SECURE_SSL_REDIRECT              SECURE_SSL_REDIRECT         n/a                                            True
DJANGO_SECURE_CONTENT_TYPE_NOSNIFF      SECURE_CONTENT_TYPE_NOSNIFF n/a                                            True
DJANGO_SECURE_FRAME_DENY                SECURE_FRAME_DENY           n/a                                            True
DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS   HSTS_INCLUDE_SUBDOMAINS     n/a                                            True
DJANGO_SESSION_COOKIE_HTTPONLY          SESSION_COOKIE_HTTPONLY     n/a                                            True
DJANGO_SESSION_COOKIE_SECURE            SESSION_COOKIE_SECURE       n/a                                            False
======================================= =========================== ============================================== ======================================================================


Getting up and running
----------------------

Basics
^^^^^^

The steps below will get you up and running with a local development environment. We assume you have the following installed:

* pip
* virtualenv

First make sure to create and activate a virtualenv_, then open a terminal at the project root and install the requirements for local development::

    $ pip install -r requirements/local.txt


Running
^^^^^^^

     $ manage.py runserver


.. _virtualenv: http://docs.python-guide.org/en/latest/dev/virtualenvs/
