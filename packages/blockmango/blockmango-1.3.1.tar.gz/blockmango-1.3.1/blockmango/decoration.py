import requests
import json

class Decoration:
	def __init__(self, user_id, access_token):
		self.user_id = user_id
		self.access_token = access_token
		self.headers = {
		"userId": user_id,
		"Access-Token": access_token,
		"User-Agent": "okhttp/3.12.1"
		}
		
	def see_skins(self, uid):
		url = f"http://modsgs.sandboxol.com/decoration/api/v1/new/decorations/users/{uid}/classify/all"
		params = {"engineVersion": "10105",
		"os": "android", "showVip": 1}
		response = requests.get(url, headers=self.headers)
		return self._handle_response(reponse)