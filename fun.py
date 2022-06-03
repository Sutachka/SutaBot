# ======================================= Развлечения
import requests
import bs4  # BeautifulSoup4
from telebot import types
from io import BytesIO
import json

# -----------------------------------------------------------------------
def get_text_messages(bot, cur_user, message):
    chat_id = message.chat.id
    ms_text = message.text

    if ms_text == "Пёсики":
        bot.send_photo(chat_id, photo=get_dogURL(), caption="Вот тебе пёсель!")

    elif ms_text == "Лисята":
        bot.send_photo(chat_id, photo=get_foxURL(), caption="Вот тебе лисёнок!")

    elif ms_text == "Приколдесы":
        bot.send_message(chat_id, text=get_anekdot())

    elif ms_text == "Прислать фильм":
        send_film(bot, chat_id)

    elif ms_text == "Курс биткоина":
        bot.send_message(chat_id, text=get_bitcoin())

    elif ms_text == "Фактик":
        bot.send_message(chat_id, text=get_fact())


# -----------------------------------------------------------------------
def get_anekdot():
    from random import randint
    import bs4
    array = []
    anek = requests.get("http://anekdotme.ru/anekdot/random")
    soup = bs4.BeautifulSoup(anek.text, "html.parser")
    result = soup.select(".anekdot_text")
    for finalResult in result:
        array.append(finalResult.getText().strip())
    return array[0]


#------------------------------------------------------------------------
def get_bitcoin():
    contents = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json').json()
    date = contents['time']['updateduk']
    cost = contents['bpi']['EUR']['rate']
    return 'Сегодня, ' + date + ' по Британскому времени' + '\n' + 'курс биткоина: ' + cost + ' евро'


#----------------------------------------------------------------------------
def get_fact():
    array_anekdots = []
    req_anek = requests.get('https://randstuff.ru/fact/random')
    if req_anek.status_code == 200:
        soup = bs4.BeautifulSoup(req_anek.text, "html.parser")
        result_find = soup.select('table', class_='text')
        for result in result_find:
            array_anekdots.append(result.getText().strip())
    if len(array_anekdots) > 0:
        return array_anekdots[0]
    else:
        return ""


# -----------------------------------------------------------------------
def get_foxURL():
    url = ""
    req = requests.get('https://randomfox.ca/floof/')
    if req.status_code == 200:
        r_json = req.json()
        url = r_json['image']
        # url.split("/")[-1]
    return url


#------------------------------------------------------------------------
def get_dogURL():
    url = ""
    req = requests.get('https://random.dog/woof.json')
    if req.status_code == 200:
        r_json = req.json()
        url = r_json['url']
        # url.split("/")[-1]
    return url


# ----------------------------------------------------------------------
def get_randomFilm():
    url = 'https://randomfilm.ru/'
    infoFilm = {}
    req_film = requests.get(url)
    soup = bs4.BeautifulSoup(req_film.text, "html.parser")
    result_find = soup.find('div', align="center", style="width: 100%")
    infoFilm["Наименование"] = result_find.find("h2").getText()
    names = infoFilm["Наименование"].split(" / ")
    infoFilm["Наименование_rus"] = names[0].strip()
    if len(names) > 1:
        infoFilm["Наименование_eng"] = names[1].strip()

    images = []
    for img in result_find.findAll('img'):
        images.append(url + img.get('src'))
    infoFilm["Обложка_url"] = images[0]

    details = result_find.findAll('td')
    infoFilm["Год"] = details[0].contents[1].strip()
    infoFilm["Страна"] = details[1].contents[1].strip()
    infoFilm["Жанр"] = details[2].contents[1].strip()
    infoFilm["Продолжительность"] = details[3].contents[1].strip()
    infoFilm["Режиссёр"] = details[4].contents[1].strip()
    infoFilm["Актёры"] = details[5].contents[1].strip()
    infoFilm["Трейлер_url"] = url + details[6].contents[0]["href"]
    infoFilm["фильм_url"] = url + details[7].contents[0]["href"]

    return infoFilm


# -----------------------------------------------------------------------
def send_film(bot, chat_id):
    film = get_randomFilm()
    info_str = f"<b>{film['Наименование']}</b>\n" \
               f"Год: {film['Год']}\n" \
               f"Страна: {film['Страна']}\n" \
               f"Жанр: {film['Жанр']}\n" \
               f"Продолжительность: {film['Продолжительность']}"
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Трейлер", url=film["Трейлер_url"])
    btn2 = types.InlineKeyboardButton(text="СМОТРЕТЬ онлайн", url=film["фильм_url"])
    markup.add(btn1, btn2)
    bot.send_photo(chat_id, photo=film['Обложка_url'], caption=info_str, parse_mode='HTML', reply_markup=markup)