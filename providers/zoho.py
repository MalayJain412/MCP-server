import requests
from providers.base import CRMProvider
from config import ZOHO_BASE_URL, API_TIMEOUT

class ZohoProvider(CRMProvider):

    def create_lead(self, payload):
        res = requests.post(
            f"{ZOHO_BASE_URL}/zoho/leads",
            json=payload,
            timeout=API_TIMEOUT
        )

        return {
            "status_code": res.status_code,
            "json": res.json()
        }
