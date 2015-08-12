Concepts
========

Wristband relies on Pipelines and Environments.
The relevant Python data structures are built from the environments variables passed into the config factory functions.


Pipelines
---------

Pipelines represent the *direction* of the promotion in the different zones.

.. code:: python

    PIPELINES = {
        "zone_one": ["dev", "qa-zone_one", "staging-zone_one"],
        "zone_two": ["dev", "qa-zone_two", "staging-zone_two"],
    }



Environments
------------

.. code:: python

    ENVIRONMENTS = {
        "qa-zone_one": {
            "jenkins_uri": "https://deploy-qa-zone_one.tax.service.gov.uk"
        },
        "qa-zone_two": {
            "jenkins_uri": "https://deploy-qa-zone_two.tax.service.gov.uk"
        },
        "staging-zone_one": {
            "jenkins_uri": "https://deploy-staging-zone_one.tax.service.gov.uk"
        },
        "staging-zone_two": {
            "jenkins_uri": "https://deploy-staging-zone_two.tax.service.gov.uk"
        },
    }