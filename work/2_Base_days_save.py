import backtrader as bt
import requests
import json
#from tabulate import tabulate
import datetime
import pandas as pd

class JsonDataStream(bt.feed.DataBase):
    params = (
        ('url', 'http://localhost:24300/iss/history/engines/stock/markets/shares/boards/TQBR/securities/sber?from=2024-01-01&till=2024-07-20'),
    )

    def __init__(self):
        super(JsonDataStream, self).__init__()
        self.session = requests.Session()
        self.last_data = None  # Хранение последних полученных данных

    def _load(self):
        global last_received_data  # Объявляем глобальную переменную для хранения последних полученных данных
        try:
            response = self.session.get(self.p.url)
            #data_list = json.loads(response.text)
            #df = pd.DataFrame(data_list)
            #print(df)
            if response.status_code != 200:
                raise Exception("Failed to fetch data")
            data_list = json.loads(response.text)
            df = pd.DataFrame(data_list,columns=['board_id','trade_date','short_name','sec_id','num_trades','value','open','low','high','legal_close_price',
                                                 'wa_price','close','volume','market_price2','market_price3','admin_ted_quote','mp2valtrd','market_price3_trades_value',
                                                 'admitted_value','waval','trading_session','currency_id','trendclspr'])
            df = df[['trade_date','open','high','low','close','volume']]
            df.set_index('trade_date',inplace=True)
            df.to_csv('downloads_frame.csv',index=True)
            print(df)

        except Exception as e:
            print(f"Error loading data: {e}")
            return False

cerebro = bt.Cerebro()
data = JsonDataStream(url='http://localhost:24300/iss/history/engines/stock/markets/shares/boards/TQBR/securities/sber?from=2024-01-01&till=2024-07-20')
cerebro.adddata(data)

cerebro.run()