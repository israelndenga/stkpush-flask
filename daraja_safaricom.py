import requests
from requests.auth import HTTPBasicAuth

consumer_key = "apSEeKMsRr5Amkdw8tNpk20PqT0Gw3xSsaMZvE0jLdrDJyce"
consumer_secret = "NzsxZzkX4Yr3R4LAjcKKFaxh8GRAWaAFAchCkwBzRkzkKmxGmR9NChRiKBLnhycQ"

api_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

print("👉 Requesting access token...")

response = requests.get(api_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))

print("✅ Status code:", response.status_code)
print("✅ Response body:", response.text)
input("Press Enter to exit...")
