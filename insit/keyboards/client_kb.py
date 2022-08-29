from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

b1 = KeyboardButton("/⏰Режим_работы")
b2 = KeyboardButton("/🗺Расположение")
b3 = KeyboardButton("/📋Тарифы")
b4 = KeyboardButton("/💯Скидки/Акции")
b5 = KeyboardButton("/🏬В_многоквартирных_домах")
b6 = KeyboardButton("/🏠В_частных_домах")
b7 = KeyboardButton("/↪️Вернуться")
b8 = KeyboardButton("/⏬Скачать")
b9 = KeyboardButton("/🌐Полезные_ссылки")
url1 = InlineKeyboardButton(text="Android", url="https://play.google.com/store/apps/details?id=ru.insit.insit&hl=ru&gl=US")
url2 = InlineKeyboardButton(text="IPhone", url="https://apps.apple.com/ru/app/%D0%B8%D0%BD%D1%81%D0%B8%D1%82/id1545485956")
url3 = InlineKeyboardButton(text="Официальный сайт", url="https://www.insit.ru/")
#url4 = InlineKeyboardButton(text="Невероятно важная информация", url="https://rroll.to/45yx6A")
#url5 = InlineKeyboardButton(text="Камера", url="http://mobile.insit.ru:7654/streetcam-centr-4f969eb039/embed.html")

downloadkb = InlineKeyboardMarkup(row_width=2).add(url1, url2)
usefullkb = InlineKeyboardMarkup(row_width=2).add(url3)#.add(url4).row(url5)
kb_client = ReplyKeyboardMarkup(resize_keyboard=True).row(b1, b2).row(b3, b4).row(b8, b9)
client_kb_choose_home = ReplyKeyboardMarkup(resize_keyboard=True).add(b5).add(b6).add(b7)


#kb_client.row(b1, b2).row(b3, b4).add(b8)
#client_kb_choose_home.add(b5).add(b6).add(b7)
#urlkb.add(url1, url2).insert(url3).add(url4)
