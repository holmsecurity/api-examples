# Updating assets 

## Description 
The motive is to make it easier for the customer to update their existing assets. There are two codes in the project: 
* get_assets.py; gets the list of existing assets and creates a csv file named assets.csv in the directory.
* update_assets.py: takes the modified CSV file and send a request for update. 

## Prerequisites
* python3
* requests library

## Inputs arguments
To use this script, the following inputs are requierd; 
* Token which gives access to the API endpoint. (mandatory for both codes)
* Path to the csv file. (mandatory for update_assets.py)

## assets.csv format
```
name, uuid, type, tags uuid, ip/ip_range
```

For instance: 

```
test,22c5e448-0fa0-45de-bf68-396e85c365bb,host,28229346-c605-4944-a0c7-820d7d80a9cc,192.141.24.2
```
* URL to the end point (https://se-api.holmsecurity.com/v2/ by default). (optional)

## What to edit?
* Tags uuids are editable, however one can choose among the static tags, some of them could for instance be: 
    * Operating systems: 28229346-c605-4944-a0c7-820d7d80a9cc
    * Services: 7e03a282-0061-472f-b106-10b7edc7d634
    * TCP/IP ports & protocols: 186e0a25-e28b-4ecf-b9ad-223c8ee2a62d
* The name is editable.
* Ip/ip_range is editable.

## To run the script
### Step 1

```
$ python3 get_assets.py -k xxxxxxxxxx 
```
### Step 2 
`
Edit the assets.csv file in any editor and SAVE the changes.
`
### Step 3 
```
$ python3 update_assets.py -k xxxxxxxxxx -p your_path
```

##  output
Updated assets
