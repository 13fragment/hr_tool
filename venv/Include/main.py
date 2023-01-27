from aiogram import Dispatcher,executor,types,Bot
from aiogram.types import KeyboardButton,ReplyKeyboardMarkup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup,State
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
import random
import datetime
from config.config import API_TOKEN,ANALITICS,TEH,SALE_OTDEL,LOGIN,PASS

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


text = open('greeting_msg.txt',encoding='utf-8')
commands_welcome = ['start','начать','Начать', 'НАЧАТЬ','Start']
if text != None:
    welcome_text = text.read()
    
keyboard_login = ReplyKeyboardMarkup(keyboard = [[KeyboardButton('Авторизация')]],
resize_keyboard=True,one_time_keyboard=True)

keyboard_mp = ReplyKeyboardMarkup (keyboard = [
    [
        
    KeyboardButton('Создать мероприятие'),
    KeyboardButton('Сгенерировать мероприятие')
    
    ]

],
 resize_keyboard=True, input_field_placeholder='Выберите действие' + ' ' + '⬇️',one_time_keyboard=True)

class MpStatesGroup(StatesGroup):
    name = State()
    description = State()
    tags = State()
    date = State()
    time = State()
    place = State()
    otdel = State()
    confirm = State()
    photo = State()

class Admin(StatesGroup):
    login = State()
    password = State()


@dp.message_handler (commands=['start'])
async def greeting(message:types.Message):
    await message.answer(text=welcome_text,reply_markup=keyboard_login,parse_mode='HTML')
    await message.answer('Для начала необходимо авторизоваться')

@dp.message_handler(Text(equals='Авторизация', ignore_case=True), state=None)
async def greeting(message:types.Message):
    await Admin.login.set()
    await message.reply('Введите логин')

@dp.message_handler(state=Admin.login)
async def a_login(message:types.Message,state: FSMContext):
    async with state.proxy() as data:
        data['login'] = message.text
    if data['login'] == LOGIN:
        await Admin.next()
        await message.reply('Введите пароль')
    else:
        await message.answer('Неверный логин, доступ запрещен!')
        await state.finish()

@dp.message_handler(state=Admin.password)
async def a_password(message:types.Message,state: FSMContext):
    async with state.proxy() as data:
        data['password'] = message.text
    if data['password'] == PASS:
        await state.finish()
        await message.reply('Авторизация выполнена успешно!',reply_markup=keyboard_mp)
    else:
        await message.answer('Неверный пароль, доступ запрещен!')
        await state.finish()

@dp.message_handler(Text(equals='Создать мероприятие', ignore_case=True), state=None)
async def greeting(message:types.Message):
    await MpStatesGroup.name.set()
    await message.reply('Введите название мероприятия')

@dp.message_handler(state=MpStatesGroup.name)
async def name_mp(message:types.Message,state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await MpStatesGroup.next()
    await message.reply('Добавьте описание')

@dp.message_handler(state=MpStatesGroup.description)
async def description_mp(message:types.Message,state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await MpStatesGroup.next()
    await message.reply('Добавьте теги, используя #')

@dp.message_handler(state=MpStatesGroup.tags)
async def tags_mp(message:types.Message,state: FSMContext):
    async with state.proxy() as data:
        data['tags'] = message.text
    await MpStatesGroup.next()
    await message.reply('Добавьте дату')

@dp.message_handler(state=MpStatesGroup.date)
async def date_mp(message:types.Message,state: FSMContext):
    async with state.proxy() as data:
        data['date'] = message.text
    await MpStatesGroup.next()
    await message.reply('Добавьте время')

@dp.message_handler(state=MpStatesGroup.time)
async def time_mp(message:types.Message,state: FSMContext):
    async with state.proxy() as data:
        data['time'] = message.text
    await MpStatesGroup.next()
    await message.reply('Добавьте место')

@dp.message_handler(state=MpStatesGroup.place)
async def place_mp(message:types.Message,state: FSMContext):
    async with state.proxy() as data:
        data['place'] = message.text
    await MpStatesGroup.next()
    await message.reply('Выберите отдел')


@dp.message_handler(state=MpStatesGroup.otdel)
async def otdel(message:types.Message,state: FSMContext):
    async with state.proxy() as data:
        data['otdel'] = message.text
    await message.answer('Все верно?')
    await bot.send_message(chat_id=message.from_user.id,
        text= data['name'] + '\n' + '\n'
        + data['description']+ '\n'
        + data['tags']+ '\n'
        + data['date']+ '\n'
        + data['time']+ '\n'
        + data['place'])
    await MpStatesGroup.next()

@dp.message_handler(state=MpStatesGroup.confirm)
async def confirm(message:types.Message,state: FSMContext):
    async with state.proxy() as data:
        data['confirm'] = message.text
    if data['confirm'] == ('Да' or 'да'):
        await message.reply('Остался последний шаг: добавьте фото')
    else:
        await state.finish()
        await message.answer('<em>Мероприятие будет создано заново</em>'+'<b>\nВведите название мероприятия</b>',parse_mode='HTML')
    await MpStatesGroup.next()

@dp.message_handler(content_types = ['photo'],state=MpStatesGroup.photo)
async def photo_mp(message:types.Message,state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
        await state.finish()
    async with state.proxy() as data:
        await bot.send_photo(chat_id=message.from_user.id,
        photo=data['photo'],
        caption = data['name'] + '\n' + '\n'
        + data['description']+ '\n'
        + data['tags']+ '\n'
        + data['date']+ '\n'
        + data['time']+ '\n'
        + data['place'])
        # await message.reply('Все верно?')
        
        if data['otdel'] == ('Аналитика' or 'аналитика'):
            async with state.proxy() as data:
                await bot.send_photo(chat_id=ANALITICS,
                photo=data['photo'],
                caption = data['name'] + '\n' + '\n'
                + data['description']+ '\n'
                + data['tags']+ '\n'
                + data['date']+ '\n'
                + data['time']+ '\n'
                + data['place'])

        
        elif data['otdel'] == ('Технический отдел' or 'технический отдел'):
            async with state.proxy() as data:
                await bot.send_photo(chat_id=TEH,
                photo=data['photo'],
                caption = data['name'] + '\n' + '\n'
                + data['description']+ '\n'
                + data['tags']+ '\n'
                + data['date']+ '\n'
                + data['time']+ '\n'
                + data['place'])


        elif data['otdel'] == ('Отдел продаж' or 'отдел продаж'):
            async with state.proxy() as data:
                await bot.send_photo(chat_id=SALE_OTDEL,
                photo=data['photo'],
                caption = data['name'] + '\n' + '\n'
                + data['description']+ '\n'
                + data['tags']+ '\n'
                + data['date']+ '\n'
                + data['time']+ '\n'
                + data['place'])
        await message.answer('Мероприятие успешно создано!')


@dp.message_handler(commands=['help','помощь'])
async def help_command(message:types.Message):
    await message.reply('Связь с тех поддержкой: @mgo1ubev')

@dp.message_handler(Text(equals='Сгенерировать мероприятие', ignore_case=True), state=None)
async def rand_events_send(message:types.Message):
    await bot.send_photo(chat_id=TEH, photo="https://mb-ar.ru/ckeditor/images/735-0b49c7f2cdaf75441dc84b2bd2f45a93.jpg", caption= rand_event())
    await message.reply('Мероприятие сгенерированно')
if __name__ == '__main__':
    executor.start_polling(dp,skip_updates='True')