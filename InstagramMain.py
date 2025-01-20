from instagrapi import Client



def login(client):
	client.login("hairy_choiga_23", "787newpassword")
	
if __name__ == "__main__":
	cl = Client()
	login(cl)

	user_id = cl.user_id_from_username("oppyolly")
	medias = cl.user_medias(user_id, 20)
	print(medias)

