from aiogram import Dispatcher,executor,types,Bot
# from aiogram.types import KeyboardButton так импортируются отдельные типы, например тип с кнопкой 
# import logging библиотечка с логами, для дальнейшего релиза будет полезна
API_TOKEN ='5727921189:AAHSWpPnpEWgjJYRVsEUzBGhi_HgTF8Kit8'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
@dp.message_handler(commands=['start'])
async def welcome_message(message:types.Message):
    await message.reply('Welcome to the party!')
@dp.message_handler(commands=['start_bot'])
async def start_bot(message:types.BotCommand):
    await executor.start_polling(dp,skip_updates='True')
@dp.message_handler(commands=['stop'])
async def stop_bot(message:types.BotCommand):
    await dp.stop_polling()
@dp.message_handler()
async def send_welcome(message:types.Message):
    await message.answer(message.text)
    global a
    a = message.text
    print(a)
if __name__ == '__main__':
    executor.start_polling(dp,skip_updates='True')

