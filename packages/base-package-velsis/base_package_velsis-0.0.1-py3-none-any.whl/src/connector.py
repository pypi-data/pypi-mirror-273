import requests


def getInfo(status_code: int = 404):
    response = requests.get(f"https://http.cat/{status_code}")
    print(response.json())
