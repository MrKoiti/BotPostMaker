import telebot
import time
import config
from telebot import types
#----------------------------------------------------------------------------
#Bad words and warns&bans:
BlockList={'украина','украинцы','украинцев','украинские','россия','российские','россияне','россии','путинские','путин','зеленский','чвк','спецоперация','спецоперацию','спецоперации'}
BlockListType={'Лабораторная работа', 'Курсовая работа'}
BlockListSub={'Программирование', 'Математика', 'Физика', 'Проект', 'Химия'}
#----#
wFile = open("Warns.txt", "r") #хранилище варнов (id чатов)
warnList=wFile.readlines()
wFile.close()
#----#
bFile = open("Bans.txt", "r") #хранилище банов (id чатов)
BanList=bFile.readlines()
bFile.close()
#----------------------------------------------------------------------------
#Setups for messages:
StartMessage = 'Привет! Я - бот Easy Peasy! \nЯ помогу Вам разместить объявление :) \nНапишите, пожалуйста, Ваш запрос по образцу:'
MessageWithSample = '1)Тип работы \n2)Предметная область \n3)Краткое описание \n4)Ценовой диапазон \n5)Срок исполнения (День.Месяц) \n 6)Способ связи (Почта, Номер телефона, Ссылка на профиль)'
WarningMessage = '-Убедительная просьба: \n-Пожалуйста, избегайте лишней информации. Все детали Вы сможете обсудить непосредственно с исполнителем. \n-Наши исполнители ждут от Вас грамотно составленную заявку.'
InfoMessage = 'Для повторного вывода информации введите \n/start или info. \nДля составления объявления отправьте любое сообщение. \nУбедительная просьба: пользуйтесь заранее заготовленными кнопками, иначе несоблюдение правил будет караться баном.'
#----------------------------------------------------------------------------
#Bot&Channel config:
id_channel = '@MEasyPeasy'
bot = telebot.TeleBot(config.token)
#----------------------------------------------------------------------------
#Order
new_message = ''
step = 1
spisok=[]
indexes=[]
#----------------------------------------------------------------------------
#Setups for functions:
def StartDialog(message): #function of start dialogs
    time.sleep(1)
    bot.send_message(message.chat.id, StartMessage)
    time.sleep(1)
    bot.send_message(message.chat.id, MessageWithSample)
    time.sleep(1)
    bot.send_message(message.chat.id, WarningMessage)
    time.sleep(1)
    bot.send_message(message.chat.id, InfoMessage)
    b = [message.chat.id, 1, ""]
    n = 0
    for i in range (len(spisok)):
        if spisok[i][0] == message.chat.id:
            spisok[i] = b
            indexes[i] = message.chat.id
            n = 1
            break
    if n == 0:
        spisok.append(b)
        indexes.append(message.chat.id)
    return spisok

def BlockFunc(chatId):
    if ((chatId) in warnList) or ((str(chatId)+'\n') in warnList):
        BanList.append(chatId)
        bot.send_message(chatId, 'Ваш аккаунт заблокирован!')
        bFile = open("Bans.txt", "a")
        bFile.write('\n'+str(chatId))
        bFile.close()
    else:
        warnList.append(chatId)
        bot.send_message(chatId, '-Ваше объявление содержит слова(высказывания), несущие в себе оскорбление, или(и) относящиеся к политике. \n-Вами было получено предупреждение. \n-При повторении инцидента ваш аккаунт будет заблокирован в нашем сообществе!')
        wFile = open("Warns.txt", "a")
        wFile.write('\n'+str(chatId))
        wFile.close()

def CheckingStep(message, spisok):
    if spisok[indexes.index(message.chat.id)][1] == 3:
        k=0
        for werb in BlockListSub:
            if werb in message.text:
                k+=1
        if k==0:
            terms -= 100
            BlockFunc(ChatId)

    elif spisok[indexes.index(message.chat.id)][1] == 2:
        k=0
        for werb in BlockListType:
            if werb in message.text:
                k+=1
        if k==0:
            terms -= 100
            BlockFunc(ChatId)

def CheckingPost(message): #function of checking terms
    ChatId=message.chat.id
    terms = 0
    #----------#
    if len(message.text)>60: terms+=1
    else:
        bot.send_message(message.chat.id, 'Извините, Ваше объявление слишком короткое! \nПожалуйста, попробуйте еще раз!')
    if len(message.text)>750:
        bot.send_message(message.chat.id, 'Извините, Ваше объявление слишком длинное! \nИзбегайте лишних деталей. \nПожалуйста, попробуйте еще раз!')
        terms-=1
    #----------#
    for werb in BlockList:
        if werb in message.text.strip('\n').lower():
            terms-=100
            BlockFunc(ChatId)
            break
    #----------#


    if terms>0:
        PostingInGroup(message, ChatId)

def PostingInGroup(message, chatId):
    keyboard = types.ReplyKeyboardRemove()
    bot.send_message(id_channel, 'Объявление: \n'+message.text)
    bot.send_message(chatId,'Ваше объявление размещено! \nСкоро с Вами свяжутся исполнители. \nУдачного Вам дня! :)', reply_markup=keyboard)



