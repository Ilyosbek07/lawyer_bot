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
            KeyboardButton(text='Referall Content'),
            KeyboardButton(text="Oylik miqdori")
        ],
        [
            KeyboardButton(text='Taklif miqdorini kiritish'),
            KeyboardButton(text='Taklif chegarasini kiritish'),
        #     KeyboardButton(text="G'oliblarga")
        ],
        [
            KeyboardButton(text="Adminni kiriting"),
        #     KeyboardButton(text="Remove File"),
            KeyboardButton(text="Barcha ma'lumotlarni tozalash")
        ],
        [
        #     KeyboardButton(text='Hisobni 0 ga tushirish'),
            KeyboardButton(text="🏘 Bosh menu")

        ]
    ],
    resize_keyboard=True
)
