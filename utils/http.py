import requests

def safe_request(fn):
    try:
        return fn()
    except requests.Timeout:
        return {"error": "TIMEOUT"}
    except requests.ConnectionError:
        return {"error": "NETWORK_ERROR"}
    except Exception as e:
        return {"error": "UNKNOWN", "detail": str(e)}
