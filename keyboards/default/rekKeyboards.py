from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

rekKey1 = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Rasm"),
            KeyboardButton(text="Video")
        ],
        [
            KeyboardButton(text='Text'),
            KeyboardButton(text='Back')
        ]
    ],
    resize_keyboard=True
)
back = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='🔙️ Orqaga'),
        ]
    ],
    resize_keyboard=True
)

main_section = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='🔝 Bosh menu'),
        ]
    ],
    resize_keyboard=True
)

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='- Tanlov'),
        ],
        [
            KeyboardButton(text="- Go School")
        ]
    ], resize_keyboard=True
)

admin_key = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Post Yuborish 🗒'),
        ],
        [
            KeyboardButton(text='Barcha Adminlar'),
            KeyboardButton(text='Admin ➕'),
            KeyboardButton(text='Admin ➖')
        ],
        [
            KeyboardButton(text='Kanal ➕'),
            KeyboardButton(text='Kanal ➖')
        ],
        [
            KeyboardButton(text="Kanallar 📈"),
            KeyboardButton(text="Statistika 📊")
        ],
        [
            KeyboardButton(text='Taklif miqdorini kiritish'),
            KeyboardButton(text='Taklif chegarasini kiritish'),
        ],
        [
            KeyboardButton(text="🏘 Bosh menu")
        ]
    ],
    resize_keyboard=True
)
admin_key2 = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Referall Content'),
            KeyboardButton(text="Referall Content tozalash"),
            KeyboardButton(text="Admin haqida ma'lumot"),
        ],
        [
            KeyboardButton(text='1-miqdor'),
            KeyboardButton(text='2-miqdor'),
            KeyboardButton(text='3-miqdor'),
        ],
        [
            KeyboardButton(text='Eng kam oylik'),
            KeyboardButton(text="Bitta farzand uchun"),
            KeyboardButton(text="Ikkita farzand uchun")
        ],
        [
            KeyboardButton(text='Uch va undan ortiq farzand uchun'),
            KeyboardButton(text="🏘 Bosh menu")
        ]
    ],
    resize_keyboard=True
)
