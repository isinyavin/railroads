import requests

url = "http://localhost:5002/find-path"
data = {
    "start_station": "Adamstown",
    "end_station": "Howth"
}
headers = {"Content-Type": "application/json"}

response = requests.post(url, json=data, headers=headers)

print("Status Code:", response.status_code)
try:
    response_data = response.json()
    print("JSON Response:", response_data)
except requests.exceptions.JSONDecodeError:
    print("Response Content:", response.content)