from urllib.parse import urljoin
import json
from ..common.context import get_domain
from ..credential import AppCredential
from ..common.util import get_http_session

defaultOptions = {
    "timeout": 60 * 1000 * 5,
    "retry_times": 0,
}


def call_action(
    action_api_name: str,
    action_data: dict,
    options: dict = {},
) -> dict:
    credential = AppCredential()
    token = credential.get_token()
    domain = get_domain()

    if not token:
        raise Exception('get token failed')

    http = get_http_session(token)
    req = {
        'customerBizId': 'spring',
        'data': {
            'actionApiName': action_api_name,
            'actionData': json.dumps(action_data),
            'options': json.dumps({
                **defaultOptions,
                **options,
            }),
        },
    }

    path = f'/ai/v1/connector_action/namespaces/{credential.namespace}/execute_action'  # noqa: E501
    url = urljoin(domain, path)
    res = http.post(url, json=req)

    if res.status_code != 200:
        raise Exception(f'call action failed: {res.text}')

    data = res.json()
    if data['code'] != '0':
        raise Exception(f'call action failed: {data}')

    if not data['data']['data']:
        raise Exception(f'parse action response error: data is empty, {data}')

    return data['data']['data']
