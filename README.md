# wristband

[![Apache-2.0 license](http://img.shields.io/badge/license-Apache-brightgreen.svg)](http://www.apache.org/licenses/LICENSE-2.0.html) [![Build Status](https://travis-ci.org/hmrc/wristband.svg)](https://travis-ci.org/hmrc/wristband) [ ![Download](https://api.bintray.com/packages/hmrc/releases/wristband/images/download.svg) ](https://bintray.com/hmrc/releases/wristband/_latestVersion)

## What is this?

A REST API for the Wristband deployment service.

## What does it do?

It speaks HTTP and JSON and executes actions defined by you. It is designed to work with [wristband-frontend][1], but will work fine without it.

## Installation

Run `setup.py` and then `wristband`.

## Requirements

- Python >= 2.7
- `requirements.txt`
- MongoDB >= 2.6

## API

| Path | Supported Methods | Description |
| ---- | ----------------- | ----------- |
| `/ping/ping` | GET | Healthcheck |

## Contributing

0. Fork this repo
1. Set up test dependencies with `pip install -r requirements-tests.txt`.
2. Write awesome code and tests
3. Open a pull request with your branch

[1]: https://github.tools.tax.service.gov.uk/HMRC/wristband-frontend
