from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import KeyboardButton

from keyboards.default.all import menu
from loader import dp, db
from states.rekStates import Calculate
from utils.misc import subscription


@dp.message_handler(text='📲 Alimentni hisoblash')
async def calculate(message: types.Message):
    status = True
    all = await db.select_chanel()
    chanels = []
    url = []
    channel_names = []
    score = 0
    elements = await db.get_elements()

    for element in elements:
        score += element['limit_score']

    for i in all:
        chanels.append(i['chanelll'])
        url.append(i['url'])
        channel_names.append(i['channel_name'])

    for channel in chanels:
        status *= await subscription.check(user_id=message.from_user.id,
                                           channel=f'{channel}')
    if status:
        button = types.ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text='Ishlayman'),
                    KeyboardButton(text='Ishsizman'),
                ]
            ], resize_keyboard=True
        )
        await message.answer(
            """
            <b>Alimentni hisoblash </b> uchun bizga bazi ma'lumotlarni taqdim qilishingiz kerak bo'ladi\n\nTugmalardan birni tanlang.)
        """, reply_markup=button)
        await Calculate.salary.set()
    else:
        button = types.InlineKeyboardMarkup(row_width=1, )
        counter = 0
        for i in url:
            button.add(types.InlineKeyboardButton(f"{channel_names[counter]}", url=f'https://t.me/{i}'))
            counter += 1
        button.add(types.InlineKeyboardButton(text="Obuna bo’ldim✅", callback_data="check_subs"))
        text = """
        Assalom aleykum, bu bot sizga Amerikada istiqomat qilib, yuridik faoliyat olib boruvchi malakali yuristlar jamoasidan bepul huquqiy maslahat olishga yordam beradi. \n\nChet elda o’qish bo’yicha tavsiyalar ham so’rashingiz mumkin.
        """
        await message.answer(text)
        await message.answer('Davom etish ta quyidagi kanalga obuna bo’ling ⬇️', reply_markup=button)


@dp.message_handler(state=Calculate.salary)
async def salary_(message: types.Message, state: FSMContext):
    if message.text == 'Ishsizman':
        await state.update_data(
            {
                'salary': 'Ishsizman'
            }
        )
        button = types.ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Bitta farzand uchun"),
                    KeyboardButton(text="Ikkita farzand uchun")
                ],
                [
                    KeyboardButton(text='Uch va undan ortiq farzand uchun'),
                ],
                [
                    KeyboardButton(text='🔙 Orqaga qaytish')
                ]
            ],
            resize_keyboard=True
        )
        await message.answer("Qabul qilindi✅\n\nFarzandlar sonini kiriting", reply_markup=button)
        await Calculate.calculate.set()
    elif message.text == "Ishlayman":
        await message.answer("Oylik maoshingizni kiriting 👇\n"
                             "<b>(Masalan: 3 000 000)</b>", reply_markup=types.ReplyKeyboardRemove())
        await Calculate.children.set()
    else:
        await message.answer("Tugmalardan birini tanlang")


@dp.message_handler(state=Calculate.children)
async def children_number(message: types.Message, state: FSMContext):
    try:
        salary_user = message.text.replace(' ', '')

        await state.update_data(
            {
                'salary': int(salary_user)
            }
        )
        button = types.ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Bitta farzand uchun"),
                    KeyboardButton(text="Ikkita farzand uchun")
                ],
                [
                    KeyboardButton(text='Uch va undan ortiq farzand uchun'),
                ],
                [
                    KeyboardButton(text='🔙 Orqaga qaytish')
                ]
            ],
            resize_keyboard=True
        )

        await message.answer("Qabul qilindi ✅\n\nFarzandlar sonini kiriting", reply_markup=button)
        await Calculate.children.set()
    except Exception as err:
        print(err)

        await message.answer("Kechirasiz faqat son jo'natishingiz mumkin")
    await Calculate.calculate.set()


