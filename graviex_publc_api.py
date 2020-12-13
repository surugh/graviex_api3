import requests

'''
All private API requires 3 authentication parameters and zero or more API specific parameters.
    access_key  Your access key.
    tonce       tonce is a timestamp in integer, stands for milliseconds elapsed since Unix epoch.
                Tonce must be within 30 seconds of server's current time. Each tonce can only be used once.
    signature   Signature of the API request, generated by you, use your secret key.

if it useful you can make a donation
GIO: GQksGKKU6PotrByC8hQzBRwMAN7FuMNugF
DOGE: D8Hy4stikB4Pk8rnSfhQxgdZ59GqmasdPj
ETH: 0x290fE67efA690AE7924DB416d4239daC9c309b97
'''


class GraviexPublicAPI:
    def __init__(self):
        self.base_url = "https://graviex.net/"
        self.uri_main = "/webapi/v3/"

    def call_api(self, path, sub_path=None, params=None):

        if sub_path:
            uri = f'{self.uri_main}{path}/{sub_path}'

        else:
            uri = f'{self.uri_main}{path}'

        if params:
            params_keys = list(params.keys())
            params_keys.sort()
            params_sorted = ''
            for key in params_keys:
                value = params[key]
                if value:
                    params_sorted += f'{key}={value}&'
            url = f'{self.base_url}{uri}?{params_sorted}'

        else:
            url = f'{self.base_url}{uri}'

        r = requests.get(url)

        return r.json()

    def markets(self, market=None):
        return self.call_api('markets', sub_path=market)

    def tickers(self, market=None):
        return self.call_api('tickers', sub_path=market)

    def depth(self, market, limit=None, order=None):
        return self.call_api('depth', params=dict(market=market,
                                                  limit=limit,
                                                  order=order))

    def trades(self, market, limit=None, timestamp=None, from_id=None, to_id=None, order_by=None):
        return self.call_api('depth', params=dict(market=market,
                                                  limit=limit,
                                                  timestamp=timestamp,
                                                  from_id=from_id,
                                                  to_id=to_id,
                                                  order_by=order_by))

    def trades_simple(self, market):
        return self.call_api('trades_simple', params=dict(market=market))

    def k(self, market, limit=None, period=None, timestamp=None):
        return self.call_api('k', params=dict(market=market,
                                              limit=limit,
                                              period=period,
                                              timestamp=timestamp))

    def k_with_pending_trades(self, market, trade_id, limit=None, timestamp=None):
        return self.call_api('k_with_pending_trades', params=dict(market=market,
                                                                  trade_id=trade_id,
                                                                  limit=limit,
                                                                  timestamp=timestamp))

    def timestamp(self):
        return self.call_api('timestamp')

    def currency(self, unit):
        return self.call_api('currency', sub_path='info', params=dict(currency=unit))


if __name__ == '__main__':
    # подключаемся
    gex_public = GraviexPublicAPI()
    # получаем все пары
    markets = gex_public.markets()
    print(markets)
    # пара
    market_id = 'giobtc'
    # информация по паре
    market_info = gex_public.markets(market_id)
    print(market_info)
    # получаем все тикеры
    tickers = gex_public.tickers()
    print(tickers)
    # тикер по паре
    ticker_pair = gex_public.tickers(market_id)
    print(ticker_pair)
    # глубина по паре
    depth = gex_public.depth(market_id)
    print(depth)
    # сделки по паре
    trade = gex_public.trades(market_id)
    print(trade)
    # сделки с минимальными свойствами
    trade_simple = gex_public.trades_simple(market_id)
    print(trade_simple)
    # OHLC (K line) по паре
    k_line = gex_public.k(market_id)
    print(k_line)
    # Получите K данных с отложенными сделками, которые еще не включены в K данных,
    # потому что существует задержка между сделкой, сгенерированной и обработанной генератором данных K
    k_with_pending_trades = gex_public.k_with_pending_trades(market_id, 1)
    print(k_with_pending_trades)
    # timestamp сервера
    timestamp = gex_public.timestamp()
    print(timestamp)
    # информация по валюте
    currency = 'gio'
    currency_info = gex_public.currency(currency)
    print(currency_info)
