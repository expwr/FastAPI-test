import requests

print(requests.get("http://127.0.0.1:8000/items/0").json())
print(requests.get("http://127.0.0.1:8000/items?name=Chocolate_bar").json())