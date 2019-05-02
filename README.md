# API-examples
This repository shows API examples for Holm Security's REST API.

The REST API endpoint and documentation can be found in your Security Center account.
The endpoint will vary depending on in which data-center your Security Center account is hosted.

Since this API is JSON based, we will use the [httpie](https://httpie.org/) tool to make requests.

Note: In this example we are using the Sweden, Stockholm data-center as REST API endpoint.


## Get Network assets
Those are targets of your scan. List them as follows:
```
$  http https://se-api.holmsecurity.com/v1/net-scans/assets "Authorization:Token {token}"
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
$  http https://se-api.holmsecurity.com/v1/net-scans/scan-profiles "Authorization:Token {token}"
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
$  http POST https://se-api.holmsecurity.com/v1/net-scans "Authorization:Token {token}" @examples/network_scan.json
HTTP/1.1 201 Created

{
    "uuid": "0c045b34-e053-4063-af93-1ebc2c754bca"
}
```

### Web App scan
The Web scan requires similar payload with two differences:
- Instead of array of `included_assets`, we send `webapp_asset_uuid`, which is the target for the Web application scan. The list of available assets can be accessed [here](https://se-api.holmsecurity.com/docs/#operation/web-scans_assets_list)
- we use different (Web specific) [scan profile](https://se-api.holmsecurity.com/docs/#operation/web-scans_scan-profiles_list)

[webapp_scan.json](examples/webapp_scan.json])
```
$  http POST https://se-api.holmsecurity.com/v1/web-scans "Authorization:Token {token}" @examples/webapp_scan.json
HTTP/1.1 201 Created

{
    "uuid": "bc62e282-828d-49bc-8c43-9b717e85b9ee"
}
```
