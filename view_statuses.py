import requests

API_KEY = "YOUR_API_KEY"

r = requests.get(
    "https://api.sievedata.com/v1/get_all_jobs",
    params={
        "project_name": "demo_project",
    },
    headers={"X-API-Key": API_KEY, "Content-Type": "application/json"},
)

if r.status_code != 200:
    print(f"Error: {r.status_code}")
    print(r.text)
    exit(1)

jobs = r.json()["jobs"]

for job in jobs:
    print(f"{job['video_name']}")
    print(f"{job['status']}")
    print("-------------------------------------------------------")