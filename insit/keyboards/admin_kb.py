from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton("/Загрузить_тариф")
b2 = KeyboardButton("/Загрузить_акцию")
b3 = KeyboardButton("/МКД")
b4 = KeyboardButton("/Частные_дома")
b5 = KeyboardButton("/Удалить_из_акций")
b6 = KeyboardButton("/Удалить_тариф")
b7 = KeyboardButton("/Назад")


button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True).row(b1, b2).add(b6, b5)
button_case_admin_choose = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(b3, b4)
button_case_admin_del_choose = ReplyKeyboardMarkup(resize_keyboard=True).row(b3, b4).add(b7)

