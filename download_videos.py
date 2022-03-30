import cv2
import requests
import numpy as np

from multiprocessing import Pool
import tqdm

VIDEO_NAMES = ["20220316_C0163.MP4", "20220316_C0199.MP4"]
API_KEY = "YOUR_API_KEY"

def download_image_from_url(url):
    response = requests.get(url)
    arr = np.asarray(bytearray(response.content), dtype=np.uint8)
    cv2_img = cv2.imdecode(arr, cv2.IMREAD_UNCHANGED)
    return url, cv2_img    


if __name__ == '__main__':
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
    completed_jobs = [job["video_name"] for job in jobs if job["status"] == "finished"]
    incomplete_jobs = [job["video_name"] for job in jobs if job["status"] != "finished"]
    jobs = completed_jobs + incomplete_jobs

    print("COMPLETED JOBS:", completed_jobs)
    print("INCOMPLETE JOBS:", incomplete_jobs)
    print("-------------------------------------------------------")

    for VIDEO_NAME in VIDEO_NAMES:
        print(f"{VIDEO_NAME}\n")
        if VIDEO_NAME not in jobs:
            print(f"Skipping {VIDEO_NAME}, doesn't exist in project")
            continue
        if VIDEO_NAME in incomplete_jobs:
            print(f"Skipping {VIDEO_NAME}, hasn't completed processing")
            continue
        
        print(f"Downloading {VIDEO_NAME}, job has completed in the cloud")

        # get urls of processed video
        r = requests.get(
            "https://api.sievedata.com/v1/get_metadata",
            params={
                "project_name": "demo_project",
                "video_name": VIDEO_NAME
            },
            headers={"X-API-Key": API_KEY, "Content-Type": "application/json"},
        )

        samples = r.json()["metadata"]
        samples.sort(key=lambda x: x["frame_number"])
        urls = [x["background_removed_url"] for x in samples]


        video_writer = None
        pool = Pool(50)
        for url, cv2_img in tqdm.tqdm(pool.map(download_image_from_url, urls), total=len(urls)):
            if video_writer is None:
                width = cv2_img.shape[1]
                height = cv2_img.shape[0]
                frame_rate = 30
                fourcc = cv2.VideoWriter_fourcc(*'MP4V')
                video_writer = cv2.VideoWriter(f'{VIDEO_NAME}_out.mp4', fourcc, int(frame_rate), (int(width), int(height)))

            video_writer.write(cv2_img)

        video_writer.release()
        print(f"Finished downloading background removed {VIDEO_NAME} into {VIDEO_NAME}_out.mp4")
        print("-------------------------------------------------------")