def MakingNewOrder_step1(message, spisok):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Лабораторная работа")
    item2 = types.KeyboardButton("Курсовая работа")
    markup.add(item1, item2)
    bot.send_message(message.chat.id, text="Укажите тип работы: ".format(message.from_user), reply_markup=markup)
    spisok[indexes.index(message.chat.id)][1] = 2
    return spisok


def MakingNewOrder_step2(message, spisok):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Программирование")
    item2 = types.KeyboardButton("Математика")
    item3 = types.KeyboardButton("Физика")
    item4 = types.KeyboardButton("Химия")
    item5 = types.KeyboardButton("Проект")
    markup.add(item1, item2, item3, item4, item5)
    bot.send_message(message.chat.id, text="Укажите предметную область: ".format(message.from_user), reply_markup=markup)
    spisok[indexes.index(message.chat.id)][1] = 3
    spisok[indexes.index(message.chat.id)][2] += '1) ' + str(message.text) + '\n'
    return spisok


def MakingNewOrder_step3(message, spisok):
    keyboard = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, 'Дайте краткое описание заданию: ', reply_markup=keyboard)
    spisok[indexes.index(message.chat.id)][1] = 4
    spisok[indexes.index(message.chat.id)][2] += '2) ' + str(message.text) + '\n'
    return spisok


def MakingNewOrder_step4(message, spisok):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("До 500 рублей")
    item2 = types.KeyboardButton("До 1000 рублей")
    item3 = types.KeyboardButton("До 2000 рублей")
    item4 = types.KeyboardButton("До 4000 рублей")
    item5 = types.KeyboardButton("До 5000 рублей")
    item6 = types.KeyboardButton("От 5000 рублей")
    markup.add(item1, item2, item3, item4, item5, item6)
    bot.send_message(message.chat.id, text="Укажите ценовой диапазон: ".format(message.from_user), reply_markup=markup)
    spisok[indexes.index(message.chat.id)][1] = 5
    spisok[indexes.index(message.chat.id)][2] += '3) ' + str(message.text) + '\n'
    return spisok


def MakingNewOrder_step5(message, spisok):
    keyboard = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, text="Укажите дедлайн (в формате дд.мм): ", reply_markup=keyboard)
    spisok[indexes.index(message.chat.id)][1] = 6
    spisok[indexes.index(message.chat.id)][2] += '4) ' + str(message.text) + '\n'
    return spisok


def MakingNewOrder_step6(message, spisok):
    bot.send_message(message.chat.id, text="Укажите как с Вами связаться: ")
    spisok[indexes.index(message.chat.id)][1] = 7
    spisok[indexes.index(message.chat.id)][2] += '5) ' + str(message.text) + '\n'
    return spisok


def MakingNewOrder_step7(message, spisok):
    spisok[indexes.index(message.chat.id)][1] = 8
    spisok[indexes.index(message.chat.id)][2] += '6) ' + str(message.text) + '\n'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton(spisok[indexes.index(message.chat.id)][2])
    markup.add(item1)
    bot.send_message(message.chat.id, text="Отправить заказ?".format(message.from_user, bot.get_me()), parse_mode = 'html', reply_markup = markup)
    return spisok

def MakingNewOrder_step8(message, spisok):
    CheckingPost(message)
    spisok[indexes.index(message.chat.id)][1] = 1
    spisok[indexes.index(message.chat.id)][2] = ''
#----------------------------------------------------------------------------
#Bot start working:
@bot.message_handler(content_types=["text"])
def commands(message):
    if (message.chat.id in BanList) or ((str(message.chat.id)+'\n') in BanList):
        bot.send_message(message.chat.id, 'Ваш акканут заблокирован. \nВам стоит вести себя этичнее, когда вы используете сеть Интернет!')
    else:
        if (message.text == '/start') or (message.text.strip('\n').lower() == 'info') or (message.text == 'Info'):
            StartDialog(message)
        else:
            if spisok[indexes.index(message.chat.id)][1] == 1:
                MakingNewOrder_step1(message, spisok)
            elif spisok[indexes.index(message.chat.id)][1] == 2:
                MakingNewOrder_step2(message, spisok)
            elif spisok[indexes.index(message.chat.id)][1] == 3:
                MakingNewOrder_step3(message, spisok)
            elif spisok[indexes.index(message.chat.id)][1] == 4:
                MakingNewOrder_step4(message, spisok)
            elif spisok[indexes.index(message.chat.id)][1] == 5:
                MakingNewOrder_step5(message, spisok)
            elif spisok[indexes.index(message.chat.id)][1] == 6:
                MakingNewOrder_step6(message, spisok)
            elif spisok[indexes.index(message.chat.id)][1] == 7:
                MakingNewOrder_step7(message, spisok)
            elif spisok[indexes.index(message.chat.id)][1] == 8:
                MakingNewOrder_step8(message, spisok)

#----------------------------------------------------------------------------
#BotDontDie:
bot.infinity_polling(timeout=10, long_polling_timeout = 5)