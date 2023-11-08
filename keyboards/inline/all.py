from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

link = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🔗 Taklif postini olish", callback_data="link")
        ]

    ]
)

invite_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="👤 Одам таклиф қилиб балларни тўплаш", callback_data="invite")
        ]

    ]
)
