import socket
import json
import pickle


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


result = []


def find_value(key_name, json_data, *value_name):
    for el in json_data:
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
                        result.append(new_el)
                elif len(value_name) == 0:
                    if key == key_name:
                        result.append(new_el)


if __name__ == "__main__":
    HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
    PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(15000)
                if data == b"exit":
                    print("Bye bye dear!")
                    break
                else:
                    data = pickle.loads(data)
                    if len(data) == 2:
                        find_value(data[1], data[0])
                    elif len(data) == 3:
                        find_value(data[1], data[0], data[2])
                    print("Result length: ",len(result))
                    result = pickle.dumps(result)
                    conn.sendall(result)
                    result = []
