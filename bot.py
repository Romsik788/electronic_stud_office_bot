import telebot
import bcrypt

from aiogram import types
from getpass import getpass
from mysql.connector import ERROR_NO_CEXT, connect, Error

token = "2109429431:AAFkUumRJNvtdwTUudjjoVSdY-1VqewbB6s"
bot = telebot.TeleBot(token, parse_mode=None)

stud = str
id = int
auth = False
login = str

def query_to_bot_database(query, commit = False):
    try:
        with connect(
            host="localhost",
            user="root",
            password="",
            database="telegram_bot",
        ) as connection:
            try:
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    if commit:
                        connection.commit()
                    else:
                        result = cursor.fetchall()
            except Error as e:
                print("Помилка у виконанні запиту -", e)
    except Error as e:
        print(e)
    if commit == False: return result

def check_user(message):
    global auth, id, stud
    if auth == False:
        get_id_query = "SELECT `chat_id`, `user_id` FROM `data` WHERE chat_id=%s"
        get_id_res = query_to_bot_database(get_id_query % int(message.chat.id))
        try:
            if get_id_res[0][0] == message.chat.id:
                auth = True
                id = get_id_res[0][1]
                select_student_query = "SELECT * FROM student WHERE id=%s"
                stud = queryToDB(select_student_query % id)
        except:
            pass


def queryToDB(query):
    try:
        with connect(
            host="localhost",
            user="root",
            password="",
            database="electronic_student_office",
        ) as connection:
            try:
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    result = cursor.fetchall()
            except Error as e:
                print("Помилка у виконанні запиту -", e)
    except Error as e:
        print(e)
    return result

