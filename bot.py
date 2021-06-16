import telebot,requests,sys
from bs4 import BeautifulSoup
from telebot import types

Token='1839553097:AAFQs_g_R4HK6IOJzFIJUetzAyuLxGiTgRQ'
bot=telebot.TeleBot(Token)

mm = types.ReplyKeyboardMarkup(row_width=3)
ss = types.ReplyKeyboardMarkup(row_width=1)

button1 = types.KeyboardButton(" milf")
button2 = types.KeyboardButton(" lolita_channel")
button3 = types.KeyboardButton(" small_breasts")
button4 = types.KeyboardButton(" big_breasts") 
button5 = types.KeyboardButton(" small_ass") 
button6 = types.KeyboardButton(" big_ass") 
button7 = types.KeyboardButton(" /send") 


mm.add(button1,button2,button3,button4,button5,button6)
ss.add(button7)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id,f'''Привет братик!
Что ты хочешь?''', reply_markup=ss)

@bot.message_handler(commands=['send'])
def main(message):
    global page
    msg = bot.send_message(message.chat.id, 'Что тебя интересует?)', reply_markup=mm)
    bot.register_next_step_handler(msg,tags_call)

def tags_call(message):
    global name
    name = message.text
    page = bot.send_message(message.chat.id, 'Сколько страниц тебе надо?))')
    bot.register_next_step_handler(page, page_call)
    print(name)

def page_call(message):
    global name
    page=message.text
    print(page)
    urls = step1(name, page)  # Получаем первые ссылки из поиска
    for item in urls:
        respoce = requests.get(item)
        soup = BeautifulSoup(respoce.content, 'html.parser')
        imgs = soup.find('img', {'id': 'image'})
        vid = soup.find('source')
        try:
            a = imgs.get('src')
        except:
            try:
                a = vid.get('src')
            except:
                pass
        print(a)
        
        try:
            if ('jpeg' in a) or ('jpg' in a) or ('png' in a):
                bot.send_photo(message.chat.id, a)
            elif ('mp4' in a):
                bot.send_video(message.chat.id, a)
            bot.send_document(message.chat.id, a)
        except:
            pass

def step1(link,page):
    URLS = []
    tags = link.split()
    tagsS=''
    for i in tags:
        tagsS+= i + '+'
    urls='https://rule34.xxx/index.php?page=post&s=list&tags=-futanari'+tagsS
    for i in range(int(page)):
        url = urls + '&pid=' + str(i * 42)
        responce = requests.get(url)
        soup = BeautifulSoup(responce.content, 'html.parser')
        preview = soup.findAll('span', 'thumb') #Что нужно искать
        for photo in preview:
            URLS.append('https://rule34.xxx/' + photo.find('a').get('href')) # Сами ссылки
    return URLS

if __name__ == '__main__':
    bot.enable_save_next_step_handlers(delay=2)
    bot.load_next_step_handlers()
    bot.infinity_polling()
