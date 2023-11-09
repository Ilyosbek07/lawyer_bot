import asyncio
import json

import asyncpg
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.default.all import menu
from keyboards.inline.all import link
from loader import bot, dp, db
from states.rekStates import DelState
from utils.misc import subscription


@dp.message_handler(CommandStart())
async def show_channels(message: types.Message, state: FSMContext):
    args = message.get_args()
    if_old = await db.select_user(telegram_id=message.from_user.id)
    elements = await db.get_elements()
    photo = ''
    gifts = ''
    score = 0
    limit_require = 0
    for element in elements:
        photo += f"{element['photo']}"
        gifts += f"{element['gifts']}"
        score += element['limit_score']
        limit_require += element['limit_require']

    if args and not if_old:
        try:
            user = await db.add_user(telegram_id=message.from_user.id,
                                     full_name=message.from_user.full_name,
                                     username=message.from_user.username
                                     )
        except asyncpg.exceptions.UniqueViolationError:
            user = await db.select_user(telegram_id=message.from_user.id)
        await db.update_user_args(user_args=f'{args}', telegram_id=message.from_user.id)

        status = True
        all = await db.select_chanel()
        chanels = []
        url = []
        channel_names = []
        for i in all:
            chanels.append(i['chanelll'])
            url.append(i['url'])
            channel_names.append(i['channel_name'])

        for channel in chanels:
            status *= await subscription.check(user_id=message.from_user.id,
                                               channel=f'{channel}')
        if status:
            text = """
            Assalom aleykum, bu bot sizga Amerikada istiqomat qilib, yuridik faoliyat olib boruvchi malakali yuristlar jamoasidan bepul huquqiy maslahat olishga yordam beradi. \n\nChet elda o’qish bo’yicha tavsiyalar ham so’rashingiz mumkin.
            """
            await message.answer(text)

            text = f"""
            ❗️<b>Diqqat bilan o’qing!</b>\n\nHuquqiy maslahat olish va tavsiyalar so’rash 100% bepul. Faqat, huquqiy jihatdan yordamga muhtoj insonlarga bu loyihamiz yetib borishi uchun  sizning yordamingiz juda ham zarur!\n\nBot sizga taqdim etgan referral linkni atigi {limit_require} nafar do'stingizga yuboring va bizga murojaat qilish imkoniga ega bo'ling va bepul maslahat olasiz! \n\n<b>🔗 Taklif postini olish tugmani bosing va taklif qilishni boshlang 👇</b>"""
            await message.answer(text, reply_markup=menu)
            try:
                args = await db.select_user(telegram_id=message.from_user.id)
                args_user = await db.select_user(telegram_id=int(args[7]))
                update_score = int(args_user[4]) + score
                await db.update_user_score(score=update_score, telegram_id=int(args[7]))

                await bot.send_message(chat_id=int(args[7]),
                                       text=f"👤 Yangi ishtirokchi qo`shildi\n"
                                            f"🎗 Siz <b>{update_score}-ta</b> foydalanuvchi taklif qildingiz\n"
                                            f"🗣 Ko`proq do`stlaringizni taklif qiling!")
                await db.update_user_oldd(oldd=1, telegram_id=message.from_user.id)
            except Exception as e:
                print(e)
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
            await message.answer('Davom etish uchun quyidagi kanalga obuna bo’ling ⬇️', reply_markup=button)
    elif not args and not if_old:
        try:
            user = await db.add_user(telegram_id=message.from_user.id,
                                     full_name=message.from_user.full_name,
                                     username=message.from_user.username

                                     )
        except asyncpg.exceptions.UniqueViolationError:
            user = await db.select_user(telegram_id=message.from_user.id)
        status = True
        all = await db.select_chanel()
        chanels = []
        url = []
        channel_names = []
        for i in all:
            chanels.append(i['chanelll'])
            url.append(i['url'])
            channel_names.append(i['channel_name'])

        for channel in chanels:
            status *= await subscription.check(user_id=message.from_user.id,
                                               channel=f'{channel}')
        if status:
            text = """
            Assalom aleykum, bu bot sizga Amerikada istiqomat qilib, yuridik faoliyat olib boruvchi malakali yuristlar jamoasidan bepul huquqiy maslahat olishga yordam beradi. \n\nChet elda o’qish bo’yicha tavsiyalar ham so’rashingiz mumkin.
            """
            await message.answer(text)

            text = f"""
            ❗️<b>Diqqat bilan o’qing!</b>\n\nHuquqiy maslahat olish va tavsiyalar so’rash 100% bepul. Faqat, huquqiy jihatdan yordamga muhtoj insonlarga bu loyihamiz yetib borishi uchun  sizning yordamingiz juda ham zarur!\n\nBot sizga taqdim etgan referral linkni atigi {limit_require} nafar do'stingizga yuboring va bizga murojaat qilish imkoniga ega bo'ling va bepul maslahat olasiz! \n\n<b>🔗 Taklif postini olish tugmani bosing va taklif qilishni boshlang 👇</b>"""
            await message.answer(text, reply_markup=menu)
        else:
            button = types.InlineKeyboardMarkup(row_width=1, )
            counter = 0

            for i in url:
                button.add(types.InlineKeyboardButton(f"{channel_names[counter]}", url=f'https://t.me/{i}'))
                counter += 1
            button.add(types.InlineKeyboardButton(text="Obuna bo’ldim✅", callback_data="check_subs"))
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
            await message.answer('Davom etish uchun quyidagi kanalga obuna bo’ling ⬇️', reply_markup=button)
    else:
        try:
            user = await db.add_user(telegram_id=message.from_user.id,
                                     full_name=message.from_user.full_name,
                                     username=message.from_user.username
                                     )
        except asyncpg.exceptions.UniqueViolationError:
            user = await db.select_user(telegram_id=message.from_user.id)
        status = True
        all = await db.select_chanel()
        chanels = []
        url = []
        channel_names = []
        for i in all:
            chanels.append(i['chanelll'])
            url.append(i['url'])
            channel_names.append(i['channel_name'])

        for channel in chanels:
            status *= await subscription.check(user_id=message.from_user.id,
                                               channel=f'{channel}')
        if status:
            text = """
            Assalom aleykum, bu bot sizga Amerikada istiqomat qilib, yuridik faoliyat olib boruvchi malakali yuristlar jamoasidan bepul huquqiy maslahat olishga yordam beradi. \n\nChet elda o’qish bo’yicha tavsiyalar ham so’rashingiz mumkin.
            """
            await message.answer(text)
            text = f"""
            ❗️<b>Diqqat bilan o’qing!</b>\n\nHuquqiy maslahat olish va tavsiyalar so’rash 100% bepul. Faqat, huquqiy jihatdan yordamga muhtoj insonlarga bu loyihamiz yetib borishi uchun  sizning yordamingiz juda ham zarur!\n\nBot sizga taqdim etgan referral linkni atigi {limit_require} nafar do'stingizga yuboring va bizga murojaat qilish imkoniga ega bo'ling va bepul maslahat olasiz! \n\n<b>🔗 Taklif postini olish tugmani bosing va taklif qilishni boshlang 👇</b>"""
            await message.answer(text, reply_markup=menu)
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
            await message.answer('Davom etish uchun quyidagi kanalga obuna bo’ling ⬇️', reply_markup=button)


