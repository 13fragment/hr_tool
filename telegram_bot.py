from aiogram import Dispatcher,executor,types,Bot
from aiogram.types import KeyboardButton,ReplyKeyboardMarkup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup,State
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
import random
import datetime
# import logging библиотечка с логами, для дальнейшего релиза будет полезна
API_TOKEN ='5727921189:AAHSWpPnpEWgjJYRVsEUzBGhi_HgTF8Kit8'
SALE_OTDEL = '-1001295882228'
ANALITICS = '-1001899403427'
TEH = '-1001704512557'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())




# Мероприятия предустановленные
def rand_event():
    event_id = random.randint(0,2)
    
 
    current_time = datetime.datetime.today()
    event_time = random.randint(0,14)
    if event_id == 0:
        name = "Кинотимбилдинг"
        description = "В основу положена актёрская игра,продуманный сценарий и другие обязательные составляющие киноиндустрии. Фантазия о главной роли в оскароносном фильме посещала каждого хоть единожды – именно она и подтолкнула к освещению этого мероприятие. Вы сможете попробовать себя в роли актёра, сыграв небольшие сценки с такими же творческими личностями, как вы! "
        tags = "#Event #Chill"
        date = "Дата мероприятия: " + str(event_time) + "/" + str(current_time.month + 1)
        time = random.randint(9,20)
        place = "Место встречи будет оглашено позже"
        photo = "kinoteambuilding.jpg"
    elif event_id == 1:
        name = "Офисная фотоохота"
        description = "Задача команды – найти и сфотографировать череду каких-либо объектов или предметов, находящийся в офисе. Выигрывает команда, подготовивший фотоотчет быстрее и в нужной последовательности.Игра по указанному сценарию развивает пространственное мышление, память и позволяет лучше узнать рабочее пространство."
        tags = "#Event #Chill"
        date = "Дата мероприятия: " + str(event_time) + "/" + str(current_time.month + 1)
        time = random.randint(9,20)
        place = "Место встречи будет оглашено позже"
        photo = "fotoohota.jpg"
    if event_id == 2:
        name = "Войти в историю компании"
        description = "Сотрудникам предлагается не просто стать частью структуры компании, а войти в ее историю и привнести собственную лепту в развитие нового продукта фирмы. По условиям творческого тимбилдинга команда из нескольких сотрудников должна разработать собственную уникальную рецептуру продукта или создать какую-либо полезную модель, которая впоследствии станет новым витком развития бизнеса."
        tags = "#Event #Chill"
        date = "Дата мероприятия: " + str(event_time) + "/" + str(current_time.month + 1)
        time = random.randint(9,20)
        place = "Место встречи будет оглашено позже"
        photo = "comp_history.jpg"
    return(name + "\n" + "\n" + description + "\n"+ tags +"\n" + date + " Время: " + str(time)+ ":00" + "\n" + place)





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
    confirm = State()
    photo = State()

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