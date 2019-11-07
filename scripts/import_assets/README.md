# Importing assets


## Description 
Post request for assets creation by attaching CSV files stored locally. 
## prerequisites
* python3

## Inputs arguments
To use this code, the following inputs are requierd; 
* CSV file containg the assets in the following format:

```
name, type, business impact, details, tags, hosts personal data, ip/ip range
```
For instance: 


```
test_one,neutral,description of the scan,28229346-c605-4944-a0c7-820d7d80a9cc|7e03a282-0061-472f-b106-10b7edc7d634,false,192.164.5.1
test_two,neutral,description of the scan,7e03a282-0061-472f-b106-10b7edc7d634,true,192.169.5.1
test_three,neutral,description of the scan,186e0a25-e28b-4ecf-b9ad-223c8ee2a62d,false,192.170.5.1/24


```
* Token which gives access to the API endpoint. (mandatory)
* Path to the csv file. (mandatory)
* URL to the end point (https://se-api.holmsecurity.com/v1/ by default). (optional)
* There are three statics tags to choose from: 
    * Operating systems: 28229346-c605-4944-a0c7-820d7d80a9cc
    * Services: 7e03a282-0061-472f-b106-10b7edc7d634
    * TCP/IP ports & protocols: 186e0a25-e28b-4ecf-b9ad-223c8ee2a62d
* There are four business impact types to choose from:
    * neutral
    * low 
    * medium 
    * high
## To run the code 

```
$ python3 main.py -p file.csv -k xxxxxxxxxx -u your_url
```


##  output
Assets created.
