from aiogram import Dispatcher,executor,types,Bot
from aiogram.types import KeyboardButton,ReplyKeyboardMarkup

# import logging библиотечка с логами, для дальнейшего релиза будет полезна
API_TOKEN ='5727921189:AAHSWpPnpEWgjJYRVsEUzBGhi_HgTF8Kit8'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


text = open('greeting_msg.txt',encoding='utf-8')
commands_welcome = ['start','начать','Начать', 'НАЧАТЬ','Start']
if text != None:
    data = text.read()
    

keyboard_mp = ReplyKeyboardMarkup (keyboard=[
    [
    KeyboardButton(text='Создать мероприятие'),
    KeyboardButton(text = 'Сгенерировать мероприятие')
    ]
 ],
 resize_keyboard=True, input_field_placeholder='Выберите действие' + ' ' + '⬇️')


@dp.message_handler (commands=commands_welcome)
async def greeting(message:types.Message):
    await bot.send_message(chat_id=message.from_user.id, text = data,parse_mode="HTML",reply_markup=keyboard_mp)
    await message.delete()


@dp.message_handler(commands=['help','помощь'])
async def help_command(message:types.Message):
    await message.reply('Связь с тех поддержкой: @mgo1ubev')


@dp.message_handler(text='Создать мероприятие')
async def create_mp(message:types.Message):
    await message.answer('Введите название мероприятия')
    @dp.message_handler()
    def s(message:types.Message):
        global a
        a = message.text
        print(a)


@dp.message_handler(text=a)
async def create_mp(message:types.Message):
    await message.answer('Введите дату')





if __name__ == '__main__':
    executor.start_polling(dp,skip_updates='True')
