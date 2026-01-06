import requests
from providers.base import CRMProvider
from config import SF_BASE_URL, API_TIMEOUT

class SalesforceProvider(CRMProvider):

    def create_lead(self, payload):
        res = requests.post(
            f"{SF_BASE_URL}/salesforce/leads",
            json=payload,
            timeout=API_TIMEOUT
        )

        return {
            "status_code": res.status_code,
            "json": res.json()
        }
