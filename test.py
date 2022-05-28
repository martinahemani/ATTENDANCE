import requests
import json
url = 'https://7sj1hjl2qh.execute-api.us-east-1.amazonaws.com/test/attendance'
body = {

    "password": "hello",
    "name": "Marteena"
}
print(body["name"])
x = json.dumps(body)
print(x)
print(x[4])
# response = requests.post(url, data = json.dumps(body))
# print(response.text)
