import time
import concurrent.futures
import os
import requests
import socket
import json

import functions


def delete_comma(element, end):
    new_element = str(element)
    new_element = new_element[:end]
    new_element += "]"
    return new_element


def prepare_json_xml(element, start, end):
    new_element = str(element)
    new_element = new_element[:end]
    new_element = new_element[start:]
    return new_element


def find_value(key_name, *value_name):
    for el in functions.json_data:
        if "36-0066196" in el:
            el = delete_comma(el, -3)
        loader = json.loads(el)
        if "record" in loader:
            el = prepare_json_xml(el, 11, -1)
            loader = json.loads(el)

        for new_el in loader:
            for key, value in new_el.items():
                if len(value_name) >= 1:
                    if key == key_name and value == value_name[0]:
                        print("Key:", key, " Value:", value)
                        print(new_el)
                elif len(value_name) == 0: 
                    if key == key_name and len(value_name) == 0:
                        print(new_el)


# def client():
#     HOST = '127.0.0.1'  # The server's hostname or IP address
#     PORT = 65432        # The port used by the server

#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         s.connect((HOST, PORT))
#         s.sendall(b'Hello, world')
#         data = s.recv(1024)

#     print('Received', repr(data))


if __name__ == "__main__":

    start = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        # register
        res_register = requests.request("GET", functions.url + "/register")
        # get access_token from json response
        json_register = res_register.text
        data = json.loads(json_register)
        x_access_token = data["access_token"]
        link = data["link"]
        header = {
            'X-Access-Token': x_access_token
        }

        # home route
        functions.get_request(link, header)

        for route in iter(functions.routes.get, None):
            executor.submit(functions.get_request, route, header)
            if(functions.routes.empty()):
                if functions.counter == len(functions.new_routes_list):
                    break

    os.remove("file.csv")
    end = time.time()
    print(f"Done in {end - start}")

    find_value("employee_id","36-0066196")
