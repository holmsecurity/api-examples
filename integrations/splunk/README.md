# Holm Security - Splunk app

Version 1.0

## About

This Splunk App let's you lookup the number of vulnerabilities per severity for a network asset using its IP (IPv4/IPv6) directly inside of Splunk. The lookup is done against Holm Security VMP using its REST API to retrieve information about the asset.
The app works both for SaaS and On-Premise installations from Holm Security.

**Example use case:**

To get more context about an network asset and understand what the security risk is on it. Use the search lookup command to get enhanced information about it using this app that integrates with Holme Security. 


**Severity levels:**


- Critical
- High
- Medium
- Low
- Info

## Prerequisites

This guide assumes that the splunk app package (tar.gz) is available for you and that you have access to install apps on your Splunk instance as well as editing the files provisioned by the Splunk app inside of the apps directory.

## Install

Login to splunk and install the new app using the tar.gz file

## Configure

**Edit app config**
To configure the app you will need to edit the app config inside the bin/holm.py of the app.

- Splunk\etc\apps\holm-security\bin
- open for edit: holm.py
- Replace xyz with your API TOKEN
- Replace ABC with your API HOST + PORT
- Save holm.py

## Use the app

In the search field: | holm asset_ip=x.x.x.x

## Limitations

- There is a UI for configuring the app but it is not functional. Configure the app using the described steps above.

## TODO

- Configuration supported through the Splunk UI
- Make it a certified Splunk app

Copyright 2020 - Holm Security AB
