from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            # KeyboardButton(text='🔗 Taklif postini olish'),
        ],
        [
            KeyboardButton(text='👤 Yurist bilan aloqa'),
            KeyboardButton(text='📲 Alimentni hisoblash'),
        ],
    ],
    resize_keyboard=True
)

number = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='📲 Raqamni yuborish', request_contact=True),
        ],
    ],
    resize_keyboard=True
)
