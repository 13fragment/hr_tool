from aiogram import Dispatcher,executor,types,Bot
from aiogram.types import KeyboardButton,ReplyKeyboardMarkup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup,State
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
# import logging библиотечка с логами, для дальнейшего релиза будет полезна
API_TOKEN ='5727921189:AAHSWpPnpEWgjJYRVsEUzBGhi_HgTF8Kit8'

SALE_OTDEL = '-1001295882228'
ANALITICS = '-1001899403427'
TEH = '-1001704512557'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())



text = open('greeting_msg.txt',encoding='utf-8')
commands_welcome = ['start','начать','Начать', 'НАЧАТЬ','Start']
if text != None:
    welcome_text = text.read()
    

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
    photo = State()
    confirm = State()

@dp.message_handler (commands=['start'])
async def greeting(message:types.Message):
    await message.answer(text=welcome_text,reply_markup=keyboard_mp,parse_mode='HTML')
    

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
    await MpStatesGroup.next()
    await message.reply('Добавьте фото')

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


if __name__ == '__main__':
    executor.start_polling(dp,skip_updates='True')