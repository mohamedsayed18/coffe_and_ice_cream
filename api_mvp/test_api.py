import requests

# URL of the API login endpoint
login_url = 'https://example.com/api/login'

# Your login credentials
payload = {
    'username': 'your_username',
    'password': 'your_password'
}

# Send a POST request
response = requests.post(login_url, data=payload)