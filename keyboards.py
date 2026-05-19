from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

main = ReplyKeyboardMarkup(keyboard = [
    [KeyboardButton(text='･: * Соц-сети * :･'), KeyboardButton(text='･: * Заказать арт * :･')],
    [KeyboardButton(text='･: * Трейд/Коллаб * :･'), KeyboardButton(text='･: * Написать сообщение * :･')]
],
    resize_keyboard=True,
    input_field_placeholder='Выберите пункт меню.')

back = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='back')]
])

tradecollab = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Трейд', callback_data='trade_type_trade')],
    [InlineKeyboardButton(text='Коллаб', callback_data='trade_type_collab')] 
])

def get_socials_keyboard():
    keyboard = InlineKeyboardBuilder()

    keyboard.add(
        InlineKeyboardButton(text='DevianArt', url='https://www.deviantart.com/fluttbet'),
        InlineKeyboardButton(text='X/Twitter', url='https://x.com/fluttbet'),
        InlineKeyboardButton(text='Furaffinity', url='https://www.furaffinity.net/user/fluttbet'),
    )

    keyboard.adjust(1)

    return keyboard.as_markup()


def get_pricelist():
    keyboard = InlineKeyboardBuilder()

    keyboard.add(
        InlineKeyboardButton(text='Price list', url='https://www.deviantart.com/fluttbet/art/ADOPTS-SET-PRICE-OPEN-1272401141'),
    )
    keyboard.adjust(1)

    return keyboard.as_markup() 


def get_contacts():
    keyboard = InlineKeyboardBuilder()

    keyboard.add(
        InlineKeyboardButton(text='･: * Написать сообщение * :･', url='http://t.me/fluttbet'),
    )
    keyboard.adjust(1)

    return keyboard.as_markup()


def get_collab():
    keyboard = InlineKeyboardBuilder()

    keyboard.add(
        InlineKeyboardButton(text='･: * Трейд/Коллаб * :･', url='https://t.me/fluttbetart'),
    )
    keyboard.adjust(1)

    return keyboard.as_markup()
