import requests

r=requests.get("https://upload.pypi.org/legacy/")

print(r.status_code)