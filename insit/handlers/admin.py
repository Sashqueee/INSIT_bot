from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import bot, dp
from aiogram.dispatcher.filters import Text
from data_base import sqlite_db
from keyboards.admin_kb import button_case_admin, button_case_admin_choose, button_case_admin_del_choose
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

ID = None

class FSMAdmin(StatesGroup):
    name = State()
    description = State()
    price = State()
    choose = State()
    name_sales = State()
    description_sales = State()
    condition_sales = State()


#Получим ID текущего модератора
#@dp.message_handler(commands=["moderator"], is_chat_admin=True)
async def make_changes_command(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, "Что надо, хозяин???", reply_markup=button_case_admin)
    await message.delete()

#Выбираем что сделать и кнопка возврата
#@dp.message_handler(commands=["Удалить_тариф"])
async def admin_del_choose(message: types.Message):
    if message.from_user.id == ID:
        await bot.send_message(message.from_user.id, "Какой тариф удалить?", reply_markup=button_case_admin_del_choose)


#@dp.message_handler(commands=["Назад"])
async def admin_back(message: types.Message):
    if message.from_user.id == ID:
        await bot.send_message(message.from_user.id, "Что надо, хозяин???", reply_markup=button_case_admin)



#-------------------------=====НАЧАЛО ЗАГРУЗКИ ТАРИФА=====-------------------------
#Начало дилога для загрузки нового тарифа
#@dp.message_handler(commands="Загрузить_тариф", state=None)
async def cm_start(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.name.set()
        await message.reply("Введи название тарифа")

#Выход из состояний
#@dp.message_handler(state="*", commands="отмена")
#@dp.message_handler(Text(equals="отмена", ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply("OK")

#Ловим название тарифа
#@dp.message_handler(state=FSMAdmin.name)
async def load_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data["name"] = message.text
        await FSMAdmin.next()
        await message.reply("Теперь введи описание")

#Ловим описание тарифа
#@dp.message_handler(state=FSMAdmin.description)
async def load_description(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data["description"] = message.text
        await FSMAdmin.next()
        await message.reply("Теперь укажи цену")


#Ловим цену тарифа
#@dp.message_handler(state=FSMAdmin.price)
async def load_price(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data["price"] = message.text
        await FSMAdmin.next()
        await bot.send_message(message.from_user.id, "Для каких домов этот тариф?", reply_markup=button_case_admin_choose)

#Выбираем для каких домов загружаем тариф
#@dp.message_handler(state=FSMAdmin.choose)
async def choose_command(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        if message.text == "/МКД":
            await sqlite_db.sql_add_command_mkd(state)
            await state.finish()
            await bot.send_message(message.from_user.id, "Добавлен тариф для МКД", reply_markup=button_case_admin)
        elif message.text == "/Частные_дома":
            await sqlite_db.sql_add_command_privat(state)
            await state.finish()
            await bot.send_message(message.from_user.id, "Добавлен тариф для частных домов", reply_markup=button_case_admin)
#-------------------------=====КОНЕЦ ЗАГРУЗКИ ТАРИФА=====-------------------------

#-------------------------=====НАЧАЛО ЗАГРУЗКИ АКЦИИ=====-------------------------
#Начало дилога для загрузки новой акции
#@dp.message_handler(commands="Загрузить_акцию", state=None)
async def cm_start_sales(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.name_sales.set()
        await message.reply("Введи название акции")

#Ловим название акции
#@dp.message_handler(state=FSMAdmin.name)
async def load_name_sales(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data["name_sales"] = message.text
        await FSMAdmin.next()
        await message.reply("Теперь введи описание")

#Ловим описание акции
#@dp.message_handler(state=FSMAdmin.description)
async def load_description_sales(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data["description_sales"] = message.text
        await FSMAdmin.next()
        await message.reply("Теперь укажи условие для акции")


#Ловим условие для акции
#@dp.message_handler(state=FSMAdmin.price)
async def load_condition(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data["condition_sales"] = message.text
        await sqlite_db.sql_add_command_sales(state)
        await state.finish()
        await bot.send_message(message.from_user.id, "Акция добавлена", reply_markup=button_case_admin)
#-------------------------=====КОНЕЦ ЗАГРУЗКИ АКЦИИ=====-------------------------

#-------------------------=====УДАЛЕНИЕ ТАРИФОВ И АКЦИЙ=====-------------------------

#Удаление из МКД
#@dp.message_handler(commands= "Удалить_из_МКД")
async def delete_item_mkd(message: types.Message):
    if message.from_user.id == ID:
        read = await sqlite_db.sql_read_mkd2()
        for ret in read:
            await bot.send_message(message.from_user.id, f"Название: {ret[0]}\nОписание: {ret[1]}\nЦена: {ret[2]}")
            await bot.send_message(message.from_user.id, text="^^^", reply_markup=InlineKeyboardMarkup().\
                                   add(InlineKeyboardButton(f"Удалить {ret[0]}", callback_data=f"del {ret[0]}")))


#@dp.callback_query_handler(lambda x: x.data.startswith("del "))
async def del_callback_run_mkd(callback_query: types.CallbackQuery):
    await sqlite_db.sql_delete_mkd(callback_query.data.replace("del ", ""))
    await callback_query.answer(text=f"{callback_query.data.replace('del ', '')} удалён.", show_alert=True)



#Удаление из частных домов
#@dp.message_handler(commands= "Удалить_из_частных_домов")
async def delete_item_privat(message: types.Message):
    if message.from_user.id == ID:
        read = await sqlite_db.sql_read_privat2()
        for ret in read:
            await bot.send_message(message.from_user.id, f"Название: {ret[0]}\nОписание: {ret[1]}\nЦена: {ret[2]}")
            await bot.send_message(message.from_user.id, text="^^^", reply_markup=InlineKeyboardMarkup().\
                                   add(InlineKeyboardButton(f"Удалить {ret[0]}", callback_data=f"delp {ret[0]}")))

#@dp.callback_query_handler(lambda x: x.data.startswith("del "))
async def del_callback_run_privat(callback_query: types.CallbackQuery):
    await sqlite_db.sql_delete_privat(callback_query.data.replace("delp ", ""))
    await callback_query.answer(text=f"{callback_query.data.replace('delp ', '')} удалён.", show_alert=True)


#Удаление из акций
#@dp.message_handler(commands= "Удалить_из_акций")
async def delete_item_sales(message: types.Message):
    if message.from_user.id == ID:
        read = await sqlite_db.sql_read_sales2()
        for ret in read:
            await bot.send_message(message.from_user.id, f"Название: {ret[0]}\nОписание: {ret[1]}\nУсловие: {ret[2]}")
            await bot.send_message(message.from_user.id, text="^^^", reply_markup=InlineKeyboardMarkup().\
                                   add(InlineKeyboardButton(f"Удалить {ret[0]}", callback_data=f"dels {ret[0]}")))

#@dp.callback_query_handler(lambda x: x.data.startswith("del "))
async def del_callback_run_sales(callback_query: types.CallbackQuery):
    await sqlite_db.sql_delete_sales(callback_query.data.replace("dels ", ""))
    await callback_query.answer(text=f"{callback_query.data.replace('dels ', '')} удалена.", show_alert=True)



def register_handlers_admin(dp : Dispatcher):
    dp.register_message_handler(admin_del_choose, commands=["Удалить_тариф"])
    dp.register_message_handler(admin_back, commands=["Назад"])
    dp.register_message_handler(cm_start, commands="Загрузить_тариф", state=None)
    dp.register_message_handler(cm_start_sales, commands="Загрузить_акцию", state=None)
    dp.register_message_handler(cancel_handler, state="*", commands="отмена")
    dp.register_message_handler(cancel_handler, Text(equals="отмена", ignore_case=True), state="*")
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_name_sales, state=FSMAdmin.name_sales)
    dp.register_message_handler(load_description_sales, state=FSMAdmin.description_sales)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_condition, state=FSMAdmin.condition_sales)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(delete_item_mkd, commands="МКД")
    dp.register_callback_query_handler(del_callback_run_mkd, (lambda x: x.data and x.data.startswith("del ")))
    dp.register_message_handler(delete_item_privat, commands="Частные_дома")
    dp.register_callback_query_handler(del_callback_run_privat, (lambda x: x.data and x.data.startswith("delp ")))
    dp.register_message_handler(delete_item_sales, commands="Удалить_из_акций")
    dp.register_callback_query_handler(del_callback_run_sales, (lambda x: x.data and x.data.startswith("dels ")))
    dp.register_message_handler(choose_command, state=FSMAdmin.choose)
    dp.register_message_handler(make_changes_command, commands=["moderator"], is_chat_admin=True)


