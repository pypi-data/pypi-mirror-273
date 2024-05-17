import requests

class KlazifyApiClient:
    
    def __init__(self, access_key:str):
        self.access_key = access_key
        
    def categorize_url(self, url:str):
        URL = "https://klazify.com/api/categorize"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_key}"
        }
        payload = {
            "url": url
        }
        
        response = requests.post(URL, json=payload, headers=headers)
        data = response.json()
        return data