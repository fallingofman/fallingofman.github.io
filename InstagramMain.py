from instagrapi import Client
from urllib.request import urlretrieve
import os
import argparse
from Login import load_secret
from MediaStore import VideoInfo, MediaStore

NUMBER_OF_DAILY_POSTS = 24
LAST_N_POSTS = 20
VIDEO_DIR = "./videos"
CAPTION = "This is a test caption"

def login(client):
    # if there is a secret file, use that to login
    # otherwise use "hairy_choiga_23"
    username = "hairy_choiga_23"
    password = "787newpassword"

    if os.path.exists("./secret.txt"):
        username, password = load_secret("./secret.txt")
    
    client.login(username, password)

def pull_meme_data(client, usernames_list):
    user_media_map = {}
    for username in usernames_list:
        user_id = client.user_id_from_username(username)
        user_media_map[username] = client.user_medias(user_id, LAST_N_POSTS)
    print(user_media_map)
    return user_media_map

def download_videos_for_upload(user_media_map, ms:MediaStore):
    all_media = user_media_map.values()
    all_media = sum(all_media, [])
    all_media = sorted(all_media, key=lambda post: -post.like_count)
    # filter out non-video media, for now.
    all_media = [m for m in all_media if m.video_url is not None]
    all_media = all_media[:NUMBER_OF_DAILY_POSTS]

    print(len(all_media), "videos to download")
    ms.save_medias(all_media)

def upload_videos(client, ms:MediaStore, count=1):
    for i in range(count):
        vf = ms.get_one_media()
        video_path = os.path.join(VIDEO_DIR, vf.video_file_name)
        client.clip_upload(video_path, vf.caption_text)
        ms.delete_media(vf)

def load_accounts(accounts_dir):
    accounts_list = []
    with open(accounts_dir, 'r') as f:
        for line in f:
            accounts_list.append(line.strip())
    return accounts_list

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', help='1: download, 2: upload')
    parser.add_argument('--userlist', help='path to users file, a list of all users to target', required=True)
    args = parser.parse_args()

    # make sure the video directory exists
    if not os.path.exists(VIDEO_DIR):
        os.makedirs(VIDEO_DIR)

    user_list_dir = args.userlist
    user_list = load_accounts(user_list_dir)
    media_store = MediaStore(VIDEO_DIR)

    print("user list:")
    print("\n".join(user_list))
    
    cl = Client()
    login(cl)

    if args.mode == "1":
        print("downloading mode")
        user_media_map = pull_meme_data(cl, user_list)
        print(user_media_map)
        download_videos_for_upload(user_media_map, media_store)
    if args.mode == "2":
        print("uploading mode")
        upload_videos(cl, media_store)






