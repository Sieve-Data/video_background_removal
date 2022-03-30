import requests

API_KEY = "YOUR_API_KEY"

VIDEO_URLS = [
    'https://www.dropbox.com/sh/xjdskprx970d6gt/AADm14JOjE1HjQzL9fUuvbD_a/20220316_C0163.MP4',
    'https://www.dropbox.com/sh/xjdskprx970d6gt/AACjgDn_C4olvIJQyifOd52Pa/20220316_C0199.MP4',
]

# Get Dropbox direct links
VIDEO_URLS = [url.replace('www.dropbox.com', 'dl.dropboxusercontent.com') for url in VIDEO_URLS]

for VIDEO_URL in VIDEO_URLS:
    print(f"{VIDEO_URL}\n")
    r = requests.post(
        "https://api.sievedata.com/v1/push_video",
        json={
            "project_name": "demo_project",
            "video_url": VIDEO_URL,
            "video_name": VIDEO_URL.split('/')[-1],
        },
        headers={"X-API-Key": API_KEY, "Content-Type": "application/json"},
    )

    if r.status_code != 200:
        print(f"Error: {r.status_code}")
        print(r.text)
        exit(1)

    print(f"Sent request for url with video_name {VIDEO_URL.split('/')[-1]}")
    print(r.json())
    print("-------------------------------------------------------")
