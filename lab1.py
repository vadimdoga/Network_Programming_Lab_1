import requests
import time
import json
import csv
import threading
import concurrent.futures
import yaml
import os
from xmljson import Abdera
from xml.etree.ElementTree import fromstring
from collections import OrderedDict

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

    return name


def getRoute(res_name, route_name):
    route_text = res_name.text
    data = json.loads(route_text)
    if 'link' in data:
        link = data["link"]
        for key, value in link.items():
            route_name.append(value)
    else:
        print("no more links")

    return route_name


def makeFile(file_text, file_name):
    # f = open(file_name, "w")
    # f.write(file_text.text)
    # f.close()
    file_json = file_text.text
    data = json.loads(file_json)
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


f = open("file.json","w")
f.write("[")
f.close()
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


def route_1():
    for route in route1:
        new_route = getRequest(route, header)
        makeFile(new_route, route.replace("/", ""))
        getRoute(new_route, route1)


def route_2():
    for route in route2:
        new_route = getRequest(route, header)
        makeFile(new_route, route.replace("/", ""))
        getRoute(new_route, route2)


def route_3():
    links = []
    for route in route3:
        new_route = getRequest(route, header)
        makeFile(new_route, route.replace("/", ""))
        getRoute(new_route, links)
    link31 = []
    link32 = []
    link33 = []
    link31.append(links.pop(0))
    link32.append(links.pop(0))
    link33.append(links.pop(0))

    def link_31():
        for route in link31:
            new_route = getRequest(route, header)
            makeFile(new_route, route.replace("/", ""))
            getRoute(new_route, link31)

    def link_32():
        for route in link32:
            new_route = getRequest(route, header)
            makeFile(new_route, route.replace("/", ""))
            getRoute(new_route, link32)

    def link_33():
        for route in link33:
            new_route = getRequest(route, header)
            makeFile(new_route, route.replace("/", ""))
            getRoute(new_route, links)
        link331 = []
        link332 = []
        link331.append(links.pop(0))
        link332.append(links.pop(0))

        def link_331():
            for route in link331:
                new_route = getRequest(route, header)
                makeFile(new_route, route.replace("/", ""))
                getRoute(new_route, link331)

        def link_332():
            for route in link332:
                new_route = getRequest(route, header)
                makeFile(new_route, route.replace("/", ""))
                getRoute(new_route, link332)
        executor331 = threading.Thread(target=link_331)
        executor332 = threading.Thread(target=link_332)

        executor331.start()
        executor332.start()

        executor331.join()
        executor332.join()
    executor33 = threading.Thread(target=link_33)
    executor32 = threading.Thread(target=link_32)
    executor31 = threading.Thread(target=link_31)

    executor33.start()
    executor31.start()
    executor32.start()

    executor31.join()
    executor32.join()
    executor33.join()


def route_4():
    for route in route4:
        new_route = getRequest(route, header)
        makeFile(new_route, route.replace("/", ""))
        getRoute(new_route, route4)


start = time.time()
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    executor.submit(route_3)
    executor.submit(route_1)
    executor.submit(route_2)
    executor.submit(route_4)

end = time.time()
print(f"Done in {end - start}")

os.remove("file.csv")

f = open("file.json","a")
f.write("]")
f.close()