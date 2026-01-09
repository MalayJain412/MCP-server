from providers.zoho import ZohoProvider
from providers.salesforce import SalesforceProvider

PROVIDERS = {
    "zoho": ZohoProvider(),
    "salesforce": SalesforceProvider()
}
