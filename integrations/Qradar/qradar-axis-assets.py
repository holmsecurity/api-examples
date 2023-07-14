#!/usr/bin/env python
import sys
from datetime import datetime
from xml.dom import minidom

import requests

from settings import API_TOKEN, API_URL, SCANNER_IP, SCANNER_NAME, SCANNER_USER


def create_host_element(root, host_data):
    host = root.createElement("host")

    ip = root.createElement("ip")
    ip.setAttribute("type", "IPv4")
    ip.setAttribute("value", host_data["ip"])
    host.appendChild(ip)

    name = root.createElement("hostName")
    name.appendChild(root.createTextNode(host_data["hostname"]))
    host.appendChild(name)

    last_seen = root.createElement("lastSeen")
    last_seen.appendChild(root.createTextNode(host_data["last_detected"] or ""))
    host.appendChild(last_seen)

    return host


def create_host_elements(root):
    request_url = (
        API_URL + "net-assets?type=host&limit=100&last_detected_from=2000-01-01"
    )
    while request_url:
        try:
            response = requests.request(
                "GET",
                url=request_url,
                headers={
                    "Authorization": f"Token {API_TOKEN}",
                    "Content-Type": "application/json",
                },
                verify=False,
            )
        except Exception as e:
            print(f"Failed to establish integration due to {e}")
            exit()

        data = response.json()
        for host in data["results"]:
            if not host["last_detected"]:
                continue
            yield create_host_element(root, host)

        request_url = data["next"]


def create_scanner_element(root):
    scanner = root.createElement("identifyingScanner")

    ip = root.createElement("scannerIp")
    ip.setAttribute("type", "IPv4")
    ip.setAttribute("value", SCANNER_IP)
    scanner.appendChild(ip)

    name = root.createElement("scannerName")
    name.appendChild(root.createTextNode(SCANNER_NAME))
    scanner.appendChild(name)

    vendor = root.createElement("scannerVendor")
    vendor.appendChild(root.createTextNode("Holm Security"))
    scanner.appendChild(vendor)

    user = root.createElement("scannerUser")
    user.appendChild(root.createTextNode(SCANNER_USER))
    scanner.appendChild(user)

    current_time = datetime.utcnow()
    export_time = root.createElement("scannerExportTime")
    export_time.appendChild(
        root.createTextNode(current_time.strftime("%Y-%m-%dT%H:%M:%SZ"))
    )
    scanner.appendChild(export_time)

    return scanner


def create_export_file(output_file):
    root = minidom.Document()

    scan_report = root.createElement("scanReport")
    root.appendChild(scan_report)

    scanner = create_scanner_element(root)
    scan_report.appendChild(scanner)

    hosts = create_host_elements(root)
    for host in hosts:
        scan_report.appendChild(host)

    xml_str = root.toprettyxml(indent="\t", encoding="utf-8")
    with open(output_file, "wb") as f:
        f.write(xml_str)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: qradar-axis-assets.py output_file")
        exit()

    create_export_file(sys.argv[1])
    print("Export completed")
