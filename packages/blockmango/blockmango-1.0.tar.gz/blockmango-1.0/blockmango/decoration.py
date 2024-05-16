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
		
	def current_price(self, skin_id, is_suit):
		url = "http://modsgs.sandboxol.com/decoration/api/v1/decoration/current/price"
		json = [{"id":skin_id,"isSuit":is_suit}]
		response = requests.post(url, json=json, headers=self.headers)
		return self._handle_response(response)
		
	def buy_skin(self, diamond, clothVoucher, paytype):
		url = "http://modsgs.sandboxol.com/shop/api/v1/new/shop/decorations/buy"
		params = {"diamond": diamond, "gold": 0, "clothVoucher": clothVoucher, "payType": paytype}
		response = requests.post(url, headers=self.headers, params=params)
		return self._handle_response(response)
	
	def shop_info(self):
		url = "http://modsgs.sandboxol.com/user/api/v1/user/shop/info"
		response = requests.get(url, headers=self.headers)
		return self._handle_response(response)
		
	def equip_skin(self, skinid):
		url = "http://modsgs.sandboxol.com/decoration/api/v1/decorations/using/new"
		params = {"ids": skinid}
		response = requests.post(url, params=params, header=self.headers)
		return self._handle_response(response)
		
		
    def _handle_response(self, response):
        if response.status_code == 200:
            return response.json()
        else:
            return {"Error": f"Failed to perform action. Status code: {response.status_code}"}