@dp.callback_query_handler(text="check_subs")
async def checker(call: types.CallbackQuery, state: FSMContext):
    status = True
    all = await db.select_chanel()
    chanels = []
    url = []
    channel_names = []
    for i in all:
        chanels.append(i['chanelll'])
        url.append(i['url'])
        channel_names.append(i['channel_name'])
    score = 0
    limit_require = 0
    elements = await db.get_elements()

    for element in elements:
        score += element['limit_score']
        limit_require += element['limit_require']

    elements = await db.get_elements()
    photo = ''
    gifts = ''
    for element in elements:
        photo += f"{element['photo']}"
        gifts += f"{element['gifts']}"

    for channel in chanels:
        status *= await subscription.check(user_id=call.from_user.id,
                                           channel=f'{channel}')
    if status:
        text = f"""
        ❗️<b>Diqqat bilan o’qing!</b>\n\nHuquqiy maslahat olish va tavsiyalar so’rash 100% bepul. Faqat, huquqiy jihatdan yordamga muhtoj insonlarga bu loyihamiz yetib borishi uchun  sizning yordamingiz juda ham zarur!\n\nBot sizga taqdim etgan referral linkni atigi {limit_require} nafar do'stingizga yuboring va bizga murojaat qilish imkoniga ega bo'ling va bepul maslahat olasiz! \n\n<b>🔗 Taklif postini olish tugmani bosing va taklif qilishni boshlang 👇</b>"""
        await call.message.answer(text, reply_markup=menu)

        try:
            if_old = await db.select_user(telegram_id=call.from_user.id)

            if if_old[5] == 0:
                args = await db.select_user(telegram_id=call.from_user.id)
                args = await db.select_user(telegram_id=call.from_user.id)
                args_user = await db.select_user(telegram_id=int(args[7]))
                update_score = int(args_user[4]) + score
                await db.update_user_score(score=update_score, telegram_id=int(args[7]))

                await bot.send_message(chat_id=int(args[7]),
                                       text=f"👤 Yangi ishtirokchi qo`shildi\n"
                                            f"🎗 Siz <b>{update_score}-ta</b> foydalanuvchi taklif qildingiz\n"
                                            f"🗣 Ko`proq do`stlaringizni taklif qiling!")
                await db.update_user_oldd(oldd=1, telegram_id=call.from_user.id)
        except Exception as e:
            print(e, 'check_sub')

        try:
            await call.message.delete()
        except Exception as e:
            pass
    else:
        button = types.InlineKeyboardMarkup(row_width=1, )

        counter = 0

        for i in url:
            button.add(types.InlineKeyboardButton(f"{channel_names[counter]}", url=f'https://t.me/{i}'))
            counter += 1
        button.add(types.InlineKeyboardButton(text="Obuna bo’ldim✅", callback_data="check_subs"))

        try:
            await call.answer(show_alert=True, text="⚠️ Kanallarga a'zo bo'lmadingiz")
        except Exception as e:
            pass


