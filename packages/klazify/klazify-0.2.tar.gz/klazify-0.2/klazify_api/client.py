import requests

class KlazifyApiClient:
    
    def __init__(self, access_key:str):
        self.access_key = access_key
        
    def categorize_url(self, url:str):
        URL = "https://api.klazify.com/categorize"
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
        
    def get_latest(self, base:str, symbols):
        URL = "https://commodities-api.com/api/latest"        
        params = {
            "access_key": self.access_key,
            "base": base,
        }
        if isinstance(symbols, list):
            params["symbols"] = ",".join(symbols)
        else:
            params["symbols"] = symbols
        
        response = requests.get(URL, params=params)        
        data = response.json()        
        return data
    
    def get_historical(self, date:str, base:str, symbols):
        URL = f"https://commodities-api.com/api/{date}"        
        params = {
            "access_key": self.access_key,
            "base": base,
        }
        if isinstance(symbols, list):
            params["symbols"] = ",".join(symbols)
        else:
            params["symbols"] = symbols
        
        response = requests.get(URL, params=params)        
        data = response.json()        
        return data
    
    def get_time_series(self, start_date:str, end_date:str, base:str, symbols):
        URL = "https://commodities-api.com/api/timeseries"
        params = {
            "access_key": self.access_key,
            "start_date": start_date,
            "end_date": end_date,
            "base": base,
        }
        if isinstance(symbols, list):
            params["symbols"] = ",".join(symbols)
        else:
            params["symbols"] = symbols
        
        response = requests.get(URL, params=params)
        data = response.json()
        return data