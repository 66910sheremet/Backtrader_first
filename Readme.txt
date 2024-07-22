Установка:

Классика: 

Создаем requirements.txt в папке с проектом, туда копируем зависимости из файла pyproject.toml

python>=3.9,<4
backtrader==1.9.78.123
requests==2.32.3
tabulate==0.9.0
psycopg2==2.9.9
pandas==2.2.2
matplotlib==3.9.1

далее устанавливаем зависимости:

pip install -r requirements.txt

Второй вариант установка poetry. 

Установить poetry на комп:

pip install poetry

В папке с проектом в консоли:

  poetry init

Для установки зависимостей из файла pyproject.toml:

 poetry install

