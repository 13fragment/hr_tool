from aiogram import Dispatcher,executor,types,Bot
from aiogram.types import KeyboardButton,ReplyKeyboardMarkup

# import logging библиотечка с логами, для дальнейшего релиза будет полезна
API_TOKEN ='5727921189:AAHSWpPnpEWgjJYRVsEUzBGhi_HgTF8Kit8'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

text = open('greeting_msg.txt',encoding='utf-8')
if text != None:
    data = text.read()

commands_welcome = ['start','начать','Начать', 'НАЧАТЬ','Start']

@dp.message_handler (commands=commands_welcome)
async def greeting(message:types.Message):
    await bot.send_message(chat_id=message.from_user.id, text = data,parse_mode="HTML")
    await message.delete()



@dp.message_handler(commands=['help','помощь'])
async def help_command(message:types.Message):
    await message.reply('Связь с тех поддержкой: @mgo1ubev')
if __name__ == '__main__':
    executor.start_polling(dp,skip_updates='True')
