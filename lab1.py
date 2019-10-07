import requests
import time
import queue
import concurrent.futures
import os
from functools import reduce
import operator
import json
import yaml
import csv
from xmljson import Parker
from xml.etree.ElementTree import fromstring
from collections import OrderedDict

#define a counter 
counter = 2
def find_value(key_name,*value_name):
    i = 0
    for el in json_data:
        i += 1
        print(i)
        if "36-0066196" in el:
            new_element = el[:-3]
            new_element += "]"
            el = new_element
        loader = json.loads(el)
        if "record" in loader: 
            print("XML")
            xml_element = str(el)
            xml_element = xml_element[:-1]
            xml_element = xml_element[11:]
            el = xml_element
            loader = json.loads(el)

        for new_el in loader:
            for key,value in new_el.items():
                if key == key_name and value == value_name:
                    print("Key:", key, " Value:", value)
                    print(new_el)
                elif key == key_name:
                    print("Key:", key, " Value:", value)
                    print(new_el)
                  

def xml_to_json(data):
    pk = Parker(dict_type=OrderedDict)
    converted_json = json.dumps(pk.data(fromstring(data)))
    return converted_json
def csv_to_json(data):
    with open("file.csv","w") as f:
        f.write(data)

    csv_file = open('file.csv', 'r')

    reader_csv = csv.DictReader(csv_file)
    out = json.dumps( [ row for row in reader_csv ] )
    return out
def yaml_to_json(data):
    out = json.dumps(yaml.safe_load(data))
    return out

def getRequest(route, header):
    name = requests.request("GET", url + route, headers=header)
    global counter
    counter += 1
    getRoute(name)
    makeFile(name)
    
def getRoute(res_name):
    route_text = res_name.text
    data = json.loads(route_text)
    if 'link' in data:
        link = data["link"]
        for key, value in link.items():
            routes.put(value)
            new_routes_list.append(value)
    else:
        print("No more routes")
    return routes


def makeFile(file_text):
    file_json = file_text.text
    data = json.loads(file_json)
    if 'data' in data:
        all_data = data["data"]
        if 'mime_type' in data:
            type = data["mime_type"]
            if(type == "application/xml"):
                json_result = xml_to_json(all_data)
            elif(type == "text/csv"):
                json_result = csv_to_json(all_data)
            elif(type == "application/x-yaml"):
                json_result = yaml_to_json(all_data)
        else:
            json_result = all_data
        json_element = {}
        json_element = json_result
        json_data.append(json_element)
    else:
        print("No link-data in file")

start = time.time()
new_routes_list = []
json_data = []
url = "http://localhost:5000"


routes = queue.Queue(maxsize=20)

with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
    # register
    res_register = requests.request("GET", url + "/register")
    # get access_token from json response
    json_register = res_register.text
    data = json.loads(json_register)
    x_access_token = data["access_token"]
    link = data["link"]
    header = {
        'X-Access-Token': x_access_token
    }

    # home route
    getRequest(link, header)

    for route in iter(routes.get, None):
        executor.submit(getRequest, route, header)
        if(routes.empty()):
            if counter == len(new_routes_list):
                break

os.remove("file.csv")
end = time.time()
print(f"Done in {end - start}")

find_value("employee_id")
