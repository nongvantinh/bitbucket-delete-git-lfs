import config
import os
import subprocess

def locate():
    if os.path.exists(config.dangling_git_lfs_data_filename):
        print(f"File {config.dangling_git_lfs_data_filename} already exists. Please consider what to do with it (delete/rename) before using this operation.")
        return

    git_lfs_data = config.read_git_lfs_data_from_file(config.git_lfs_data_filename)
    dangling_git_lfs_data = []
    for item in git_lfs_data:
        try:
            result = subprocess.run(["git", "log", "--all", "--format=%H", "-S", item.content_oid], capture_output=True, text=True, check=True)
            if result.stdout.strip():
                # print(f"Found in git history: {item.content_oid}")
                pass
            else:
                print(f"{item.content_oid} not found in git history")
                dangling_git_lfs_data.append(item)
        except subprocess.CalledProcessError as e:
            print(f"Error while running git command for {item.content_oid}: {e}")

    config.save_git_lfs_data_to_file(dangling_git_lfs_data, config.dangling_git_lfs_data_filename)

    print(f"Dangling Git LFS data saved to {config.dangling_git_lfs_data_filename}.")