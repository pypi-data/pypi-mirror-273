import httpx
import json
import os

class SnusbaseModel:
    """
    api_key : your snusbase api key
    """
    def __init__(
        self,
        api_key: str
    ) -> None:
        self.api_key = api_key
        self.client  = httpx.Client()

    def find_ip(self, ip_address) -> dict:
        r = self.client.get(
            url = f'https://beta.snusbase.com/v1/whois/{ip_address}',
            headers = {
                "Authorization": self.api_key
            }
        )
        if r.status_code == 200:
            return r.json()
        else:
            return {"error": "failed"}
        
    