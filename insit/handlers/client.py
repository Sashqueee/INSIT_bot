from aiogram import types, Dispatcher
from create_bot import bot
from keyboards import kb_client, client_kb_choose_home, downloadkb, usefullkb
from data_base import sqlite_db


#@dp.message_handler(commands=["start", "help"])
async def command_start(message : types.Message):
    try:
        await bot.send_message(message.from_user.id, "Здравствуйте, пожалуйста, выберете комманду ниже", reply_markup=kb_client)
        await message.delete()
    except:
        await message.reply("Общение с ботом через ЛС, напишите ему:\nt.me/Ins1t_bot")


async def insit_open_command(message : types.Message):
        await bot.send_message(message.from_user.id, "Абонентский отдел: ПН - ПТ с 9:00 до 18:00, СБ с 9:00 до 17:00, ВС - выходной.\nНомер телефона: 8(35139) 999–88\n\n"
                                                     "Техническая поддержка: круглосуточно.\nНомер телефона: 8(35139) 999–66")

async def insit_place_command(message : types.Message):
        await bot.send_message(message.from_user.id, "г. Копейск, пр. Коммунистический, д. 22")


async def insit_price_command(message : types.Message):
    await bot.send_message(message.from_user.id, "Какие тарифы вас интересуют?", reply_markup=client_kb_choose_home)

#Возврат
async def insit_back_command(message : types.Message):
    await bot.send_message(message.from_user.id, "Пожалуйста, выберите команду ниже", reply_markup=kb_client)

#Вывод данных из базы данных МКД
async def insit_mkd_command(message : types.Message):
    await sqlite_db.sql_read_mkd(message)

#Вывод данных из базы данных Частных домов
async def insit_privat_command(message : types.Message):
    await sqlite_db.sql_read_privat(message)

#Вывод данных об акциях
async def insit_sales_command(message : types.Message):
    await sqlite_db.sql_read_sales(message)

#Ссылки для скачивания
async def insit_download_URL(message: types.Message):
    await message.answer("Скачать приложение <ИНСИТ> для:", reply_markup=downloadkb)

#Полезные ссылки
async def insit_usefull_URL(message: types.Message):
    await message.answer("Полезные ссылки:", reply_markup=usefullkb)


def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(command_start, commands=["start", "help"])
    dp.register_message_handler(insit_open_command, commands=["⏰Режим_работы"])
    dp.register_message_handler(insit_place_command, commands=["🗺Расположение"])
    dp.register_message_handler(insit_price_command, commands=["📋Тарифы"])
    dp.register_message_handler(insit_mkd_command, commands=["🏬В_многоквартирных_домах"])
    dp.register_message_handler(insit_privat_command, commands=["🏠В_частных_домах"])
    dp.register_message_handler(insit_back_command, commands=["↪️Вернуться"])
    dp.register_message_handler(insit_sales_command, commands=["💯Скидки/Акции"])
    dp.register_message_handler(insit_download_URL, commands=["⏬Скачать"])
    dp.register_message_handler(insit_usefull_URL, commands=["🌐Полезные_ссылки"])


