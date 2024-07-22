from datetime import datetime  # Работаем с датой и временем
import backtrader as bt


if __name__ == '__main__':  # Точка входа при запуске этого скрипта
    cerebro = bt.Cerebro()  # Инициируем "движок" BackTrader
    data = bt.feeds.GenericCSVData(  # Можно принимать любые CSV файлы с разделителем десятичных знаков в виде точки https://backtrader.com/docu/datafeed-develop-csv/
        dataname='D:\Projects\Backtrader_first\downloads_frame.csv',  # Файл для импорта
        separator=',',  # Колонки разделены табуляцией
        dtformat='%Y-%m-%d',  # Формат даты/времени DD.MM.YYYY HH:MI
        openinterest=-1)  # Открытого интереса в файле нет
        #fromdate=datetime(2024, 7, 1),  # Начальная дата приема исторических данных (Входит)
        #todate=datetime(2024, 7, 11))  # Конечная дата приема исторических данных (Не входит)
    cerebro.adddata(data)  # Привязываем исторические данные
    cerebro.broker.setcash(1000000)  # Стартовый капитал для "бумажной" торговли
    #print(f'Старовый капитал: {cerebro.broker.getvalue():.2f}')
    cerebro.run()  # Запуск торговой системы. Пока ее у нас нет
    #print(f'Конечный капитал: {cerebro.broker.getvalue():.2f}')
    cerebro.plot()  # Рисуем график. Требуется matplotlib версии 3.2.2 (pip install matplotlib==3.2.2)