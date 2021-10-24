import telebot,requests
from bs4 import BeautifulSoup

Token=''
bot=telebot.TeleBot(Token)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id,f'''Приветствую тебя {message.chat.username}!
Отправь мне команду для выполнения.''')

@bot.message_handler(commands=['send'])
def main(message):
    global page
    msg = bot.send_message(message.chat.id, 'Отправь мне теги')
    bot.register_next_step_handler(msg,tags_call)

def tags_call(message):
    global name
    name = message.text
    page = bot.send_message(message.chat.id, 'Отправь мне pages')
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
        imgs = soup.find('div', {'class': 'link-list'})
        imgs = imgs.findAll('a')
        imgs = imgs[2]
        vid = soup.find('source')

        try:
            a = imgs.get('href')
        except:
            try:
                a = vid.get('src')
            except:
                pass

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
    urls='https://rule34.xxx/index.php?page=post&s=list&tags='+tagsS
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