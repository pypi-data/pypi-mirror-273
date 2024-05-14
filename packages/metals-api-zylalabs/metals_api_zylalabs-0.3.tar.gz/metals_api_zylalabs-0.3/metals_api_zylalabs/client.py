import requests

class MetalsApiClient:
    
    def __init__(self, access_key:str):
        self.access_key = access_key
        
    def get_latest(self, base:str, symbols):
        URL = "https://metals-api.com/api/latest"        
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