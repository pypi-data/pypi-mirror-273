from typing import Dict, TypedDict

class TakionAPI:
    DOMAIN = "https://takionapi.tech"
    

class CookieRequest(TypedDict):
    payload: Dict[str, str]
    headers: Dict[str, str]
    url: str

class IncapsulaGeeTest(TypedDict):
    gt: str
    challenge: str
    gee_test_reese84: str
    request_reese84: str