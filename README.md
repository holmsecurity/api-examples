# API-examples
This repository shows API examples for Holm Security's REST API.

The REST API endpoint and documentation can be found in your Security Center account.
The endpoint will vary depending on in which data-center your Security Center account is hosted.

Since this API is JSON based, we will use the [httpie](https://httpie.org/) tool to make requests.

Note: In this example we are using the Sweden, Stockholm data-center as REST API endpoint.


## Get Network assets
Those are targets of your scan. List them as follows:
```
$  http https://se-api.holmsecurity.com/v2/net-assets "Authorization:Token {token}"
HTTP/1.1 200 OK

{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "created": "2019-04-23T14:39:31Z",
            "last_detected": null,
            "name": "Test server",
            "operating_system": null,
            "tags": [],
            "times_detected": 0,
            "type": "host",
            "uuid": "1237a6c5-4b8d-45a8-8d57-687d8ce76aab",
            "vulnerabilities_count": 0
        }
    ]
}
```

Where `{token}` is API token generated in your Security Center account.

## Get Network scan profiles
Configuration of the scan:
```
$  http https://se-api.holmsecurity.com/v2/net-scans/scan-profiles "Authorization:Token {token}"
HTTP/1.1 200 OK

[
    {
        "created": "2019-04-23T14:42:50Z",
        "details": "Will be used for all scans now",
        "name": "Test scan profile",
        "scan_type": "network",
        "uuid": "d1ef4f56-3fb9-4a34-b197-bb59041a98fa"
    }
]

```

## Start a scan
### Network scan
The [network_scan.json](examples/network_scan.json) contains an example payload that will initiate a simple Network scan using an asset and scan profile that was listed above.

```
$  http POST https://se-api.holmsecurity.com/v2/net-scans "Authorization:Token {token}" @examples/network_scan.json
HTTP/1.1 201 Created

{
    "uuid": "0c045b34-e053-4063-af93-1ebc2c754bca"
}
```

### Web App scan
The Web scan requires similar payload with two differences:
- Instead of array of `included_assets`, we send `webapp_asset_uuid`, which is the target for the Web application scan. The list of available assets can be accessed [here](https://se-api.holmsecurity.com/docs/#operation/web-scans_assets_list)
- we use different (Web specific) [scan profile](https://se-api.holmsecurity.com/docs/#operation/web-scans_scan-profiles_list)

[webapp_scan.json](examples/webapp_scan.json)
```
$  http POST https://se-api.holmsecurity.com/v1/web-scans "Authorization:Token {token}" @examples/webapp_scan.json
HTTP/1.1 201 Created

{
    "uuid": "bc62e282-828d-49bc-8c43-9b717e85b9ee"
}
```

### API example file

An [example file](https://github.com/holmsecurity/api-examples/blob/master/get_scan_results.py) has been composed which servers to exemplify how the API can be used.

The following external python libraries are used in the example file:

| Library  | Usage |
| ------------- | ------------- |
| datetime  | to get datetime object |
| requests | to make http requests    |
| pprint | simply to print prettier  |
| dateutil | to parse datetime objects |
| pytz | to get the right string formatting |
| requests.exceptions import MissingSchema | to raise the right exception |
| argparse | to parse arguments from STDIN |



 The example script is used simply by running the python code with python3 interpreter and takes input arguments from CLI.
 The output will be printed to STDOUT. There are two different scans that can be run using the example script with flag "--type" or "-tp"

In order to alter the script to output JSON instead of printing to STDOUT simply change the return statements to return the objects {scans} and {scan_results) instead of printing them,

The following are examples of how to run the api-examples.py:

 
 `$ python3 get_scan_results -t 256 -l 200 -tp net_scan`
 
 Returns all network scans from the last 256 hour period, limit the number of scans to 200.
 For example output see:
 [output network scan](https://github.com/holmsecurity/api-examples/blob/master/examples/network_scan_results.json)
 
  `$ python3 get_scan_results -t 128 -l 100 -tp net_scan -s "high, critical"`
  
Returns all network scans from the last 128 hour period, limit the number of scans to 100 and filter scan results by severity high and/or critical.
For example output see:
[output webapp scan](https://github.com/holmsecurity/api-examples/blob/master/examples/webapp_scan_results.json)

Full help docs for the api-examples:

```
python3 get_scan_results.py -help                                                    
usage: get_scan_results.py [-h] [--api API] [--time TIME] [--limit LIMIT]
                           [--type TYPE] [--severity SEVERITY]
                           key

positional arguments:
  key                   API key to be used

optional arguments:
  -h, --help            show this help message and exit
  --api API, -a API     API URL to use, default https://se-
                        api.holmsecurity.com/v1
  --time TIME, -t TIME  Timeperiod to grab scan results from: Specified in
                        hours e.g 24, 48 or 768 (default: 24)
  --limit LIMIT, -l LIMIT
                        result limit, eg. maximum number of scans to return.
                        (default: 10)
  --type TYPE, -tp TYPE
                        scan type to run, eg. net_scan or web_scan, default
                        net_scan
  --severity SEVERITY, -s SEVERITY
                        severity level for filtering scan result
                        vulnerabilities. For multiple severities please
                        provide a list as such: 'high, medium' !Note the
                        space!(default: 'high')


```

