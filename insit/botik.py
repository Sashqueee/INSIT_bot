from aiogram.utils import executor
from create_bot import dp
from handlers import client, admin, other
from data_base import sqlite_db


async def on_startup(_):
    print("Бот вышел в онлайн")
    sqlite_db.sql_start()


    #await message.answer(message.text)
    #await message.reply(message.text)
    #await bot.send_message(message.from_user.id, message.text)

client.register_handlers_client(dp)
admin.register_handlers_admin(dp)
other.register_handlers_other(dp)



executor.start_polling(dp, skip_updates=True, on_startup=on_startup)