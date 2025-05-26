import requests
import subprocess
import config


def delete_git_lfs_by_oid(oid):
    url = f"https://bitbucket.org/!api/internal/repositories/{config.workspace}/{config.repository}/lfs/{oid}"
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://bitbucket.org',
        'priority': 'u=1, i',
        'referer': 'https://bitbucket.org',
        'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
        'x-csrftoken': 'paD5ojHfHBpsjrZSswN8hhmWxdh1y6rzPImNnaPR5iWAo29E9SfOw0LwsE1oulBX',
        'x-requested-with': 'XMLHttpRequest',
    }

    response = requests.delete(url, headers=headers, cookies=config.cookies)

    # print("Status Code:", response.status_code)
    # print("Response Content:", response.text)

    return response

def delete():
    dangling_git_lfs_data = config.read_git_lfs_data_from_file(config.dangling_git_lfs_data_filename)
    for item in dangling_git_lfs_data:
        try:
            response = delete_git_lfs_by_oid(item.content_oid)
            print(f"Delete Git LFS object {item.content_oid} server response with code: {response.status_code}")
        except subprocess.CalledProcessError as e:
            print(f"Error while running git command for {item.content_oid}: {e}")

    print(f"Delete operation completed.")