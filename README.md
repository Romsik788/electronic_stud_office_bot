# Electronic Student Office Bot

Бот для [електронної системи](https://github.com/Romsik788/electronic_stud_office) оцінювання студентів.

## Встановлення

Необхідно інсталювати Python 3.10 або вище. Дана система використовує залежності pyTelegramBotAPI, bcrypt, aiogram та mysql-connector-python, тому їх необхідно встановити якщо вони не встановлені до цього.

```bash
pip install pyTelegramBotAPI bcrypt aiogram mysql-connector-python
```
Тепер необхідно встановити сам бот, якщо встановлений git то можна командою
```bash
git clone https://github.com/Romsik788/electronic_stud_office_bot
```
Або архів за [посиланням](https://github.com/Romsik788/electronic_stud_office_bot/archive/refs/heads/main.zip) який потім необхідно розпакувати
## Використання

Перед запуском бота, необхідно зробити наступне:

1. Імпортувати файл бази даних **telegram_bot.sql** на сервер MySQL. Також на сервері має бути база даних електронної системи. Рекомендуємо використовувати MySQL 8.0 та вище. В якості сервера можна використовувати [OpenServer](https://ospanel.io/).

2. Тепер необхідно вказати шлях до бази даних бота, та електронної системи. Для цього необхідно знайти методи **query_to_bot_database** та **queryToDB** та знайти в них певні параметри (для прикладу візьмемо **query_to_bot_database**)
```python
with connect(
    host="localhost",
    user="root",
    password="",
    database="telegram_bot",
)
```
Дані поля необхідні для доступу до БД, і їх необхідно змінити під ваші налаштування.

**host** - Адреса вашого MySQL сервера.

**user** та **password** - ім'я та пароль користувача. Тут потрібно вказати ім'я та пароль користувача, який матиме доступ на вашому MySQL сервері до бази даних *telegram_bot*

**database** - Назва бази даних.

3. Змінити в полі **token** на власний токен

Тепер можна запустити бота
```bash
python bot.py
```
## Внесок
Запити на виправлення вітаються. Для серйозних змін, будь ласка, спочатку відкрийте питання, щоб обговорити, що ви хочете змінити.

## Ліцензія
[MIT](https://choosealicense.com/licenses/mit/)
