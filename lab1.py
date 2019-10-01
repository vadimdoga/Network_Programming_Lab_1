import requests
import time
import json
import threading
import concurrent.futures
from requests.exceptions import HTTPError


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


with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    executor.submit(all_routes, route1)
    executor.submit(all_routes, route2)
    executor.submit(all_routes, route3)
    executor.submit(all_routes, route4)

end = time.time()
print(f"Done in {end - start}")
