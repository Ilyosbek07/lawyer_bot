from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='🔗 Taklif postini olish'),
        ],
        [
            KeyboardButton(text='📲 Alimentni hisoblash'),
            KeyboardButton(text='👤 Huquqshunos bilan aloqa'),
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
