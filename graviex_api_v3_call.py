import time
import hmac
import hashlib
import requests

"""
WebSite https://graviex.net/desktop
API v3 https://graviex.net/documents/api_v3
API Usage Policy https://graviex.net/documents/user-agreement

if it useful you can make a donation
GIO: GQksGKKU6PotrByC8hQzBRwMAN7FuMNugF
ETH: 0x290fE67efA690AE7924DB416d4239daC9c309b97
"""
DEBUG = True


class GraviexAPI:
    def __init__(self, access_key=None, secret_key=None):
        self.access = access_key
        self.secret = secret_key
        self.uri_main = "/webapi/v3/"
        self.base_url = "https://graviex.net/"
        # or use
        # self.base_url = "https://graviex.net:443/"

    def call_api(self, uri_path, param_path=None, params=None, get=True):
        # create tonce & sorting parameters to make sure the request is correct
        time.sleep(2)  # edit as needed
        tonce = int(time.time()) * 1000

        if not params:
            params = {}
        params.update(dict(tonce=tonce, access_key=self.access))
        params_keys = list(params.keys())
        params_keys.sort()

        if DEBUG:
            print(f'params: {params}')

        # create {canonical_query} & {canonical_uri}
        request = ''
        for key in params_keys:
            value = params[key]
            request += f'{key}={value}&'

        if DEBUG:
            print(f'request: {request}')

        if param_path:
            uri = f'{self.uri_main}{uri_path}/{param_path}'

        else:
            uri = f'{self.uri_main}{uri_path}'

        if DEBUG:
            print(f'uri: {uri}')

        # create payload & signature (hash  of the request)
        # with crop the last character "&" in request, otherwise the signature will be incorrect
        if get:
            verb = 'GET'

        else:
            verb = 'POST'

        message = f'{verb}|{uri}|{request[:-1]}'

        if DEBUG:
            print(f'message: {message}')

        if self.secret:
            signature = hmac.new(
                # if api Secret Key not in bytes replace self.secret to
                # bytes(self.secret, encoding='utf-8'),
                self.secret,
                message.encode(),
                hashlib.sha256
            ).hexdigest()

            # now we have a signed request which can be used like url
            query = f'{self.base_url}{uri}?{request}signature={signature}'

        else:
            query = f'{self.base_url}{uri}'
        print(f'query: {query}')

        # send requests and get responses
        if get:
            response = requests.get(query)

        else:
            response = requests.post(query)

        return response.json()


if __name__ == '__main__':
    # 6000 requests/keypair/5 minutes, you can contact GRAVIEX if you need more.
    gex_private = GraviexAPI(
        access_key='',
        secret_key=b''
    )
    market = 'giobtc'
    currency = 'gio'
    timestamp = int(time.time() - 1000000000000) * 1000
    public_apis = [
        {'path': 'markets', 'sub_path': None, 'params': {}},
        {'path': 'markets', 'sub_path': market, 'params': {'market': market}},
        {'path': 'tickers', 'sub_path': None, 'params': {}},
        {'path': 'markets', 'sub_path': market, 'params': {'market': market}},
        {'path': 'depth', 'sub_path': None, 'params': {'market': market, 'limit': 1, 'order': None}},
        {'path': 'trades', 'sub_path': None, 'params': {'market': market, 'limit': 1, 'order_by': 'desc',
                                                        'timestamp': timestamp, 'from': timestamp, 'to': timestamp}},
        {'path': 'trades_simple', 'sub_path': None, 'params': {'market': market}},
        {'path': 'k', 'sub_path': None, 'params': {'market': market, 'limit': 1, 'period': 1, 'timestamp': timestamp}},
        {'path': 'k_with_pending_trades', 'sub_path': None, 'params': {'market': market, 'trade_id': 1, 'limit': 1,
                                                                       'period': 1, 'timestamp': timestamp}},
        {'path': 'timestamp', 'sub_path': None, 'params': {}},
        {'path': 'currency', 'sub_path': 'info', 'params': {'currency': currency}},
    ]
    for api in public_apis:
        r = gex_private.call_api(api['path'], param_path=api['sub_path'], params=api['params'])
        print(f'api: {api}:\n{r}\n')
