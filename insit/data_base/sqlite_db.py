import sqlite3 as sq
from create_bot import bot

def sql_start():
    global base, cur
    base = sq.connect("insit_info.db")
    cur = base.cursor()
    if base:
        print("Data base connected OK")
    base.execute('CREATE TABLE IF NOT EXISTS mkd(name TEXT PRIMARY KEY, description TEXT, price TEXT)')
    base.execute('CREATE TABLE IF NOT EXISTS privat(name TEXT PRIMARY KEY, description TEXT, price TEXT)')
    base.execute('CREATE TABLE IF NOT EXISTS sales(name TEXT PRIMARY KEY, description TEXT, condition TEXT)')
    base.commit()


#добавление в бд данных о тарифах в МКД
async def sql_add_command_mkd(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO mkd VALUES (?, ?, ?)', tuple(data.values()))
        base.commit()

#добавление в БД данных о тарифах в частных домах
async def sql_add_command_privat(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO privat VALUES (?, ?, ?)', tuple(data.values()))
        base.commit()

#добавление в БД данных об акциях
async def sql_add_command_sales(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO sales VALUES (?, ?, ?)', tuple(data.values()))
        base.commit()

#извлечение данных из БД для МКД
async def sql_read_mkd(message):
    for ret in cur.execute("SELECT * FROM mkd").fetchall():
        await bot.send_message(message.from_user.id, f"🔻 ТАРИФ: {ret[0]}\n\nОПИСАНИЕ: {ret[1]}\n\nЦЕНА: {ret[2]}")

#извлечение данных из БД для частных домов
async def sql_read_privat(message):
    for ret in cur.execute("SELECT * FROM privat").fetchall():
        await bot.send_message(message.from_user.id, f"🔻 ТАРИФ: {ret[0]}\n\nОПИСАНИЕ: {ret[1]}\n\nЦЕНА: {ret[2]}")

#извлечение данных из БД информации об акциях
async def sql_read_sales(message):
    for ret in cur.execute("SELECT * FROM sales").fetchall():
        await bot.send_message(message.from_user.id, f"🔻 НАЗВАНИЕ АКЦИИ: {ret[0]}\n\nОПИСАНИЕ: {ret[1]}\n\nУСЛОВИЕ АКЦИИ: {ret[2]}")

#Вытаскиваем список МКД на удаление
async def sql_read_mkd2():
    return cur.execute("SELECT * FROM mkd").fetchall()

#Удаление данных из МКД
async def sql_delete_mkd(data):
    cur.execute("DELETE FROM mkd WHERE name ==?", (data,))
    base.commit()

#Вытаскиваем список частных домов на удаление
async def sql_read_privat2():
    return cur.execute("SELECT * FROM privat").fetchall()

#Удаление данных из частных домов
async def sql_delete_privat(data):
    cur.execute("DELETE FROM privat WHERE name ==?", (data,))
    base.commit()

#Вытаскиваем список акций на удаление
async def sql_read_sales2():
    return cur.execute("SELECT * FROM sales").fetchall()

#Удаление данных из акций
async def sql_delete_sales(data):
    cur.execute("DELETE FROM sales WHERE name ==?", (data,))
    base.commit()



