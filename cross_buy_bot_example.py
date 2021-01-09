import time

from graviex_publc_api import GraviexPublicAPI
from graviex_private_api import GraviexPrivateAPI

gex_public = GraviexPublicAPI()
gex_private = GraviexPrivateAPI(
    access_key='',
    secret_key=b''
)

PAIR = 'giodoge'
# Начинаем скупать монету по самой низкой доступной цене до нужного колличества
MIN_BASE = 10000.0
# Покупать будем частями пока не выкупим необходимое кол-во
ORDER_SIZE = 100

# Получаем информацию по паре
market_info = gex_public.markets(PAIR)
# print(market_info)
# Выделяем базовую и котируемую валюты
pair_info = market_info['attributes']
base_curr = pair_info['base_unit']
quote_curr = pair_info['quote_unit']
pair_curr = base_curr, quote_curr

while True:
    # Узнаем края стаканов
    ticker = gex_public.tickers(PAIR)
    # print(ticker)
    ask = float(ticker['sell'])
    bid = float(ticker['buy'])
    print(f'Pair: {PAIR}\nBID: {bid}\tASK: {ask}')

    # Узнаем максимальную цену покупки
    base_btc = gex_public.tickers(base_curr + 'btc')
    quote_btc = gex_public.tickers(quote_curr + 'btc')
    base_sellers = float(base_btc['sell'])
    quote_sellers = float(quote_btc['sell'])
    max_buy_price = round(base_sellers / quote_sellers, 8)
    print(f'Max buy price:\n{max_buy_price}')

    # Нужно проверить наличие открытых ордеров
    order = gex_private.get_orders(market=PAIR, limit=1)
    # print(f'Last order:\n{orders}')
    time.sleep(1)

    if order:

        # Если ордер выше/равен максимальной цены закупки
        if max_buy_price >= float(order[0]['price']):

            # Если ордер по краю стакана, курим
            if bid == float(order[0]['price']):
                print('Wait...')

        # Снимаем все ордера на покупку для коррекции
        else:
            gex_private.post_orders_clear(side='buy')
            print('Clear order')
            time.sleep(1)

    # Нужно выставить ордер
    else:

        # Получаем баланс по валютам из пары
        profile = gex_private.get_members_me()
        time.sleep(1)
        # print(profile)

        balance = profile['accounts_filtered']
        # print(balance)
        pair_balance = []
        for unit in balance:
            for curr in pair_curr:
                if unit['currency'] == curr:
                    pair_balance.append(dict(currency=unit['currency'], balance=unit['balance']))
        print(f'Pair balance:\n{pair_balance}')

        # Узнаем сколько у нас базовй валюты
        base_balance = []
        for info in pair_balance:
            if info['currency'] == base_curr:
                base_balance.append(info['balance'])
        print(f'Base balance:\n{base_balance}')

        # Если базовой валюты на балансе меньше нужного кол-ва
        if float(base_balance[0]) <= MIN_BASE:

            # Выкупаем ордер по выгодной цене
            if ask <= max_buy_price:
                gex_private.post_orders(PAIR, 'buy', str(MIN_BASE), str(ask))
                print(f'Выкупаем ордер по ASK: {ask}')

            # Ставим ордер на покупку по BID ниже либо равную максимальной закупочной цены
            else:
                if bid <= max_buy_price:
                    gex_private.post_orders(PAIR, 'buy', str(ORDER_SIZE), str(bid))
                    print(f'Новый ордер по BID: {bid} {PAIR}')

        # Снимаем все ордера и выходим (при желании прикурчиваем отправку сообщения в телеграм)
        else:
            gex_private.post_orders_clear(side='buy')
            print('Done')
            quit()

    print('-'*15)
    time.sleep(60)
