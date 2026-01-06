import time
import json

def audit_log(event: dict):
    event["ts"] = time.time()
    print(json.dumps(event))
