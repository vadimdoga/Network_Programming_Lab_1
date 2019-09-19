import requests
import json
from requests.exceptions import HTTPError


def getRequest(route, header):
    name = requests.request("GET", url + route, headers=header)
    return name


def getRoute(res_name, route_name):
    route_text = res_name.text
    data = json.loads(route_text)
    if 'link' not in data:
        print("no link")
    else:
        link = data["link"]
        for key, value in link.items():
            route_name.append(value)
    return routes


def makeFile(file_text,file_name):
    f = open(file_name, "w")
    f.write(file_text.text)
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

for route in route1:
    new_route = getRequest(route, header)
    makeFile(new_route,route.replace("/",""))
    getRoute(new_route, route1)
for route in route2:
    new_route = getRequest(route, header)
    makeFile(new_route,route.replace("/",""))
    getRoute(new_route, route2)
for route in route3:
    new_route = getRequest(route, header)
    makeFile(new_route,route.replace("/",""))
    getRoute(new_route, route3)
for route in route4:
    new_route = getRequest(route, header)
    makeFile(new_route,route.replace("/",""))
    getRoute(new_route, route4)

