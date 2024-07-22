import backtrader as bt
import requests
import json
from tabulate import tabulate
import datetime

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
        while True:
            try:
                response = self.session.get(self.p.url)
                if response.status_code != 200:
                    raise Exception("Failed to fetch data")
                data_list = json.loads(response.text)
                if not data_list or data_list == self.last_data:  # Проверяем, изменились ли данные
                    break  # Выходим из цикла, если данные не изменились или отсутствуют
                self.last_data = data_list  # Обновляем последние полученные данные

                for data in data_list:
                    date_str = data[1]
                    try:
                        date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
                        self.lines.datetime[0] = bt.date2num(date_obj)
                    except ValueError:
                        print(f"Invalid date format: {date_str}")
                        continue
                    
                    self.lines.open[0] = data[6]
                    self.lines.high[0] = data[8]
                    self.lines.low[0] = data[7]
                    self.lines.close[0] = data[11]
                    self.lines.volume[0] = data[12]



                    table_data = [[self.lines.datetime[0], self.lines.open[0], self.lines.high[0],
                                   self.lines.low[0], self.lines.close[0], self.lines.volume[0]]]
                    print(tabulate(table_data, headers=['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume']))

                return True
            except Exception as e:
                print(f"Error loading data: {e}")
                return False

cerebro = bt.Cerebro()
data = JsonDataStream(url='http://localhost:24300/iss/history/engines/stock/markets/shares/boards/TQBR/securities/sber?from=2024-01-01&till=2024-07-20')
cerebro.adddata(data)

# Добавьте здесь свою торговую стратегию
# cerebro.addstrategy(YourStrategy)

cerebro.run()