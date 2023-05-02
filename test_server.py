import requests

# Retreives item by id
print(requests.get("http://127.0.0.1:8000/items/0").json())

# Retreives item by name
print(requests.get("http://127.0.0.1:8000/items?name=Chocolate_bar").json())

# Adds a new item 
print(requests.post("http://127.0.0.1:8000/", json={"name": "Crunch_bar", "price": 3.99, "count": 23, "id": 3, "category": "candy"}).json())