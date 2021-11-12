import telebot;
import logging;
from telebot import types as ty
import threading
# from threading import Thread, local

from bd import getIdBuNumber, reg, searchPhone, isExistsById, searchPhoneById, searchCarNumberById, deleteById

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


bot = telebot.TeleBot('2034711051:AAFzh9AnJsqxsrqA6MnmbaRp59omtJg7F3Q');

data = threading.local()

phone = threading.local()
carNumber = threading.local()
userName = threading.local()
userId = threading.local()
name = threading.local()
model = threading.local()


phone.v = 0
carNumber.v = ''
userName.v = ''
userId.v = 0
name.v = ''
model.v = ''


@bot.message_handler(commands=['start', 'registration', 'search', 'block', 'evacuation', 'del'])
def start(message):
    if message.text == '/start':
        print('New user ' + message.from_user.username)
        bot.send_message(189437726, "New user @" + str(message.from_user.username));
        bot.send_message(message.from_user.id, 
                            '/registration - регистрация в системе\n' 
                            '/search - найти данные по номеру автомобиля\n'
                            '/block - сообщите владельцу, если вы его перекрыли\n'
                            '/evacuation - сообщить, что автомобиль эвакуируют\n'
                            '/del - удалить свою машину\n'
                            'Вопросы, жалобы, предложению сюда 👉 @nikola_fp')
    elif message.text == '/help':
        bot.send_message(message.from_user.id, 
                            '/registration - регистрация в системе\n' 
                            '/search - найти данные по номеру автомобиля\n'
                            '/block - сообщите владельцу, если вы его перекрыли\n'
                            '/evacuation - сообщить, что автомобиль эвакуируют\n'
                            '/del - удалить свою машину\n'
                            'Вопросы, жалобы, предложения сюда 👉 @nikola_fp')
    elif message.text == '/registration':
        # global userName
        # global userId
        userName.v = message.from_user.username
        userId.v = message.from_user.id
        # TO DO Проверить регистрацию
        bot.send_message(message.from_user.id, "Ваш номер телефона");
        bot.register_next_step_handler(message, setPhone)
        print(logger)
    elif message.text == '/search':
        # TO DO Проверить регистрацию      
        if isExistsById(message.from_user.id):
            bot.send_message(message.from_user.id, "Номер автомобиля");
            bot.register_next_step_handler(message, getPhoneByCarNumber)
        else:
            bot.send_message(message.from_user.id, "Сначала необходимо пройти регистрацию /registration");
    elif message.text == '/block':
        # TO DO Проверить регистрацию
        bot.send_message(message.from_user.id, "Отправьте номер перекрытого автомобиля, и мы сообщим об этом владельцу");
        bot.register_next_step_handler(message, comment)
    elif message.text == '/evacuation':
        bot.send_message(message.from_user.id, "Отправьте номер автомобиля, которого собираются увезти, и мы сообщим об этом владельцу");
        bot.register_next_step_handler(message, evacuationInform)
    elif message.text == '/del':
        if isExistsById(message.from_user.id):
            keyboard = ty.InlineKeyboardMarkup(); #наша клавиатура
            for number in searchCarNumberById(message.from_user.id):
                key = ty.InlineKeyboardButton(text=number[1], callback_data='del'+str(number[0])); 
                keyboard.add(key);
            question = 'Какой автомобиль Вы хотите удалить?';
            bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
        else:
            bot.send_message(message.from_user.id, "Ваших автомобилей нет в списке");

def comment(message):
    # global carNumber
    if message.text[:1] == '/':
        start(message)
        return
        
    carNumber.v = repl(message.text.upper())
    bot.send_message(message.from_user.id, "Оставьте комментарий(время убытия, цвет машины..)");
    bot.register_next_step_handler(message, report)


def report(message):
    # global carNumber
    if message.text[:1] == '/':
        start(message)
        return

    comment = message.text
    # phone = str(searchPhoneById(message.from_user.id))
    phone = ''
    if searchPhoneById(message.from_user.id):
        for phone_i in searchPhoneById(message.from_user.id):
            phone = phone + ', ' + phone_i[0]
    phone = phone[2:]
    print(phone)
    print ('New report ')
    bot.send_message(189437726, "New report " + phone);
    
    if getIdBuNumber(carNumber.v):
        for id in getIdBuNumber(carNumber.v):
            bot.send_message(id[0], 'Вас перекрыли, но оставили все данные @' + message.from_user.username + ', телефон: ' + str(phone) + '\n'
             + 'комментарий: ' + comment);
    else:
        bot.send_message(message.from_user.id, 'К сожалению нам не удалось связаться с владельцем..(');

def evacuationInform(message):

    if message.text[:1] == '/':
        start(message)
        return

    carNumber = repl(message.text.upper())
    print ('New evacuationInform ')
    bot.send_message(189437726, "New evacuationInform ");
    
    if getIdBuNumber(carNumber):
        for id in getIdBuNumber(carNumber):
            bot.send_message(id[0], 'Ваш автомобиль с номером ' + carNumber + ', кажется, эвакуируют ;(');
    else:
        bot.send_message(message.from_user.id, 'К сожалению нам не удалось связаться с владельцем..(');

