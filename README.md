# wristband

[![Apache-2.0 license](http://img.shields.io/badge/license-Apache-brightgreen.svg)](http://www.apache.org/licenses/LICENSE-2.0.html) [![Build Status](https://travis-ci.org/hmrc/wristband.svg)](https://travis-ci.org/hmrc/wristband) [ ![Download](https://api.bintray.com/packages/hmrc/releases/wristband/images/download.svg) ](https://bintray.com/hmrc/releases/wristband/_latestVersion)
[![Coverage Status](https://coveralls.io/repos/hmrc/wristband/badge.svg?branch=master&service=github)](https://coveralls.io/github/hmrc/wristband?branch=master)

## What is this?

A REST API for the Wristband deployment service.

## What does it do?

It speaks HTTP and JSON and executes actions defined by you. It is designed to work with [wristband-frontend][1], but will work fine without it.

## Installation

### Virtualenv
To run wristband;

$ virtualenv env
$ source env/bin/activate
$ pip install -r requirements.txt

For tests run this in addition to the ones above;
pip install -r requirements-tests.txt

### Vagrant 

- [Install Vagrant](https://docs.vagrantup.com/v2/installation/)
- [Install Ansible](https://docs.ansible.com/ansible/intro_installation.html)
- `$ vagrant up` to spin the VM, provision will apply
- `$ vagrant ssh` to ssh into the VM
- Run the app using the command:

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

- Log in using admin/password

## Requirements

- Python 2.7
- `requirements.txt`

## API

| Path | Supported Methods | Description |
| ---- | ----------------- | ----------- |
| `/ping/ping` | GET | Healthcheck |

## Running wristband

PIPELINES='one,two'  \
ENVIRONMENTS='qa-one,qa-two,staging-one,staging-two' \
ENVIRONMENT_qa_one_jenkins_uri=https://wristband:pass@deploy-qa-one.tax.service.gov.uk  \
ENVIRONMENT_qa_two_jenkins_uri=https://deploy-qa-two.tax.service.gov.uk  \
ENVIRONMENT_staging_one_jenkins_uri=https://wristband:pass@deploy-staging-one.tax.service.gov.uk  \
ENVIRONMENT_staging_two_jenkins_uri=https://deploy-staging-two.tax.service.gov.uk  \
PIPELINE_one=qa-one,staging-one \
PIPELINE_two=qa-two,staging-two \
LDAP_URL=ldap://ldap_url.com \
LDAP_BASE_DN=dc=example,dc=com \
CONFIG_FILE=config/production.py \
SECRET_KEY=your_secret_key \
python app.py

## Contributing

- Fork this repo
- Open a pull request with your branch

[1]: https://github.tools.tax.service.gov.uk/HMRC/wristband-frontend


TODO
--
* Validate environment options
