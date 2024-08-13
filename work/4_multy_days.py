import backtrader as bt
import requests
import json
import pandas as pd

class JsonDataStream(bt.feed.DataBase):
    params = (
        ('url', ''),
    )

    def __init__(self):
        super(JsonDataStream, self).__init__()
        self.session = requests.Session()
        self.last_data = None  # Хранение последних полученных данных

    def _load(self):
        try:
            response = self.session.get(self.p.url)
            if response.status_code != 200:
                raise Exception("Failed to fetch data")
            data_list = json.loads(response.text)
            df = pd.DataFrame(data_list,columns=['board_id','trade_date','short_name','sec_id','num_trades','value','open','low','high','legal_close_price',
                                                 'wa_price','close','volume','market_price2','market_price3','admin_ted_quote','mp2valtrd','market_price3_trades_value',
                                                 'admitted_value','waval','trading_session','currency_id','trendclspr'])
            df = df[['trade_date','open','high','low','close','volume']]
            url_part = self.p.url.split('/')[-1].split('?')[0]
            df['ticker'] = url_part
            df.to_csv('downloads_frame.csv', mode='a', header=False)  # используем mode='a' для добавления данных в файл без перезаписи
            #print(df)

        except Exception as e:
            print(f"Error loading data: {e}")
            return False

cerebro = bt.Cerebro()

# Список тикеров для обработки
tickers = ['RNFT', 'AFLT', 'POLY', 'VTBR', 'PLZL', 'SBERP', 'TRNFP', 'CHMF', 
           'LNTA', 'PHOR', 'MTSS', 'NVTK', 'FEES', 'SNGS', 'PIKK', 'MVID', 
           'RTKM', 'LSRG', 'AFKS', 'GMKN', 'IRAO', 'LKOH', 'TATN', 'SBER', 
           'RUAL', 'SNGSP', 'TATNP', 'CBOM', 'NLMK', 'GAZP', 'MOEX']

# Базовый URL для запроса данных
base_url = 'http://localhost:24300/iss/history/engines/stock/markets/shares/boards/TQBR/securities/'

for ticker in tickers:
    # Формирование полного URL с текущим тикером
    url = base_url + f'{ticker}?from=2024-01-01&till=2024-07-31'
    
    # Создание экземпляра JsonDataStream с текущим URL и добавление его в cerebro
    data = JsonDataStream(url=url)
    cerebro.adddata(data)

cerebro.run()
