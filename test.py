import requests

response = requests.get('https://www.example.com', timeout=10)

print(response.status_code)
