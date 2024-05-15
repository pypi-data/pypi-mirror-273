import requests
from .context import get_by_headers


def get_http_session(token: str = '') -> requests.Session:
    s = requests.Session()
    s.headers.update({
        "Authorization": token,
        "biz_id": "spring",
        "x-tt-env": get_by_headers("x-tt-env"),
        "Content-Type": "application/json",
    })
    return s
