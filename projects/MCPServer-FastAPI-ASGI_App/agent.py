import requests

# Define variables
endpoint = "/items/"
base_url = "http://localhost:3000"
url = f"{base_url}{endpoint}"

# Print a message about what is being tested
print(f"Testing GET {url}")

# Send a GET request to the endpoint
response = requests.get(url)

# Print the status code
print(f"Status code: {response.status_code}")

# Print the response body
print("Response:\n", response.json())
