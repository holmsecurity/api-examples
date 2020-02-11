# Holm Security - Splunk app

Version 1.0

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
