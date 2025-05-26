from dataclasses import dataclass
from typing import List

workspace = '<workspace>'
repository = '<project-name>'
# Just copy full the cookies from the browser and replace the value below
cookies = {
    'atl-bsc-consent-token': '<atl-bsc-consent-token>',
    'atl-bsc-show-banner': '0',
    'atlassian.account.xsrf.token': '<atlassian.account.xsrf.token>',
    'csrftoken': '<csrftoken>',
    'bb_session': '<bb_session>',
    '__awc_tld_test__': '<__awc_tld_test__>',
    'JSESSIONID': '<JSESSIONID>',
    'cloud.session.token': '<cloud.session.token>',
}



#===============================Common Configurations=========================================
git_lfs_data_filename = "git-lfs-data.txt"
dangling_git_lfs_data_filename = "dangling-git-lfs-data.txt"

@dataclass
class GitLFSData:
    size: str
    pushed_by: str
    content_oid: str
    pushed_date: str

def save_git_lfs_data_to_file(data: List[GitLFSData], filename):
    with open(filename, 'a', encoding='utf-8') as file:
        for item in data:
            file.write(f"Size: {item.size}, Pushed By: {item.pushed_by}, Content OID: {item.content_oid}, Pushed Date: {item.pushed_date}\n")


def read_git_lfs_data_from_file(filename: str) -> List[GitLFSData]:
    data = []
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split(", ")
            size = parts[0].split(": ")[1]
            pushed_by = parts[1].split(": ")[1]
            content_oid = parts[2].split(": ")[1]
            pushed_date = parts[3].split(": ")[1]
            
            data.append(GitLFSData(size=size, pushed_by=pushed_by, content_oid=content_oid, pushed_date=pushed_date))
    return data
