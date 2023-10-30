from aiogram import Dispatcher, types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from random import randint
import requests, json
from bot_wb.keyboards import create_keyboard



def get_basket(a):
    if 0 <= a <= 143:
        return '01'
    if 144 <= a <= 287:
        return '02'
    if 288 <= a <= 431:
        return '03'
    if 432 <= a <= 719:
        return '04'
    if 720 <= a <= 1007:
        return '05'
    if 1008 <= a <= 1061:
        return '06'
    if 1062 <= a <= 1115:
        return '07'
    if 1116 <= a <= 1169:
        return '08'
    if 1170 <= a <= 1313:
        return '09'
    if 1314 <= a <= 1601:
        return '10'
    if 1602 <= a <= 1889:
        return '12'   



def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=['start'])
    dp.register_message_handler(get_product, content_types=['text'])
    dp.register_callback_query_handler(price, text='price')
    dp.register_callback_query_handler(desc, text = 'desc')
    dp.register_callback_query_handler(new, text='new')
    dp.register_callback_query_handler(feed, text='status')



async def cmd_start(message: types.Message, state:FSMContext):
    await message.answer(text='Привет. Этот бот поможет тебе получить всю интересующую тебя информацию о товаре  на Wilberries по его артикулу. Пришли боту артикул товара')
    async with state.proxy() as data:
        try:
            if data['name'] is None:
                data['name'] = []
        except:
            data['name'] = []
        try:
            if data['desc'] is None:
                data['desc'] = []
        except:
            data['desc'] = []
        try:
            if data['price'] is None:
                data['price'] = []
        except:
            data['price'] = []
        try:
            if data['w_price'] is None:
                data['w_price'] = []
        except:
            data['w_price'] = []
        try:
            if data['type'] is None:
                data['type'] = []
        except:
            data['type'] = []
        try:
            if data['rate'] is None:
                data['rate'] = []
        except:
            data['rate'] = []
        try:
            if data['feed'] is None:
                data['feed'] = []
        except:
            data['feed'] = []



async def get_product(message: types.Message, state: FSMContext):
    await message.answer('Ищу...')
    txt = str(message.text)
    vol = int(txt)//100000 
    bsk = str(get_basket(int(vol)))
    part = int(txt)//1000
    try:
        URL = f"https://basket-{bsk}.wb.ru/vol{vol}/part{part}/{txt}/info/ru/card.json"
        response = requests.get(URL)
        info = json.loads(response.text)
        URL1 = f"https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&nm={txt}"
        price_response = requests.get(URL1)
        price_info = json.loads(price_response.text)
        price_w = price_info['data']['products'][0]['priceU']
        price_w = str(price_w)[:-2]
        price = price_info['data']['products'][0]['salePriceU']
        feed = price_info['data']['products'][0]['feedbacks']
        rating = price_info['data']['products'][0]['reviewRating']
        price = str(price)[:-2]
        async with state.proxy() as data:
            data['desc'].append(info['description'])
            data['name'].append(info['imt_name'])
            data['type'].append(info['subj_root_name'])
            data['w_price'].append(price_w)
            data['price'].append(price)
            data['feed'].append(feed)
            data['rate'].append(rating)
            await message.answer(text=f"Товар: {data['name'][0]}. Выберите, какую информацию вы хотите получить о товаре",reply_markup=create_keyboard())
    except:
        try:
            URL = f"https://basket-11.wb.ru/vol{vol}/part{part}/{txt}/info/ru/card.json"
            response = requests.get(URL)
            info = json.loads(response.text)
            URL1 = f"https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&nm={txt}"
            price_response = requests.get(URL1)
            price_info = json.loads(price_response.text)
            price_w = price_info['data']['products'][0]['priceU']
            price_w = str(price_w)[:-2]
            price = price_info['data']['products'][0]['salePriceU']
            feed = price_info['data']['products'][0]['feedbacks']
            rating = price_info['data']['products'][0]['reviewRating']
            price = str(price)[:-2]
            async with state.proxy() as data:
                data['desc'].append(info['description'])
                data['name'].append(info['imt_name'])
                data['type'].append(info['subj_root_name'])
                data['w_price'].append(price_w)
                data['price'].append(price)
                data['feed'].append(feed)
                data['rate'].append(rating)
                await message.answer(text=f"Товар: {data['name'][0]}. Выберите, какую информацию вы хотите получить о товаре",reply_markup=create_keyboard())
        except:
            await message.answer("Несуществующий артикул")
   


async def price(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        await call.message.answer(text=f"Цена товара без скидки - {data['w_price'][0]}. Реальная цена товара - {data['price'][0]}. ВАЖНО! Цены указываются без учета вашей скидки постоянного клиента на WB", reply_markup = create_keyboard())



async def desc(call: types.CallbackQuery, state:FSMContext):
    async with state.proxy() as data:
        await call.message.answer(text=f"{data['desc'][0]}", reply_markup= create_keyboard())



async def new(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = []
        data['desc'] = []
        data['type'] = []
        data['w_price'] = []
        data['price'] = []
        data['rate'] = []
        data['feed'] = []
    await call.message.answer(text='Введите артикул, чтобы получить данные о новом товаре.')



async def feed(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        await call.message.answer(text = f"Количество отзывов на товар: {data['feed'][0]}. Его рейтинг: {data['rate'][0]}", reply_markup= create_keyboard())