import requests
import json
import yaml
import csv
import queue
from xmljson import Parker
from xml.etree.ElementTree import fromstring
from collections import OrderedDict

new_routes_list = []
json_data = []
url = "http://localhost:5000"
counter = 2
routes = queue.Queue(maxsize=20)


def xml_to_json(data):
    pk = Parker(dict_type=OrderedDict)
    converted_json = json.dumps(pk.data(fromstring(data)))
    return converted_json


def csv_to_json(data):
    with open("file.csv", "w") as f:
        f.write(data)

    csv_file = open('file.csv', 'r')

    reader_csv = csv.DictReader(csv_file)
    out = json.dumps([row for row in reader_csv])
    return out


def yaml_to_json(data):
    out = json.dumps(yaml.safe_load(data))
    return out


def get_request(route, header):
    name = requests.request("GET", url + route, headers=header)
    global counter
    counter += 1
    get_route(name)
    convert_to_json(name)


def get_route(res_name):
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


def convert_to_json(file_text):
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