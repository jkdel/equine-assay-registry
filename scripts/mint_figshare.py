import os
import sys
import json
import requests
import time

FIGSHARE_TOKEN = os.environ.get("FIGSHARE_TOKEN")
CHANGED_FILES = os.environ.get("CHANGED_FILES", "")
PR_TITLE = os.environ.get("PR_TITLE", "GitHub Automation Upload")
HEADERS = {"Authorization": f"token {FIGSHARE_TOKEN}"}
BASE_URL = "https://api.figshare.com/v2/account/articles"

def create_article(metadata):
    """Creates a draft Figshare article."""
    resp = requests.post(BASE_URL, headers=HEADERS, json=metadata)
    resp.raise_for_status()
    location = resp.headers.get("Location")
    if not location:
        raise Exception("Failed to get article location from Figshare")
    return location

def upload_file(article_url, file_path):
    """Handles Figshare's 3-step file upload process."""
    file_size = os.path.getsize(file_path)
    file_name = os.path.basename(file_path)
    init_data = {"name": file_name, "size": file_size}
    resp = requests.post(f"{article_url}/files", headers=HEADERS, json=init_data)
    resp.raise_for_status()
    file_info = resp.json()
    upload_url = file_info["upload_url"]
    file_id = file_info["id"]
    with open(file_path, "rb") as f:
        resp = requests.put(upload_url, data=f)
        resp.raise_for_status()
    resp = requests.post(f"{article_url}/files/{file_id}", headers=HEADERS)
    resp.raise_for_status()
    print(f"Successfully uploaded {file_name}")

def publish_article(article_url):
    """Publishes the article to mint the DOI."""
    resp = requests.post(f"{article_url}/publish", headers=HEADERS)
    if resp.status_code == 202:
        print("Article is processing on Figshare, waiting 10 seconds...")
        time.sleep(5)
        resp = requests.get(article_url, headers=HEADERS)
        resp.raise_for_status()
    elif resp.status_code == 200:
        pass
    else:
        resp.raise_for_status()
    return resp.json().get("doi")

def main():
    changed_files = [f.strip() for f in CHANGED_FILES.split(' ') if f.strip()]
    existing_files = [f for f in changed_files if os.path.exists(f)]
    target_json = [f for f in existing_files if f.endswith('.json')][0]
    supporting_files = [f for f in existing_files if f != target_json]
    print("Creating Figshare article...")
    article_url = create_article({
        "title": f"Data for PR: {PR_TITLE}",
        "description": "Automated data upload from GitHub repository via GitHub Actions.",
        "defined_type": "dataset"
    })
    print("Uploading files...")
    for sf in [target_json] + supporting_files:
        upload_file(article_url, sf)
    print("Publishing article...")
    doi = publish_article(article_url)
    if not doi:
        print("Error: Could not retrieve DOI after publishing.")
        sys.exit(1)
    print(f"DOI minted successfully: {doi}")
    with open(target_json, "r") as f:
        data = json.load(f)
    data["submissionDetails"]["doi"] = doi
    with open(target_json, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Updated {target_json} with new DOI.")

if __name__ == "__main__":
    main()
