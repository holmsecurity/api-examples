# Holm Security - Qradar app

Version 2.0

## About

The app polls the data about network assets via Holm Security Security Center's REST API and creates an XML file with relevant data. This data can subsequently be processed by QRadar via an AXIS scan.


## Prerequisites

This guide assumes that the Qradar instance up and running.

API access needs to be enables and an API token must be created in Holm Security. The token and base url are used for establishing the integration. Make sure that net-assets endpoint is allowed for read while creating the token.

## Install

- Download the files from this directory
- Set the values in `settings.py`. `API_URL` and `API_TOKEN` are required, other need to be present but can be blank.
- Create a cron job running the script regularily. Usage: `python qradar-axis-assets.py <<output_file>>`

## Use the app

Create an AXIS scanner in QRadar and schedule a scan to poll the created files.

Referrences:
- https://www.ibm.com/docs/en/dsm?topic=guide-scheduling-vulnerability-scan
- https://www.ibm.com/docs/en/dsm?topic=scanner-adding-axis-vulnerability-scan

## TODO

- Support more data on port vulnerabilities

## Copyright

Copyright 2023 - Holm Security AB