from instagrapi import Client
from urllib.request import urlretrieve
import os

def login(client):
	client.login("hairy_choiga_23", "787newpassword")
	
if __name__ == "__main__":
	cl = Client()
	login(cl)

	user_id = cl.user_id_from_username("oppyolly")
	medias = cl.user_medias(user_id, 20)
	urls = [media.video_url for media in medias]
	print(urls)
	print(len(urls))

	for i in range(0, len(urls)):
		print
		url = urls[i]
		if url is not None:
			urlretrieve(str(url), "oppyolly_videos_" + str(i) + ".mp4")

	cl.clip_upload(os.path.dirname(__file__) + "/oppyolly_videos_10.mp4", "hello this is a test from instagrapi")





