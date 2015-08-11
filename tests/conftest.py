import pytest

from app import create_app


@pytest.fixture(scope='session')
def app():
    """
    Testing app with testing flag set to True and testing configs pre-loaded
    """
    app = create_app()
    app.testing = True
    app.config.update(dict(
        ENVIRONMENTS={
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
        },
        PIPELINES={
            "zone_one": ["dev", "qa-zone_one", "staging-zone_one"],
            "zone_two": ["dev", "qa-zone_two", "staging-zone_two"],
        },

        RELEASES_URI="https://releases.tax.service.gov.uk/apps",

        LDAP={
            'url': 'ldap://test',
            'user_dn': 'uid={username},dc=example,dc=com',
            'base_dn': 'dc=example,dc=com'
        }
    ))
    return app

