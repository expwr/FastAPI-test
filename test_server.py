import requests

# Retrieves item by id
print(requests.get("http://127.0.0.1:8000/items/0").json())

# Retrieves item by name
print(requests.get("http://127.0.0.1:8000/items?name=Chocolate_bar").json())

# Adds a new item 
print(requests.post("http://127.0.0.1:8000/", json={"name": "Crunch_bar", "price": 3.99, "count": 23, "id": 3, "category": "candy"}).json())

# Updates an item 
print(requests.put("http://127.0.0.1:8000/items/0?count=9001").json())
print(requests.get("http://127.0.0.1:8000/").json())

# Deletes the item
print(requests.delete("http://127.0.0.1:8000/delete/0").json())
print(requests.get("http://127.0.0.1:8000/items").json())
