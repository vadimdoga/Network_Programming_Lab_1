import requests
import time
from time import sleep
import json
import csv
import threading
import queue
import concurrent.futures
import yaml
import os
from xmljson import Abdera
from xml.etree.ElementTree import fromstring
from collections import OrderedDict

#declare counter
counter = 2

def xml_to_json(data):
    ab = Abdera(dict_type=OrderedDict)
    converted_json = json.dumps(ab.data(fromstring(data)))
    return converted_json
def csv_to_json(data):
    f = open("file.csv","w")
    f.write(data)
    f.close()

    csv_file = open('file.csv', 'r')
    reader_csv = csv.DictReader( csv_file)
    out = json.dumps( [ row for row in reader_csv ] )
    return out
def yaml_to_json(data):
    out = json.dumps(yaml.load(data))
    return out

def getRequest(route, header):
    name = requests.request("GET", url + route, headers=header)
    global counter
    counter += 1
    makeFile(name)
    getRoute(name)
    
def getRoute(res_name):
    route_text = res_name.text
    data = json.loads(route_text)
    if 'link' in data:
        link = data["link"]
        for key, value in link.items():
            routes.put(value)
            new_routes_list.append(value)
    else:
        print("No more links in " + res_name)
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

        f = open("file.json", "a")
        f.write(json_result + ",")
        f.write(os.linesep)
        f.close()
    else:
        print("No data in file")

f = open("file.json","w")
f.write("[")
f.close()

start = time.time()
new_routes_list = []
url = "http://localhost:5000"
routes = queue.Queue(maxsize=20)

with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
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

    
end = time.time()
print(f"Done in {end - start}")

os.remove("file.csv")

f = open("file.json","a")
f.write("]")
f.close()