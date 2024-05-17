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
    
    def real_time_categorization(self, url:str):
        URL = "https://klazify.com/api/real_time_categorization"
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
    
    def domain_company(self, url:str):
        URL = "https://klazify.com/api/domain_company"
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
    
    def domain_logo(self, url:str):
        URL = "https://klazify.com/api/domain_logo"
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
    
    def domain_iab_categories(self, url:str):
        URL = "https://klazify.com/api/domain_iab_categories"
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
    
    def domain_tech(self, url:str):
        URL = "https://klazify.com/api/domain_tech"
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
    
    def domain_expiration(self, url:str):
        URL = "https://klazify.com/api/domain_expiration"
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
    
    def domain_social_media(self, url:str):
        URL = "https://klazify.com/api/domain_social_media"
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
    
    def similar_domain(self, url:str):
        URL = "https://klazify.com/api/similar_domain"
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