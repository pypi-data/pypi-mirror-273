import contextvars
import os

NodeClsKey = "x-apaas-node-cls"

CtxVar = contextvars.ContextVar(NodeClsKey)

try:
    from _sys import CtxVar  # type: ignore
except Exception:
    pass


def Ctx():
    return contextvars.copy_context()


def get_ctx():
    try:
        return CtxVar.get()
    except LookupError:
        CtxVar.set({})
        return CtxVar.get()


def get_ctx_key(key):
    try:
        return get_ctx()[key]
    except Exception:
        return None


def get_from_credential(key: str):
    credential = get_ctx_key("credential")
    if credential is None:
        return ""
    return credential["key"]


def is_local_dev():
    return os.environ.get("AILY_SDK_LOCAL_DEBUG") == "true"


def get_client_id():
    if is_local_dev():
        return os.environ.get("AILY_SDK_CLIENT_ID")
    return get_from_credential("clientID")


def get_client_secret():
    if is_local_dev():
        return os.environ.get("AILY_SDK_CLIENT_SECRET")
    return get_from_credential("clientSecret")


def get_domain():
    if is_local_dev():
        return os.environ.get("AILY_SDK_DOMAIN")
    return get_from_credential("domain")


def get_by_headers(key):
    headers = get_ctx_key("headers")
    if headers is None:
        return ""
    return headers[key]
