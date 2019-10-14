# Laboratory Work No. 1

This is the first project on PR lectures.

## Getting Started

Here will be written each mandatory task and my implementation of it.

### Mandatory Tasks

```
1. Pull a docker container (alexburlacu/pr-server) from the registry
2. Run it, don't forget to forward the port 5000 to the port that you want on the local machine
3. Only languages and libraries supporting threads, locks and semaphores are allowed. Node or JS generally, Go, Elixir/Erlang are prohibited.
4. Now that you're up and running, you need to access the root route of the server and find your way to register
5. The access token that you get after accessing the register route must be put in http header of subsequent requests under the key X-Access-Token key
6. Most routes return a json with data and link keys. Extract data from data key and get next links fron link key
7. Hardcoding the routes is strictly forbidden. You need to "traverse" the api
8. Access token has a timeout of 20 seconds, and you are not allowed to get another token every time you access different route. So, one register per program run
9. Once you fetch all the data, convert it to a common representation, doesn't matter what this representation is
10. The final part of the lab is to make a concurrent TCP server, serving the fetched content, that will respond to (mandatory) a column selector message, like `SelectColumn column_name`, and (optional) `SelectFromColumn column_name glob_pattern`
11. All the code must be on GitHub with a readme file explaining the task and implementation

```

### Optional Tasks

```
1. `SelectFromColumn column_name glob_pattern` message for TCP server
2. Implementing your own thread pools
3. Using a limited number of threads for fetching data
4. Dispatch data to a different process pool/dedicated processes for conversion
5. Anything else, turn on your imagination

```

## Implementation

### First part(from task 1 till 6)

First steps were easy, so i will go further to access-token. To gain access token I made a get request to /register route, loaded and 
extracted 'token' for token and 'link' to have the next route.
```
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
```

### 7. Hardcoding the routes is strictly forbidden. You need to "traverse" the api
This is the function I use to not hardcode. It accepts the request result as an arg and then loads 'link' after it extracts all the links. 
```
name = requests.request("GET", url + route, headers=header)
get_route(name)
```
```
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
```
### 8. Access token has a timeout of 20 seconds, and you are not allowed to get another token every time you access different route. So, one register per program run


### 9. Once you fetch all the data, convert it to a common representation, doesn't matter what this representation is
After fetching I convert all data to JSON format using libraries. When a request is made it goes further to a function that gets the 'links' and after that it goes to convert_to_json function. It extracts the 'mime_type' which has info about the type of data and then uses it to access function of type converting.

```
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
```
### 10. The final part of the lab is to make a concurrent TCP server, serving the fetched content, that will respond to (mandatory) a column selector message, like `SelectColumn column_name`, and (optional) `SelectFromColumn column_name glob_pattern`

### Optional tasks:
1.Using a limited number of threads for fetching data
```
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
```
2.`SelectFromColumn column_name glob_pattern` message for TCP server

## Built With

* [Python](https://www.python.org/)


## Authors

* **Doga Vadim** - *All work* - [vadimdoga](https://github.com/vadimdoga)
