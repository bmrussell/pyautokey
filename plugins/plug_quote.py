import json
import os
from dataclasses import dataclass
 
import requests
from dotenv import load_dotenv
 
import factory
 
 
@dataclass
class PluginQuote:
    """Demonstrates calling a web API and returning the text as the value for insert"""
 
    trigger: str
    shortmatch: str
 
    def invoke(self)->str:
        try:
            load_dotenv()
            api_key = os.getenv('API_NINJA_KEY')
            api_url = 'https://api.api-ninjas.com/v1/quotes?category=best'
            response = requests.get(api_url, headers={'X-Api-Key': api_key})
            if response.status_code == requests.codes.ok:
                j = json.loads(response.text)
                quote = j[0]['quote']
                author = j[0]['author']
                return f"{quote}\n  -{author}"
        except Exception as ex:
            return f"Failed: {str(ex)}"
    
def register() -> None:
    factory.register("plug_quote", PluginQuote)
