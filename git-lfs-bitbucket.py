import argparse

import fetch_oids
import locate_dangling_git_lfs
import delete_git_lfs

def main():
    parser = argparse.ArgumentParser(description="Process git LFS operations.")
    
    parser.add_argument(
        '--fetch', 
        action='store_true', 
        help='Fetch OIDs'
    )
    
    parser.add_argument(
        '--locate', 
        action='store_true', 
        help='Locate dangling Git LFS objects'
    )
    
    parser.add_argument(
        '--delete', 
        action='store_true', 
        help='Delete Git LFS objects'
    )
    
    args = parser.parse_args()
    
    if args.fetch:
        print("Fetching OIDs...")
        fetch_oids.fetch()
    
    if args.locate:
        print("Locating dangling Git LFS objects...")
        locate_dangling_git_lfs.locate()
    
    if args.delete:
        print("Deleting Git LFS objects...")
        delete_git_lfs.delete()

if __name__ == "__main__":
    main()
