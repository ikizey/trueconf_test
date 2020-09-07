import requests

URL = "http://127.0.0.1:5000/"

# check user list
response = requests.get(url=URL)
print(response.json())

# check user1
url1 = URL + "user/1"
response = requests.get(url=url1)
print(response.json())

# check user1
url2 = URL + "user/2"
response = requests.get(url=url2)
print(response.json())

# check user3 (not exists yet)
url3 = URL + "user/3"
response = requests.get(url=url3)
print(response.json())

# add user3
urladd = URL + "users/add"
response = requests.put(url=urladd, json={'name': 'Jack'})
print(response.json())

# delete user3
response = requests.delete(url=url3)
print(response.json())

# check user3 (not exists again)
url3 = URL + "user/3"
response = requests.get(url=url3)
print(response.json())

# check user2 update
response = requests.post(url=url2, json={'name': 'Jack'})
print(response.json())