import requests
import json

class User:
    def __init__(self, user_id, access_token):
        self.user_id = user_id
        self.access_token = access_token
        self.headers = {
            "userId": user_id,
            "Access-Token": access_token,
            "User-Agent": "okhttp/3.12.1"
        }

    def get_user_info(self):
        url = "http://modsgs.sandboxol.com/user/api/v2/user/details/info"
        response = requests.get(url, headers=self.headers)
        return self._handle_response(response)
        
    def set_birthday(self, birthday):
        url = "http://modsgs.sandboxol.com/user/api/v1/user/info"
        payload = {"birthday": birthday}
        response = requests.put(url, json=payload, headers=self.headers)
        return self._handle_response(response)
        
    def login(self, device_id, device_sign, password, user_id):
        url = "http://route.sandboxol.com/user/api/v1/app/login"
        headers = self.headers.copy()
        headers["bmg-device-id"] = device_id
        headers["bmg-sign"] = device_sign
        payload = {"password": password, "uid": user_id}
        response = requests.post(url, headers=headers, json=payload)
        return self._handle_response(response)
        
    def change_name(self, new_name):
        url = "http://modsgs.sandboxol.com/user/api/v3/user/nickName"
        params = {"newName": new_name, "oldName": "darkk.py"}
        response = requests.put(url, headers=self.headers, params=params)
        return self._handle_response(response)
        
    def change_details(self, new_details):
        url = "http://modsgs.sandboxol.com/user/api/v1/user/info"
        payload = {"details": new_details}
        response = requests.put(url, headers=self.headers, json=payload)
        return self._handle_response(response)
        
    def change_pfp(self, pfp_url):
        url = "http://modsgs.sandboxol.com/user/api/v1/user/info"
        payload = {"picUrl": pfp_url}
        response = requests.put(url, json=payload, headers=self.headers)
        return self._handle_response(response)
    
    def modify_password(self, old_password, new_password):
        url = "http://modsgs.sandboxol.com/user/api/v1/user/password/modify"
        payload = {"confirmPassword": "", "newPassword": new_password, "oldPassword": old_password}
        response = requests.post(url, json=payload, headers=self.headers)
        return self._handle_response(response)
        
    def bind_email(self, email, verify_code):
        url = "http://modsgs.sandboxol.com/user/api/v1/users/bind/email"
        payload = {"email": email, "verifyCode": verify_code}
        response = requests.post(url, json=payload, headers=self.headers)
        return self._handle_response(response)
        
    def unbind_email(self, verify_code, email):
        url = f"http://modsgs.sandboxol.com/user/api/v2/users/{self.user_id}/emails"
        params = {"email": email, "verifyCode": verify_code}
        response = requests.delete(url, params=params, headers=self.headers)
        return self._handle_response(response)
        
    def _handle_response(self, response):
        if response.status_code == 200:
            return response.json()
        else:
            return {"Error": f"Failed to perform action. Status code: {response.status_code}, Response: {response.text}"}


