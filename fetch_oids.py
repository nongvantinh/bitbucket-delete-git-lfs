import requests
import os
from bs4 import BeautifulSoup
from typing import List
import config

def fetch_bitbucket_git_lfs_page(page_number=1):
    base_url = f'https://bitbucket.org/{config.workspace}/{config.repository}/admin/lfs/file-management/'
    params = {
        'sort': '-created',
        'iframe': 'true',
        'spa': '0'
    }
    if 0 < page_number:
        params['page'] = page_number

    url = requests.Request('GET', base_url, params=params).prepare().url

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'priority': 'u=0, i',
        'referer': 'https://bitbucket.org',
        'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'iframe',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    }
    response = requests.get(url, headers=headers, cookies=config.cookies)
    # print("Status Code:", response.status_code)
    # print("Response Content:")
    # with open("output.html", "w", encoding="utf-8") as file:
    #     file.write(response.text)
    # print(response.text)

    return response

def extract_git_lfs_data(html_content) -> List[config.GitLFSData]:
    soup = BeautifulSoup(html_content, 'html.parser')
    rows = soup.select('tbody tr')

    data = []
    for row in rows:
        size = row.select_one('td:nth-of-type(1)').text.strip()
        pushed_by = row.select_one('td:nth-of-type(2)').text.strip()
        content_oid = row.select_one('td:nth-of-type(3) code').text.strip()
        pushed_date = row.select_one('td:nth-of-type(4) time').text.strip()
        data.append(config.GitLFSData(size=size, pushed_by=pushed_by, content_oid=content_oid, pushed_date=pushed_date))

    # for item in data:
    #     print(item)

    return data


def fetch(page_index=1):
    if os.path.exists(config.git_lfs_data_filename):
        print(f"File {config.git_lfs_data_filename} already exists. Please consider what to do with it (delete/rename) before using this operation.")
        return


    page_response = fetch_bitbucket_git_lfs_page(page_index)
    while page_response.status_code == 200:
        print(f"Page {page_index} fetched successfully.")
        git_lfs_data = extract_git_lfs_data(page_response.text)
        config.save_git_lfs_data_to_file(git_lfs_data, config.git_lfs_data_filename)

        page_index += 1
        page_response = fetch_bitbucket_git_lfs_page(page_index)
    
    if page_response.status_code != 200:
        print(f"Failed to fetch page {page_index}. Status Code: {page_response.status_code}")
