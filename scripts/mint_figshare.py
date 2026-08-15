#!/usr/bin/env python

# modified from https://docs.figshare.com/#doc-section-upload-example

import hashlib
import json
import os
import requests
from requests.exceptions import HTTPError

FIGSHARE_TOKEN = os.environ.get("FIGSHARE_TOKEN")
CHANGED_FILES = os.environ.get("CHANGED_FILES", "")
PR_TITLE = os.environ.get("PR_TITLE", "GitHub Automation Upload")
HEADERS = {"Authorization": f"token {FIGSHARE_TOKEN}"}
BASE_URL = 'https://api.figshare.com/v2/{endpoint}'
CHUNK_SIZE = 1048576

def raw_issue_request(method, url, data=None, binary=False):
    if data is not None and not binary:
        data = json.dumps(data)
    response = requests.request(method, url, headers=HEADERS, data=data)
    try:
        response.raise_for_status()
        try:
            data = json.loads(response.content)
        except ValueError:
            data = response.content
    except HTTPError as error:
        raise ValueError(error.message)
    return data

def issue_request(method, endpoint, *args, **kwargs):
    return raw_issue_request(method, BASE_URL.format(endpoint=endpoint), *args, **kwargs)

def create_article(metadata):
    result = issue_request('POST', 'account/articles', data=metadata)
    result = raw_issue_request('GET', result['location'])
    article_id = result['id']
    # figshare automatically adds contributors as first author, remove first author
    author_id = result['authors'][0]['id']
    issue_request('delete',f"account/articles/{article_id}/authors/{author_id}")
    return article_id

def get_file_check_data(file_name):
    with open(file_name, 'rb') as fin:
        md5 = hashlib.md5()
        size = 0
        data = fin.read(CHUNK_SIZE)
        while data:
            size += len(data)
            md5.update(data)
            data = fin.read(CHUNK_SIZE)
        return md5.hexdigest(), size

def initiate_new_upload(article_id, file_name):
    endpoint = f"account/articles/{article_id}/files"
    md5, size = get_file_check_data(file_name)
    data = {'name': os.path.basename(file_name),
            'md5': md5,
            'size': size}
    result = issue_request('POST', endpoint, data=data)
    result = raw_issue_request('GET', result['location'])
    return result

def complete_upload(article_id, file_id):
    issue_request('POST', f"account/articles/{article_id}/files/{file_id}")

def upload_parts(file_info, file_name):
    url = '{upload_url}'.format(**file_info)
    result = raw_issue_request('GET', url)
    with open(file_name, 'rb') as fin:
        for part in result['parts']:
            upload_part(file_info, fin, part)

def upload_part(file_info, stream, part):
    udata = file_info.copy()
    udata.update(part)
    url = '{upload_url}/{partNo}'.format(**udata)
    stream.seek(part['startOffset'])
    data = stream.read(part['endOffset'] - part['startOffset'] + 1)
    raw_issue_request('PUT', url, data=data, binary=True)

def upload_file(article_id, file_name):
    file_info = initiate_new_upload(article_id, file_name)
    upload_parts(file_info, file_name)
    complete_upload(article_id, file_info['id'])

def publish_article(article_id):
    resp = issue_request('POST', f"account/articles/{article_id}/publish")
    if resp.status_code == 202:
        time.sleep(5)
        resp = issue_request('GET', f"account/articles/{article_id}")
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
    print("Creating article…")
    with open(target_json, 'r', encoding='utf-8') as file:
        article_data = json.load(file)
    article_id = create_article(metadata = {
        "title": f"Equine Assay Registry: {PR_TITLE}",
        "authors": [{'name': f"{a['firstName']} {a['lastName']}",
                     'orcid_id': a['orcid']} for a in article_data['submissionDetails']['authors']],
        "description": "Data upload via GitHub Actions for original Equine Assay Registry contribution.",
        "categories": [24097],
        "keywords": ["assay validation","equine"],
        "license": 1 #CC BY 4.0
    })
    for sf in [target_json] + supporting_files:
        print(f"Uploading file: {sf}")
        upload_file(article_id, sf)
    print("Publishing article…")
    doi = publish_article(article_id)
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

if __name__ == '__main__':
    main()
