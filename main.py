from aiogram.types import ReplyKeyboardRemove
import asyncio
import aiosqlite
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import ReplyKeyboardBuilder

bot = Bot(token="") # Введите сюда свой токен бота из BotFather
dp = Dispatcher()
ADMIN = [123456789] #Введите сюда свой ID из Telegram

DB_NAME = "users_database.db"

async def start():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS data (
                user_id INTEGER, 
                username TEXT, 
                res INTEGER, 
                op TEXT
            )
        """)
        await db.commit()

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username or "User"

    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Просмотреть историю"))

    if user_id in ADMIN:
        builder.add(types.KeyboardButton(text="Админка: Вся база"))

    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT user_id FROM data WHERE user_id = ?", (user_id,)) as cursor:
            row = await cursor.fetchone()
            if row is None:
                await db.execute(
                    "INSERT INTO data (user_id, username, res, op) VALUES (?, ?, ?, ?)", 
                    (user_id, username, 0, "start")
                )
                await db.commit()

    await message.answer(f"Привет, {username}! Я записал тебя в базу.\n\n"f"Чтобы посчитать пример, напиши его через пробел (например: 5 + 10).\n"f"Чтобы увидеть историю, нажми на кнопку ниже:",reply_markup=builder.as_markup(resize_keyboard=True))



@dp.message(F.text == "Просмотреть историю")
async def show_history(message: types.Message):
    user_id = message.from_user.id
    
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            "SELECT res, op FROM data WHERE user_id = ? AND op != 'start' ORDER BY rowid DESC LIMIT 1", 
            (user_id,)
        ) as cursor:
            row = await cursor.fetchone()
            if row:
                await message.answer(f" Твоя последняя операция: {row[0]}, знак: {row[1]}")
            else:
                await message.answer("Ты еще ничего не считал! Твоя история пуста.")
@dp.message(F.text == "Админка: Вся база")
async def show_all_database(message: types.Message):
    user_id = message.from_user.id
    
  
    if user_id not in ADMIN:
        await message.answer("У вас нет прав доступа к этой команде!")
        return

    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT username, op, res FROM data WHERE op != 'start'") as cursor:
            rows = await cursor.fetchall()
            
            if rows:
                response_text = "**ЛОГ ВСЕХ ПОЛЬЗОВАТЕЛЕЙ:**\n\n"
                
                
                for row in rows:
                    username = row[0] if row[0] else "Скрыт"
                    op = row[1]
                    res = row[2]
                    
                    response_text += f"Никнейм юзера: @{username}\n Его история: {op} | Результат: {res}\n"
                    response_text += "-------------------------\n"
                
                await message.answer(response_text)
            else:
                await message.answer("База данных пока пуста от вычислений!")




@dp.message(F.text)
async def zapros(message: types.Message):
    try:
        primer = message.text.split()
        
        if len(primer) != 3:
            await message.answer("Введи пример через пробел! Например: 5 + 10")
            return
            
        x = int(primer[0])
        op = primer[1]
        y = int(primer[2])
        
        if op not in ["+", "-", "/", "*"]:
            await message.answer("Такого действия нету! Доступны только +, -, /, *")
            return
            
        if op == "+": res = x + y
        elif op == "-": res = x - y
        elif op == "/": res = x / y
        elif op == "*": res = x * y

        await message.answer(f"Результат: {res}")
        
       
        async with aiosqlite.connect(DB_NAME) as db:
            await db.execute(
                "INSERT INTO data (user_id, username, res, op) VALUES (?, ?, ?, ?)", 
                (message.from_user.id, message.from_user.username, res, op)
            )
            await db.commit()

    except ValueError:
        await message.answer("Вводи цифры через пробел!")
    except ZeroDivisionError:
        await message.answer("Не дели на ноль!")

async def start_bot():
    await start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    await start_bot()