@dp.message_handler(text='dell')
async def delete_user(message: types.Message):
    await message.answer('Id ni kiriting')
    await DelState.del_user.set()


@dp.message_handler(state=DelState.del_user)
async def del_user(message: types.Message, state: FSMContext):
    await db.delete_users(telegram_id=int(message.text))
    await message.answer("O'chirildi")
    await state.finish()


@dp.message_handler(text='👤 Yurist bilan aloqa')
async def admin_profile(message: types.Message):
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
        user = await db.select_user(telegram_id=message.from_user.id)
        elements = await db.get_elements()
        limit_require = 0
        admin = ''
        for element in elements:
            limit_require += element['limit_require']
            admin += element['gifts']
        if user['score'] > limit_require - 1:
            await message.answer(
                f"👨🏻‍💻 {admin} - murojaat qilish uchun")
        else:
            url_link = f'https://t.me/huquqshunos_uz_bot?start={message.from_user.id}'
            lessons = await db.select_related_lessons(button_name="Asosiy qism")

            if lessons:
                for i in lessons:
                    if i[2] == 'video':
                        await message.answer_video(video=f"{i[3]}", caption=f'{i[5]}\n\n{url_link}')
                    elif i[2] == 'document':
                        await message.answer_document(
                            document=f"{i[3]}", caption=f'{i[5]}\n\n{url_link}'
                        )
                    elif i[2] == 'audio':
                        await message.answer_audio(audio=f"{i[3]}", caption=f"{i[5]}\n\n{url_link}")
                    elif i[2] == 'photo':
                        await message.answer_photo(photo=f"{i[3]}", caption=f"{i[5]}\n\n{url_link}")
                    elif i[2] == 'text':
                        await message.answer(f"{i[5]}\n\n{url_link}")
            elements = await db.get_elements()
            limit_require = 0
            admin = ''
            for element in elements:
                limit_require += element['limit_require']
                admin += element['gifts']

            await message.answer(
                f"<b>Yuqoridagi postni do'stlaringiz bilan ulashing. 👆</b>\n\n"
                f"<b>{limit_require} ta</b> do'stingiz sizning taklif havolingiz orqali bot'ga kirib kanallarga a'zo bo'lsa, bot avtomatik tarzda sizga bizga bog’lanish uchun imkon beradi. \n\n<b>Sizning murojaatingiz muhim ❗️\n\n"
                f"Sizda {user['score']} ball mavjud 🏆</b>")

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
        await message.answer('Davom etish uchun quyidagi kanalga obuna bo’ling ⬇️', reply_markup=button)


