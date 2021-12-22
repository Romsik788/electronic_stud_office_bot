# Electronic Student Office Bot

This bot is used to [electronic system](https://github.com/Romsik788/electronic_stud_office) asses students.

## Installation

First of all you have to Install Python 3.9 or high version. Current system uses relations pyTelegramBotAPI, bcrypt, aiogram and mysql-connector-python, because of that you have to pre-install them if they are not already installed.

```bash
pip install pyTelegramBotAPI bcrypt aiogram mysql-connector-python
```
Now you have to Install the bot it self, if git is already installed you may use command called.
```bash
git clone https://github.com/Romsik788/electronic_stud_office_bot
```
Or you may use archive via [link](https://github.com/Romsik788/electronic_stud_office_bot/archive/refs/heads/main.zip) which you have to unpack after installation
## Usage

Before you launch bot,  you have to do next:

1. Import data base file **telegram_bot.sql** into MySQL server. Also, your server has to have your system`s database. Preferably to use MySQL 8.0 or higher. As a server we recommend to use [OpenServer](https://ospanel.io/).

2. Then you have create a path to bot’s data base, and to electronic system. To make is possible you have to find methods those like **query_to_bot_database** and **queryToDB** and find in them some specific parameters. (for example lets look at the **query_to_bot_database**)
```python
with connect(
    host="localhost",
    user="root",
    password="",
    database="telegram_bot",
)
```
These fields are used to gain an access to Data Base, and they have to be changed according to your settings.

**host** - Your MySQL servers address.

**user** and **password** - In these fields you have to mention user name and password, which is going to get an access to *telegram_bot* data base onto your MySQL server.

**database** - In this field you may claim a new name for your database.

3. Change in field **token** onto personal token

Now you are allowed to launch bot.
```bash
python bot.py
```
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