@dp.message_handler(state=Calculate.calculate)
async def calculatee(message: types.Message, state: FSMContext):
    data = await state.get_data()
    salary = data.get('salary')

    if message.text == "🔙 Orqaga" and salary == "Ishsizman":
        button = types.ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Bitta farzand uchun"),
                    KeyboardButton(text="Ikkita farzand uchun")
                ],
                [
                    KeyboardButton(text='Uch va undan ortiq farzand uchun'),
                ],
                [
                    KeyboardButton(text='🔙 Orqaga qaytish')
                ]
            ],
            resize_keyboard=True
        )
        await message.answer("Farzandlar sonini kiriting", reply_markup=button)
        # await Calculate.calculate.set()
    elif message.text == "🔙 Orqaga" and salary != "Ishsizman":
        button = types.ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Bitta farzand uchun"),
                    KeyboardButton(text="Ikkita farzand uchun")
                ],
                [
                    KeyboardButton(text='Uch va undan ortiq farzand uchun'),
                ],
                [
                    KeyboardButton(text='🔙 Orqaga qaytish')
                ]
            ],
            resize_keyboard=True
        )
        await message.answer("Farzandlar sonini kiriting", reply_markup=button)
    elif message.text == "🔙 Orqaga qaytish":
        choice = types.ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text='Ishlayman'),
                    KeyboardButton(text='Ishsizman'),
                ]
            ], resize_keyboard=True
        )
        await message.answer("""
            <b>Alimentni hisoblash </b> uchun bizga bazi ma'lumotlarni taqdim qilishingiz kerak bo'ladi\n\nTugmalardan birni tanlang.)
        """, reply_markup=choice)
        await state.reset_data()
        await Calculate.salary.set()
    elif message.text == "🔝 Bosh Menu":
        await message.answer("Bosh menu", reply_markup=menu)
        await state.finish()
    else:
        try:
            children = message.text
            await message.answer("Qabul qilindi ✅")
            button = types.ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text="🔙 Orqaga"),
                        KeyboardButton(text="🔝 Bosh Menu")
                    ]], resize_keyboard=True
            )
            if salary == "Ishsizman":
                db_data = await db.get_elements()
                if children == "Bitta farzand uchun":
                    await message.answer(
                        f"Siz {children} ta farzand uchun {db_data[0]['one_child']} so'm to'lashingiz kerak",
                        reply_markup=button)

                elif children == "Ikkita farzand uchun":
                    await message.answer(
                        f"Siz {children} ta farzand uchun {db_data[0]['two_children']} so'm to'lashingiz kerak",
                        reply_markup=button)

                elif children == "Uch va undan ortiq farzand uchun":
                    await message.answer(
                        f"Siz {children} ta farzand uchun {db_data[0]['three_children']} so'm to'lashingiz kerak",
                        reply_markup=button)

            elif salary != "Ishsizman":
                if children == "Bitta farzand uchun":
                    aliment = float(salary / 4)
                    await message.answer(f"Siz {children} ta farzand uchun {aliment} so'm to'lashingiz kerak",
                                         reply_markup=button)

                elif children == "Ikkita farzand uchun":
                    aliment = float(salary / 3)
                    await message.answer(f"Siz {children} ta farzand uchun {aliment} so'm to'lashingiz kerak",
                                         reply_markup=button)

                elif children == "Uch va undan ortiq farzand uchun":
                    aliment = float(salary / 2)
                    await message.answer(f"Siz {children} ta farzand uchun {aliment} so'm to'lashingiz kerak",
                                         reply_markup=button)

        except Exception as err:
            print(err)
            await message.answer("Kechirasiz faqat son jo'natishingiz mumkin!!!!")


@dp.message_handler(state=Calculate.ishsiz)
async def calculatee(message: types.Message, state: FSMContext):
    print('keldi')
    button = types.ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Bitta farzand uchun"),
                KeyboardButton(text="Ikkita farzand uchun")
            ],
            [
                KeyboardButton(text='Uch va undan ortiq farzand uchun'),
            ],
            [
                KeyboardButton(text='🔙 Orqaga qaytish')
            ]
        ],
        resize_keyboard=True
    )
    await message.answer("Qabul qilindi✅\n\nFarzandlar sonini kiriting", reply_markup=button)
    await Calculate.calculate.set()