@dp.message_handler(text='🔗 Taklif postini olish')
async def referall(message: types.Message):
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

        url_link = f'https://t.me/course_by_native_speakers_bot?start={message.from_user.id}'
        text_link = f"<a href='{url_link}'>Bepul FULL IELTS kursi</a>"
        but = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Bepul FULL IELTS kursi 👨🏻‍💻", url=url_link)
                ]

            ]
        )

        lessons = await db.select_related_lessons(button_name="Asosiy qism")

        if lessons:
            for i in lessons:
                if i[2] == 'video':
                    await message.answer_video(video=f"{i[3]}", caption=f'{i[5]}\n\n{url_link}')
                elif i[2] == 'document':
                    await message.answer_document(
                        document=f"{i[3]}", caption=f'{i[5]}\n\n{url_link}'
                    )
                elif i[2] == 'audio':
                    await message.answer_audio(audio=f"{i[3]}", caption=f"{i[5]}\n\n{url_link}")
                elif i[2] == 'photo':
                    await message.answer_photo(photo=f"{i[3]}", caption=f"{i[5]}\n\n{url_link}")
                elif i[2] == 'text':
                    await message.answer(f"{i[5]}\n\n{url_link}")
        elements = await db.get_elements()
        limit_require = 0
        admin = ''
        for element in elements:
            limit_require += element['limit_require']
            admin += element['gifts']

        await message.answer(
            f"<b>👆 Yuqoridagi postni do'stlaringiz bilan ulashing.</b>\n\n"
            f"<b>{limit_require} ta</b> do'stingiz sizning taklif havolingiz orqali bot'ga kirib kanallarga a'zo bo'lsa, bot avtomatik tarzda sizga bizga bog’lanish uchun link beradi.\n\n<b>Sizning murojaatingiz muhim!</b>")

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
        await message.answer('Davom etish uchun quyidagi kanalga obuna bo’ling ⬇️', reply_markup=button)


@dp.message_handler(Command('jsonFile'))
async def jsonnn(message: types.Message):
    user_list = []
    userss = await db.select_all_users()
    for user in userss:
        user_dict = {}
        user_dict['full_name'] = user[1]
        user_dict['username'] = user[2]
        user_dict['phone'] = user[3]
        user_dict['score'] = user[4]
        user_dict['tg_id'] = user[6]
        user_list.append(user_dict)
        await asyncio.sleep(0.05)
    with open("users.json", "w") as outfile:
        json.dump(user_list, outfile)
    document = open('users.json')
    await bot.send_document(message.from_user.id, document=document)


async def send_json():
    user_list = []
    userss = await db.select_all_users()
    for user in userss:
        user_dict = {}
        user_dict['full_name'] = user[1]
        user_dict['username'] = user[2]
        user_dict['phone'] = user[3]
        user_dict['score'] = user[4]
        user_dict['tg_id'] = user[6]
        user_list.append(user_dict)
        await asyncio.sleep(0.05)
    with open("users.json", "w") as outfile:
        json.dump(user_list, outfile)
    document = open('users.json')
    await bot.send_document(935795577, document=document)


@dp.message_handler(Command('read_file'))
async def json_reader(message: types.Message):
    f = open('users.json', 'r')
    data = json.loads(f.read())
    for user in data:
        # print(user['tg_id'])
        try:
            user = await db.add_json_file_user(
                telegram_id=user['tg_id'],
                username=user['username'],
                full_name=user['full_name'],
                phone=user['phone'],
                score=user['score']
            )
        except Exception as e:
            print(e)
    f.close()
