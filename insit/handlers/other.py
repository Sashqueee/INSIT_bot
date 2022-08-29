from aiogram import types, Dispatcher
from keyboards.client_kb import kb_client


#@dp.message_handler()
async def echo_send(message: types.Message):
    await message.answer("Пожалуйста, воспользуйтесь предложенными командами", reply_markup=kb_client)
    await message.delete()

def register_handlers_other(dp : Dispatcher):
    dp.register_message_handler(echo_send)