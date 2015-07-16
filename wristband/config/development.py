# config.py

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
PIPELINES = {
    "zone_one": ["dev", "qa-zone_one", "staging-zone_one"],
    "zone_two": ["dev", "qa-zone_two", "staging-zone_two"],
}

RELEASES_URI = "https://releases.tax.service.gov.uk/apps"
