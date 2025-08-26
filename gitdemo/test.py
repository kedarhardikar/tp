import requests

resp = requests.post("http://127.0.0.1:5000/predict",
                     json={"tweet": "The CDC currently reports 99031 deaths. In general the discrepancies in death counts between different sources are small and explicable. The death toll stands at roughly 100000 people today."})
print(resp.json())
