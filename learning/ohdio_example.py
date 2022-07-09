import requests

url = "https://services.radio-canada.ca/neuro/sphere/v1/audio/apps/products/programmes-v2/la-soiree-est-encore-jeune/2"

querystring = {"context":"web","pageNumber":"2"}

payload = ""
response = requests.request("GET", url, data=payload, params=querystring)

print(response.text)
