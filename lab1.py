import requests
import time
from time import sleep
import json
import threading
import queue
import concurrent.futures
from requests.exceptions import HTTPError

counter = 2
def getRequest(route, header):
    name = requests.request("GET", url + route, headers=header)
    global counter
    counter += 1
    getRoute(name)
    
def getRoute(res_name):
    route_text = res_name.text
    data = json.loads(route_text)
    if 'link' in data:
        link = data["link"]
        for key, value in link.items():
            routes.put(value)
            print(value)
            new_routes_list.append(value)
    else:
        print("no more links")
    return routes


def makeFile(file_text, file_name):
    f = open(file_name, "w")
    f.write(file_text.text)
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
        print(counter)
        print(len(new_routes_list))
        if(routes.empty()):
            if counter == len(new_routes_list):
                break

    
end = time.time()
print(f"Done in {end - start}")
