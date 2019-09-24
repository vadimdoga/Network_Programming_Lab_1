import requests
import time
import json
import threading
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


def makeFile(file_text, file_name):
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
    for route in route3:
        new_route = getRequest(route, header)
        makeFile(new_route, route.replace("/", ""))
        getRoute(new_route, route3)


def route_4():
    for route in route4:
        new_route = getRequest(route, header)
        makeFile(new_route, route.replace("/", ""))
        getRoute(new_route, route4)


try:
    t1 = threading.Thread(target=route_1)
    t2 = threading.Thread(target=route_2)
    t3 = threading.Thread(target=route_3)
    t4 = threading.Thread(target=route_4)
except:
    print("ERROR WITH THREADS")

start = time.time()
t4.start()
t3.start()
t2.start()
t1.start()

t4.join()
t3.join()
t2.join()
t1.join()

end = time.time()

print(f"Done in {end - start}")
