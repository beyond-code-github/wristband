First steps
===========

Run the application
-------------------

Wristband needs a few variable environments to be set in order to run properly, a typical running command looks like this:



.. code:: bash

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


.. note::

    SECRET_KEY, PORT, LDAP_URL, LDAP_BASE_DN are set as system wide variable environments in the VM,
    pass them in the previous command to override the default values or if you are working outside of the VM


Login/logut
-----------

Wristband uses a simple client side session to keep track of the authenticated users.

- POST /api/{version}/login - accepts username and password and creates the cookie if the login credentials are correct
- GET /api/{version}/logout - it destroys the session cookie


Health check
------------

- GET /ping/ping