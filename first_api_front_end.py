import requests
import json

USER = {
    "username": "test2",
    "first_name": "Test",
    "last_name": "User",
    "password": "testing123",
}

HOST_URL = "http://localhost:5011"
REGISTER_URL = "/register/"

this_user = {}

for k in USER.keys():
    this_user[k] = input(f"Enter {k} or press ENTER for default ({USER[k]})") or USER[k]

response = requests.post(url=HOST_URL+REGISTER_URL, json=this_user)

pass