from instagrapi import Client
from urllib.request import urlretrieve
import os
import argparse
from Login import load_secret

meme_page_usernames = ["oppyolly"]

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

def pull_meme_data(client, meme_page_usernames):
    user_media_map = {}
    for username in meme_page_usernames:
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--state', help='1: download, 2: upload')
    args = parser.parse_args()

    cl = Client()
    login(cl)

    # make sure the video directory exists
    if not os.path.exists(VIDEO_DIR):
        os.makedirs(VIDEO_DIR)

    if args.state == "1":
        print(args.state)
        user_media_map = pull_meme_data(cl, meme_page_usernames)
        print(user_media_map)
        download_videos_for_upload(user_media_map)
    if args.state == "2":
        upload_videos(cl)