def setPhone(message): 
    # global phone;
    if message.text[:1] == '/':
        start(message)
        return

    phone.v = message.text
    # data.v = message.text
    bot.send_message(message.from_user.id, "Как Вас зовут?");
    bot.register_next_step_handler(message, setName);

def setName(message): 
    # global name;
    if message.text[:1] == '/':
        start(message)
        return

    name.v = message.text
    bot.send_message(message.from_user.id, "Номер автомобиля");
    bot.register_next_step_handler(message, setCarNumber);

def setCarNumber(message): 
    # global carNumber;
    if message.text[:1] == '/':
        start(message)
        return

    carNumber.v = repl(message.text.upper());   
    bot.send_message(message.from_user.id, "Модель автомобиля");
    bot.register_next_step_handler(message, setModel);

def setModel(message): 
    # global model;
    if message.text[:1] == '/':
        start(message)
        return

    model.v = message.text;
    # reg(userName, userId, phone, name, carNumber, model)
    setApprove(message)
    # bot.register_next_step_handler(message, get_approve);

def setApprove(message): 
    # global carNumber;
    # global phone;
    # global username;
    # global name;
    # global model;
    if message.text[:1] == '/':
        start(message)
        return

    keyboard = ty.InlineKeyboardMarkup(); #наша клавиатура
    key_yes = ty.InlineKeyboardButton(text='Да, продолжить!', callback_data='yes'); #кнопка «Да»
    keyboard.add(key_yes); #добавляем кнопку в клавиатуру
    key_no= ty.InlineKeyboardButton(text='Нет, отказаться от регистрации :(', callback_data='no');
    keyboard.add(key_no);
    question = 'Вы согласны, что Ваши данные будут храниться, обрабатываться и передаваться третьим лицам по запросу?';
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    # global carNumber;
    # global phone;
    # global username;
    # global name;
    # global model;

    if call.data == "yes": #call.data это callback_data, которую мы указали при объявлении кнопки
        reg(userName.v, userId, phone.v, name.v, carNumber.v, model.v) #код сохранения данных, или их обработки
        print('New user ' + str(call.message.chat.id))
        bot.send_message(189437726, "New ures ");
        # print('phone ' + str(phone))
        # print('data ' + str(data.v))
        bot.send_message(call.message.chat.id, 'Спасибо за регистрацию! Теперь вам доступен поиск по базе /search');
    elif call.data == "no":
        print('Rejection')
        bot.send_message(189437726, "Rejection");
        bot.send_message(call.message.chat.id, 'Send /help')
    elif call.data[:3] == 'del':
        bot.send_message(189437726, "Delete");
        deleteById(call.data[3:])
        bot.send_message(call.message.chat.id, 'Успешно!')


def getPhoneByCarNumber(message):
    if message.text[:1] == '/':
        start(message)
        return

    carNumber = repl(message.text.upper())
    print('New search by car number ' + str(carNumber))
    bot.send_message(189437726, "New search by car number " + str(carNumber));
    recordsAD = searchPhone(carNumber)

    if recordsAD:
        for phone in recordsAD:
            bot.send_message(message.from_user.id, '@' + phone[0] + ' телефон ' + phone[1] + ', марка авто ' + phone[2]);
    else:
        bot.send_message(message.from_user.id, 'Данный номер пока не зарегистрирован');
    # if recordsAD == []:
    #     bot.send_message(update.message.from_user.id, 'No result..(');
    # else:
    #     bot.send_message(update.message.from_user.id, '@' + recordsAD);

def repl(text):
    text = text.replace('У', 'Y')
    text = text.replace('К', 'K')
    text = text.replace('Е', 'E')
    text = text.replace('Н', 'H')
    text = text.replace('В', 'B')
    text = text.replace('А', 'A')
    text = text.replace('Р', 'P')
    text = text.replace('О', 'O')
    text = text.replace('С', 'C')
    text = text.replace('М', 'M')
    text = text.replace('Т', 'T')
    text = text.replace('Х', 'X')

    return text

bot.send_message(189437726, "Restarting");

bot.polling(none_stop=True, interval=0)
# 

    # bot.send_message(message.from_user.id, "Let's reg! Send /registration");
# # def start(update, context):
# #     """Send a message when the command /start is issued."""
# #     update.message.reply_text('Hi!')


# def help_command(update, context):
#     """Send a message when the command /help is issued."""
#     update.message.reply_text('Help!')


# def echo(update, context):
#     """Echo the user message."""
#     print(update.message.text)
#     update.message.reply_text(update.message.text)


# @bot.message_handler(commands=['start'])
# def start(message):
#   username = from_user.username
#   reg(username)


# # def bot_answer(update, context):
# #     answer = go_bot(update.message.text)
# #     print(question, answer)
# #     print(stats)
# #     update.message.reply_text()

# def main():
#     """Start the bot."""
#     updater = Updater("2034711051:AAFzh9AnJsqxsrqA6MnmbaRp59omtJg7F3Q", use_context=True)

#     dp = updater.dispatcher
#     dp.add_handler(CommandHandler("start", start))
#     dp.add_handler(CommandHandler("help", help_command))  
#     dp.add_handler(CommandHandler("registation", registration))
#     dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
#     print(logger)

#     # Start the Bot
#     updater.start_polling()
#     updater.idle()
#     #return

# main()