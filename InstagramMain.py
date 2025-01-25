from instagrapi import Client
from urllib.request import urlretrieve
import os
import argparse
from Login import load_secret

NUMBER_OF_DAILY_POSTS = 1
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
        user_media_map[username] = client.user_medias(user_id, 20)
    print(user_media_map)
    return user_media_map

def download_videos_for_upload(user_media_map):
    all_media = user_media_map.values()
    all_media = sum(all_media, [])
    all_media = sorted(all_media, key=lambda post: post.like_count)
    all_media = all_media[:NUMBER_OF_DAILY_POSTS]
    print(len(all_media))
    for i in range(0, NUMBER_OF_DAILY_POSTS):
        url = all_media[i].video_url 
        if url is not None:
            video_name = "daily_videos_" + str(i) + ".mp4"
            video_path = os.path.join(VIDEO_DIR, video_name)
            urlretrieve(str(url), video_path)

def upload_videos(client, count=1):
    for i, file in zip(range(count), os.listdir(VIDEO_DIR)):
        video_path = os.path.join(VIDEO_DIR, file)
        client.clip_upload(video_path, CAPTION)
        os.remove(video_path)

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

    print("user list:")
    print("\n".join(user_list))
    
    cl = Client()
    login(cl)

    if args.mode == "1":
        print("downloading mode")
        user_media_map = pull_meme_data(cl, user_list)
        print(user_media_map)
        download_videos_for_upload(user_media_map)
    if args.mode == "2":
        print("uploading mode")
        upload_videos(cl)






