import requests
import time
import json
import threading
import concurrent.futures
import yaml
import os
from xmljson import Abdera
from xml.etree.ElementTree import fromstring
from collections import OrderedDict

#define a counter 
counter = 2

def xml_to_json(data):
    ab = Abdera(dict_type=OrderedDict)
    converted_json = json.dumps(ab.data(fromstring(data)))
    return converted_json
def csv_to_json(data):
    f = open("file.csv","w")
    f.write(data)
    f.close()


def getRequest(route, header):
    name = requests.request("GET", url + route, headers=header)

    return name


def getRoute(res_name, route_name):
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

            route_name.append(value)
    else:
        print("no more links")

    return route_name


def makeFile(file_text, file_name):
    f = open(file_name, "w")
    f.write(file_text.text)
    f.close()


start = time.time()

url = "http://localhost:5000"
routes = []

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
res_home = getRequest(link, header)
getRoute(res_home, routes)
# all routes
route1 = []
route2 = []
route3 = []
route4 = []
route1.append(routes.pop(0))
route2.append(routes.pop(0))
route3.append(routes.pop(0))
route4.append(routes.pop(0))


def all_routes(route_list):
    for route in route_list:
        new_route = getRequest(route, header)
        makeFile(new_route, route.replace("/", ""))
        getRoute(new_route, route_list)

f = open("file.json","a")
f.write("]")
f.close()
