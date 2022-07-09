import requests


def download_cybos_plus_installer(filepath):
    url = "https://www.daishin.com/install/CYBOS5.exe"
    response = requests.get(url)
    with open(filepath, "wb") as f:
        f.write(response.content)
