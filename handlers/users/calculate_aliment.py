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
    limit_require = 0
    elements = await db.get_elements()

    for element in elements:
        score += element['limit_score']
        limit_require += element['limit_require']

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
                    KeyboardButton(text='Ishsiz'),
                ]
            ], resize_keyboard=True
        )
        await message.answer(
            """
            <b>Alimentni hisoblash ta </b> bizga bazi ma'lumotlarni taqdim qilishingiz kerak bo'ladi\n\nOylik maoshingizni kiriting 👇 (Agar ishsiz bo'lsangin <b>"Ishsiz"</b> - Tugmasini bosing)
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
    if message.text == 'Ishsiz':
        await state.update_data(
            {
                'salary': 'Ishsiz'
            }
        )
        await message.answer("Qabul qilindi\n\nFarzandlar sonini kiriting")
        await Calculate.children.set()
    else:
        try:
            salary_user = message.text.replace(' ', '')

            await state.update_data(
                {
                    'salary': int(salary_user)
                }
            )
            await message.answer("Qabul qilindi ✅\n\nFarzandlar sonini kiriting")
            await Calculate.children.set()
        except Exception as err:
            print(err)

            await message.answer("Kechirasiz faqat son jo'natishingiz mumkin")


@dp.message_handler(state=Calculate.children)
async def children_number(message: types.Message, state: FSMContext):
    try:
        children = int(message.text.replace(' ', ''))
        await message.answer("Qabul qilindi ✅")
        data = await state.get_data()
        salary = data.get('salary')
        if salary == "Ishsiz":
            min_salary = await db.get_elements()
            print(min_salary)
            if children == 1:
                aliment = int(min_salary[0]['min_salary'] / 4)
                await message.answer(f"Siz {children} ta farzand uchun {aliment} to'lashingiz kerak", reply_markup=menu)
                await state.finish()

            elif children == 2:
                aliment = int(min_salary[0]['min_salary'] / 3)
                await message.answer(f"Siz {children} ta farzand uchun {aliment} to'lashingiz kerak", reply_markup=menu)
                await state.finish()

            elif children >= 3:
                aliment = int(min_salary[0]['min_salary'] / 2)
                await message.answer(f"Siz {children} ta farzand uchun {aliment} to'lashingiz kerak", reply_markup=menu)
                await state.finish()
            else:
                aliment = int(min_salary[0]['min_salary'] / 2)
                await message.answer(f"Siz {children} ta farzand uchun {aliment} to'lashingiz kerak", reply_markup=menu)
                await state.finish()

        elif salary != "Ishsiz":
            if children == 1:
                aliment = int(salary / 4)
                await message.answer(f"Siz {children} ta farzand uchun {aliment} to'lashingiz kerak", reply_markup=menu)
                await state.finish()

            elif children == 2:
                aliment = int(salary / 3)
                await message.answer(f"Siz {children} ta farzand uchun {aliment} to'lashingiz kerak", reply_markup=menu)
                await state.finish()

            elif children == 3:
                aliment = int(salary / 2)
                await message.answer(f"Siz {children} ta farzand uchun {aliment} to'lashingiz kerak", reply_markup=menu)
                await state.finish()
            else:
                aliment = int(salary / 2)
                await message.answer(f"Siz {children} ta farzand uchun {aliment} to'lashingiz kerak", reply_markup=menu)
                await state.finish()

    except Exception as err:
        print(err)
        await message.answer("Kechirasiz faqat son jo'natishingiz mumkin!!!!")
