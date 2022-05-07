#!/usr/bin/env python3

import requests
import uuid
import pprint


def clear():
    sorted_ip_list = {}
    ip_list = None


# Lists all Azure regions and prints the list when called
def get_azure_endpoints():
    """
    Get Azure Datacenter endpoints IP addresses
    """
    clear()
    azure_response = requests.post(
        "https://azuredcip.azurewebsites.net/getazuredcipranges",
        json={"request": "dcip", "region": "all"},
    )
    sorted_ip_list = azure_response.json()
    print(sorted_ip_list)



# Lists all office365 object
def get_o365_endpoints_json():
    sorted_ip_list = {}
    request_id = uuid.uuid4()
    '''
    Get Office 365 endpoints IP addresses
    '''
    clear()
    office_response = requests.get(
        "https://endpoints.office.com/endpoints/worldwide?clientrequestid={}".format(request_id))
    object_list = office_response.json()
    pprint.pprint(object_list)

# Lists all office365 endpoint IPs and prints in a pretty json format
def get_o365_endpoints_ips():
    sorted_ip_list = {}
    request_id = uuid.uuid4()
    '''
    Get Office 365 endpoints IP addresses
    '''
    clear()
    office_response = requests.get(
        "https://endpoints.office.com/endpoints/worldwide?clientrequestid={}".format(request_id))
    ip_list = office_response.json()
    pprint.pprint(ip_list)

# Lists all office365 endpoint urls and prints in a pretty json format
def get_o365_endpoints_urls():
    sorted_ip_list = {}
    request_id = uuid.uuid4()
    '''
    Get Office 365 endpoints IP addresses
    '''
    clear()
    office_response = requests.get(
        "https://endpoints.office.com/endpoints/worldwide?clientrequestid={}".format(request_id))
    urls_list = office_response.json()
    for item in urls_list:
        if item.get("ips") is not None:
            urls_list = item["urls"]
    pprint.pprint(urls_list)


get_o365_endpoints_json()