def main_menu(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_appraisals = types.KeyboardButton(text="Оцінки☑️")
    button_studinfo = types.KeyboardButton(text="Інформація про студента👨‍🎓")
    keyboard.add(button_appraisals, button_studinfo)
    bot.send_message(chat_id=message.chat.id, text="Вітаю в системі, %s🙋" % stud[0][1], reply_markup = [keyboard])

def auth_phone_method(message):
    global id
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button_phone = types.KeyboardButton(text="Відправити номер📞", request_contact=True)
    keyboard.add(button_phone)
    bot.send_message(chat_id=message.chat.id, text="Відправте свої контактні дані📱", reply_markup = [keyboard])

def auth_finall(message):
    global login, id, auth
    passwd = message.text
    login_query = "SELECT `username` FROM `auth_user` WHERE id=%s"
    passwd_query = "SELECT `password` FROM `auth_user` WHERE id=%s"
    _login = queryToDB(login_query % stud[0][5])
    _pswd = queryToDB(passwd_query % stud[0][5])
    pswd = _pswd[0][0].replace("bcrypt$", "", 1)
    if not(_login[0][0] == login and bcrypt.checkpw(bytes(passwd, encoding='utf8'), bytes(pswd, encoding='utf8'))): 
        bot.send_message(chat_id=message.chat.id, text="Логін або пароль неправильний, спробуйте ще раз")
        auth_message(message)
    else:
        auth = True
        add_to_db_query = "INSERT INTO `data` (`id`, `chat_id`, `user_id`) VALUES (NULL, '%s', '%s')" % (int(message.chat.id), int(id))
        query_to_bot_database(add_to_db_query, commit=True)
        main_menu(message)

def auth_passwd(message):
    global login
    login = message.text
    bot.send_message(chat_id=message.chat.id, text="Введіть пароль")
    bot.register_next_step_handler(message, auth_finall)

def auth_login(message):
    bot.send_message(chat_id=message.chat.id, text="Введіть логін")
    bot.register_next_step_handler(message, auth_passwd)

def auth_message(message):
    _message = "Оберіть зручний метод підтвердження входу👊"
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button_phone = types.KeyboardButton(text="За номером телефону🤳")
    button_login_passwd = types.KeyboardButton(text="За логіном і паролем✏️")
    keyboard.add(button_phone)
    keyboard.add(button_login_passwd)
    bot.send_message(chat_id=message.chat.id, text=_message, reply_markup = [keyboard])

def set_id_message(message):
    text = message.text
    try:
        global id, stud
        try:
            id = int(text)
        except:
            bot.send_message(chat_id=message.chat.id, text="Некоректний ввід, спробуйте ще раз👀")
            bot.register_next_step_handler(message, set_id_message)
            return
        select_student_query = "SELECT * FROM student WHERE id=%s"
        stud = queryToDB(select_student_query % id)
        if len(stud) == 0: 
            bot.send_message(chat_id=message.chat.id, text="Студента не знайдено, спробуй ще раз🤚")
            bot.register_next_step_handler(message, set_id_message)
            return
        auth_message(message)
    except Error as e:
        bot.send_message(chat_id=message.chat.id, text=e)

@bot.message_handler(commands=['start'])
def on_start(message):
    check_user(message)
    if auth:
        main_menu(message)
        return
    bot.send_message(chat_id=message.chat.id, text="Привіт👋, мене звати Electronic Student Office Bot🤖, завдяки мені, можна зручно переглядати свої оцінки в електронному кабінеті🖥. Для перегляду оцінок необхідно авторизуватися. Для початку введіть свій ID", reply_markup = None)
    bot.register_next_step_handler(message, set_id_message)

@bot.message_handler(commands=['appraisals'])
def get_stud_appraisals(message):
    check_user(message)
    global auth
    if auth == False: 
        bot.send_message(chat_id=message.chat.id, text="Ви не авторизувалися🤷")
        return
    global id, stud
    try:
        subject_id_query = "SELECT student_subject.student_id, subject.subject_name, student_subject.subject_id FROM student_subject, subject WHERE student_subject.student_id=%s AND subject.id = student_subject.subject_id"
        appraisals_query = "SELECT * FROM `appraisals` WHERE subject_id IN (SELECT `id` FROM `subject` WHERE student_id=%s)"
        subjects = queryToDB(subject_id_query % stud[0][0])
        appraisals = queryToDB(appraisals_query % stud[0][0])
        _message = ""
        for i in range(len(subjects)):
            _message += "Предмет - " + subjects[i][1] + '\n'
            for y in range(len(appraisals)):
                if appraisals[y][4] != subjects[i][2]: continue
                _message += "За - " + str(appraisals[y][1]) + '\n' + "Оцінка - " + str(appraisals[y][2]) + '\n' + "Дата - " + str(appraisals[y][3].strftime('%Y-%m-%d') + '\n')
        bot.send_message(chat_id=message.chat.id, text=_message)
    except Error as e:
        bot.send_message(chat_id=message.chat.id, text="Невідома помилка - %s" % e)

@bot.message_handler(commands=['studinfo'])
def get_stud_info(message):
    check_user(message)
    global auth
    if auth == False: 
        bot.send_message(chat_id=message.chat.id, text="Ви не авторизувалися🤷")
        return
    global id, stud
    try:
        if stud[0][3]: status = "Бюджет"
        else: status = "Контракт"
        group_info = "SELECT `group_name` FROM `groups` WHERE id=%s"
        _message = "Інформація про студента\n" + "ID: " + str(stud[0][0]) + '\n' + "ФІО: " + stud[0][1] + '\n' + "Курс: " + str(stud[0][2]) + '\n' + "Джерело фінансування: " + status + '\n' + "Група: " + queryToDB(group_info % stud[0][4])[0][0]
        bot.send_message(chat_id=message.chat.id, text=_message)
    except Error as e:
        bot.send_message(chat_id=message.chat.id, text="Невідома помилка - %s" % e)

@bot.message_handler(content_types=["text"])
def check_text_message(message):
    text = message.text
    if text == "Оцінки☑️": get_stud_appraisals(message)
    if text == "Інформація про студента👨‍🎓": get_stud_info(message)
    if text == "За номером телефону🤳":
        if auth == False:
            auth_phone_method(message)
    if text == "За логіном і паролем✏️":
        if auth == False:
            auth_login(message)

@bot.message_handler(content_types=["contact"])
def get_contact(message):
    global auth, id
    if stud[0][6] == message.contact.phone_number or stud[0][6].replace('+', '', 1) == message.contact.phone_number:
        auth = True
        add_to_db_query = "INSERT INTO `data` (`id`, `chat_id`, `user_id`) VALUES (NULL, '%d', '%d')" % (int(message.chat.id), int(id))
        query_to_bot_database(add_to_db_query, commit=True)
        main_menu(message)
    else: 
        bot.send_message(chat_id=message.chat.id, text="Даного номеру телефону не знайдено, спробуйте увійти іншим способом")
        auth_message(message)
bot.polling(none_stop=True, interval=0)