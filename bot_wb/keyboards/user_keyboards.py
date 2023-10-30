from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
def create_keyboard():
    kb = InlineKeyboardMarkup()
    bt = InlineKeyboardButton(text='Цена', callback_data='price')
    kb.add(bt)
    bt = InlineKeyboardButton(text='Количество отзывов и рейтинг', callback_data='status')
    kb.add(bt)
    bt = InlineKeyboardButton(text='Описание товара', callback_data='desc')
    kb.add(bt)
    bt = InlineKeyboardButton(text='Новый товар', callback_data='new')
    kb.add(bt)
    return kb