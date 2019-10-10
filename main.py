import time
import concurrent.futures
import os
import requests
import socket
import json
import sys
import pickle

import functions

def client():
    HOST = '127.0.0.1'  # The server's hostname or IP address
    PORT = 65432        # The port used by the server

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        while True:
            val = input("$>: ")
            if val == "exit":
                print("Bye bye dear!")
                s.sendall(b"exit")
                break
            elif "find" in val:
                data_to_send = []
                data_to_send.append(functions.json_data)
                values = val.rsplit(" ",2)
                if len(values) == 2:
                    data_to_send.append(values[1])
                elif len(values) == 3:
                    data_to_send.append(values[1])
                    data_to_send.append(values[2])
                data_to_send = pickle.dumps(data_to_send)
                s.sendall(data_to_send)
                data = s.recv(15000)
                data = pickle.loads(data)
                for el in data:
                    print(el)
            else:
                print("Incorrect command")     
    
def get_routes_from_server():
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

if __name__ == "__main__":
    get_routes_from_server()
    client()


