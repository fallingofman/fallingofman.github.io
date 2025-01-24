from instagrapi import Client
from urllib.request import urlretrieve
import os
import argparse

meme_page_usernames = ["oppyolly"]
number_of_daily_posts = 1

def login(client):
    client.login("hairy_choiga_23", "787newpassword")

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
    all_media = all_media[:number_of_daily_posts]
    print(len(all_media))
    for i in range(0, number_of_daily_posts):
        url = all_media[i].video_url 
        if url is not None:
            urlretrieve(str(url), "daily_videos_" + str(i) + ".mp4")

def upload_videos(client):
    files = os.listdir('.')
    files = [file for file in files if "daily_videos" in file]
    if len(files) > 0:
        next_file_upload_name = files[0]
        client.clip_upload(os.path.dirname(__file__) + "/" + next_file_upload_name, "hello this is a test from instagrapi")
        os.remove(next_file_upload_name)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--state', help='1: download, 2: upload')
    args = parser.parse_args()

    cl = Client()
    login(cl)

    if args.state == "1":
        print(args.state)
        user_media_map = pull_meme_data(cl, meme_page_usernames)
        print(user_media_map)
        download_videos_for_upload(user_media_map)
    if args.state == "2":
        upload_videos(cl)






