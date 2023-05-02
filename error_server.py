import requests

# These are going to be checking values using Path and Query 

# Results in error since the count and price and negative
print(requests.put("http://127.0.0.1:8000/update/0?count=-1").json())
print(requests.put("http://127.0.0.1:8000/update/0?price=-1").json())

# Results in an error because item id cannot be negative
print(requests.put("http://127.0.0.1:8000/update/-1").json())

# The name cannot exceed 8 characters
print(requests.put("http://127.0.0.1:8000/update/0?name=SuperDuperHammer").json())