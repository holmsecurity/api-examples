# Holm Security - Qradar app

Version 1.0

## About

The app will pull data about network_assets and classify them based on severity. Sets will be created for different severities and the sets will be then populated with ips in Qradar. The user is able to see the response, if anything goes wrong. It will be shown there.


**Severity levels:**


- Critical
- High
- Medium
- Low
- Info

## Prerequisites

This guide assumes that the Qradar instance up and running. You also need to download Qradar app editor.
You also need to enable the api and create a token in Holm Security. The token and base url are used for establishing the integration. Make sure that net-assets endpoint is allowed for read while creating the token

## Install

- Download and Install Qradar app editor.  
- Upload the app using the .zip

## Use the app

Select use existing apps then upload the zipped app file. For more information, see https://support.holmsecurity.com/hc/en-us/articles/360020403959-How-do-I-integrate-with-IBM-Qradar-

## Troubleshooting 

- Review Chrome dev tools when setting up integration in QRadar web UI to identify calls with errors (such as 500 internal server error)
- Review the App logs on the QRadar instance. How to do this: https://www.ibm.com/support/pages/qradar-review-logs-applications-errors and https://www.ibm.com/docs/en/qradar-common?topic=2-app-logs
- Review App framework versions and any potential incompatibility with newer versions of QRadar: https://www.ibm.com/docs/en/qradar-common?topic=framework-qradar-app-version-2

## TODO

- Regular polling of data (currently ad-hoc only)
- Certified Qradar app

## Copyright

Copyright 2021 - Holm Security AB
