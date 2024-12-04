import requests
import logging
import azure.functions as func

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# URL /?op='<code>'&data='<data>'

# Http Trigger
@app.route(route="cortex_get_incidents")
def http_cortex_get_incidents(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    op = req.params.get('op')
    data = req.params.get('data')

    cortex = Cortex()
    response = ""
    match op: # Call the function based on the op and pass in data
        case "GetIncidents":
            # default code block
            response = cortex.get_incidents(data)
        case _:
            response = "Input data is missing"

    return func.HttpResponse(response,status_code=200)


class Cortex:
    def __init__(self):
        self.authorizationkey = "V0GvVUYNoLa81dqP19fmRqbbdxPCfhrvaGtFzkFZDhFNZmWUcbwTAHAl8nuEoyd6DwqOIdR0ToplZGANvSYO50eqbGnc0ARYoa0Lltq2FbTo1J6nqJkgjIwjbTJ9z3OO"
        self.authid = "55"
        self.url = "api-gpf.xdr.eu.paloaltonetworks.com"
        self.baseurl = "https://api-gpf.xdr.eu.paloaltonetworks.com/"

 
    def get_incidents(self, filters):
        try:
            request_body = {
                "request_data": {
                    "search_from": 0,
                    "search_to": 5
                }
            }

            response = requests.post(
                url=self.baseurl + "public_api/v1/incidents/get_incidents",
                json=request_body,
                headers={
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "Authorization": self.authorizationkey,
                    "x-xdr-auth-id": self.authid,
                }
            )

            # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
            response.raise_for_status()  

            json_response = response.json()
            reply = json_response["reply"]
            total_count = reply["total_count"]
            result_count = reply["result_count"]
            incidents = reply["incidents"]

            print(incidents[0])
            return incidents

        except requests.RequestException as e:
            raise SystemExit(f"Failed to make the request. Error: {e}") # Will result in HTTP 500


cortext = Cortex()
cortext.get_incidents("")
