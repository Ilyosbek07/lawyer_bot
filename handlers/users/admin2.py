import asyncio
from datetime import datetime, timedelta
from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.default.rekKeyboards import back, admin_key
from loader import dp, db, bot
from states.rekStates import RekData, AllState, Lesson, Number


@dp.message_handler(text='Admin ➕')
async def add_channel(message: types.Message):
    admins = await db.select_all_admins()
    admins_list = []
    for i in admins:
        admins_list.append(i[1])
    if message.from_user.id in admins_list:
        await message.answer('Id ni kiriting', reply_markup=back)
        await AllState.env.set()


@dp.message_handler(state=AllState.env)
async def env_change(message: types.Message, state: FSMContext):
    if message.text == '🔙️ Orqaga':
        await message.answer('Admin panel', reply_markup=admin_key)
        await state.finish()
    else:
        try:
            int(message.text)
        except ValueError:
            await message.answer('Faqat son qabul qilinadi\n\n'
                                 'Qaytadan kiriting')
        admins = await db.select_all_admins()
        admins_list = []
        for i in admins:
            admins_list.append(i[1])
        if int(message.text) in admins_list:
            await message.answer('Bunday admin mavjud')
        else:
            await db.add_admin(telegram_id=int(message.text))

            await message.answer(f"Qo'shildi\n\n", reply_markup=admin_key)
            await state.finish()


@dp.message_handler(text='Oylik miqdori')
async def add_channel(message: types.Message):
    admins = await db.select_all_admins()
    admins_list = []
    for i in admins:
        admins_list.append(i[1])
    if message.from_user.id in admins_list:
        await message.answer('Oylikni kiriting', reply_markup=back)
        await AllState.min_salary.set()


@dp.message_handler(state=AllState.min_salary)
async def env_change(message: types.Message, state: FSMContext):
    if message.text == '🔙️ Orqaga':
        await message.answer('Admin panel', reply_markup=admin_key)
        await state.finish()
    else:
        try:
            min_salary = int(message.text)
            await db.update_min_salary(min_salary=min_salary)

            await message.answer(f"Qo'shildi\n\n", reply_markup=admin_key)
            await state.finish()
        except ValueError:
            await message.answer('Faqat son qabul qilinadi\n\n'
                                 'Qaytadan kiriting')


@dp.message_handler(text='Admin ➖')
async def add_channel(message: types.Message):
    admins = await db.select_all_admins()
    admins_list = []
    for i in admins:
        admins_list.append(i[1])
    if message.from_user.id in admins_list:
        await message.answer('Id ni kiriting', reply_markup=back)
        await AllState.env_remove.set()


@dp.message_handler(state=AllState.env_remove)
async def env_change(message: types.Message, state: FSMContext):
    if message.text == '🔙️ Orqaga':
        await message.answer('Admin panel', reply_markup=admin_key)
        await state.finish()
    else:
        try:
            admins = await db.select_all_admins()
            admins_list = []
            for i in admins:
                admins_list.append(i[1])
            if int(message.text) in admins_list:
                await db.delete_admins(telegram_id=int(message.text))
                admins2 = await db.select_all_admins()
                admins_list2 = []
                for i in admins2:
                    admins_list2.append(i[1])

                await message.answer(f'O"chirildi\n\n'
                                     f'Hozirgi adminlar {admins_list2}', reply_markup=admin_key)
                await state.finish()
            else:
                await message.answer('Bunday admin mavjud emas\n\n'
                                     'Faqat admin id sini qabul qilamiz')
        except Exception as err:
            await message.answer(f'{err}')
            await message.answer('Faqat son qabul qilinadi\n\n'
                                 'Qaytadan kiriting')


@dp.message_handler(text='Barcha Adminlar')
async def add_channel(message: types.Message):
    admins = await db.select_all_admins()
    admins_list = []
    for i in admins:
        admins_list.append(i[1])
    await message.answer(f'Adminlar - {admins_list}', reply_markup=admin_key)


@dp.message_handler(commands=['admin'])
async def admin(message: types.Message):
    admins = await db.select_all_admins()
    admins_list = []
    for i in admins:
        admins_list.append(i[1])
    if message.from_user.id in admins_list:
        await message.answer(text='Admin panel',
                             reply_markup=admin_key)


@dp.message_handler(text='Kanal ➕')
async def add_channel(message: types.Message):
    admins = await db.select_all_admins()
    admins_list = []
    for i in admins:
        admins_list.append(i[1])
    if message.from_user.id in admins_list:
        await message.answer(text='Kanalni kiriting\n\n'
                                  'Masalan : "@Chanel,addlist zayavkada bo`lsa chanel_id(-123123213),chanel_url"\n\n',
                             reply_markup=back)
        await RekData.add.set()


@dp.message_handler(state=RekData.add)
async def add_username(message: types.Message, state: FSMContext):
    text = message.text
    if text[0] == '@':
        text_split = text.split(',')
        await db.add_chanell(chanelll=f"{text_split[0]}",
                             channel_name=f"{text_split[1]}", url=f"{text_split[0][1:]}")
        await message.answer("Qo'shildi", reply_markup=admin_key)
        await state.finish()
    elif text == '🔙️ Orqaga':
        await message.answer('Admin panel', reply_markup=admin_key)
        await state.finish()
    elif text[0] == '-':
        split_chanel = message.text.split(',')
        chanel_lst = []
        url_lst = []
        channel_name_lst = []
        for i in split_chanel:
            lst = i.split('and')
            chanel_lst.append(lst[0])
            url_lst.append(lst[1])
            channel_name_lst.append(lst[2])
        chanel = f'{chanel_lst}'
        url = f'{url_lst}'
        channel_name = f'{url_lst}'
        ch_text = chanel.replace("'", '')
        ch_text2 = ch_text.replace(" ", '')
        u_text = url.replace("'", '')
        u_text2 = u_text.replace(" ", '')
        channel_name_text = channel_name.replace("'", '')
        channel_name_text2 = channel_name_text.replace(" ", '')

        await db.add_chanell(chanelll=ch_text2[1:-1], url=u_text2[1:-1], channel_name=channel_name_text2[1:-1])
        await message.answer("Qo'shildi", reply_markup=admin_key)
        await state.finish()

    else:
        await message.answer('Xato\n\n'
                             '@ belgi bilan yoki kanal id(-11001835334270andLink) sini link bilan birga kiriting kiriting')


@dp.message_handler(text='Kanal ➖')
async def add_channel(message: types.Message):
    admins = await db.select_all_admins()
    admins_list = []
    for i in admins:
        admins_list.append(i[1])
    if message.from_user.id in admins_list:
        await message.answer(text='Kanalni kiriting @ belgi bilan\n\n'
                                  'Masalan : "Kanal zayavkada bo`lsa chanel_id(-123123213),chanel_url"\n\n',
                             reply_markup=back)
        await RekData.delete.set()


@dp.message_handler(state=RekData.delete)
async def del_username(message: types.Message, state: FSMContext):
    txt = message.text
    if txt[0] == '-':
        chanel = await db.get_chanel(channel=txt)
        if not chanel:
            await message.answer("Kanal topilmadi\n"
                                 "Qaytadan urinib ko'ring")

        else:
            await db.delete_channel(chanel=txt)
            await message.answer('Kanal o"chirildi', reply_markup=admin_key)
            await state.finish()

        # await message.answer("O'chirildi")
        # await state.finish()
    elif txt[0] == '@':
        chanel = await db.get_chanel(channel=f"{txt}")
        if not chanel:
            await message.answer("Kanal topilmadi\n"
                                 "Qaytadan urinib ko'ring")

        else:
            await db.delete_channel(chanel=txt)
            await message.answer('Kanal o"chirildi', reply_markup=admin_key)
            await state.finish()
    elif txt == '🔙️ Orqaga':
        await message.answer('Admin panel', reply_markup=admin_key)
        await state.finish()


activee = 0
blockk = 0


async def is_activeee():
    users = await db.select_all_users()
    global activee
    global blockk
    activate_test = 0
    blockk_test = 0
    # activee = 0
    # blockk = 0
    for user in users:

        user_id = user[6]
        try:
            await bot.send_chat_action(chat_id=user_id, action='typing')
            activate_test += 1
            await asyncio.sleep(0.034)

        except Exception as err:
            blockk_test += 1
            await asyncio.sleep(0.034)
    activee = activate_test
    blockk = blockk_test


@dp.message_handler(text='ttt')
async def is_activeee(a=None):
    users = await db.select_all_users()
    global activee
    global blockk
    activate_test = 0
    blockk_test = 0
    # activee = 0
    # blockk = 0
    for user in users:
        user_id = user[6]
        try:
            await bot.send_chat_action(chat_id=user_id, action='typing')
            activate_test += 1
            await asyncio.sleep(0.034)

        except Exception as err:
            blockk_test += 1
            await asyncio.sleep(0.034)
    activee = activate_test
    blockk = blockk_test


@dp.message_handler(text='Statistika 📊')
async def show_users(message: types.Message):
    a = await db.count_users()
    global activee
    global blockk

    await message.answer(f'<b>🔵 Jami obunachilar: {a} ta\n\n'
                         f'🟡 Active: {activee}\n'
                         f'⚫️ Block : {blockk}</b>')


@dp.message_handler(text='🏘 Bosh menu')
async def menuu(message: types.Message):
    await message.answer('Bosh menu')


@dp.message_handler(text='Kanallar 📈')
async def channels(message: types.Message):
    channels = await db.select_chanel()
    text = ''
    for channel in channels:
        text += f"{channel['chanelll']}\n"
    try:
        await message.answer(f"{text}", reply_markup=admin_key)
    except:
        await message.answer(f"Kanallar mavjud emas")


@dp.message_handler(text='Rasmni almashtirish 🖼')
async def change_picture(message: types.Message):
    admins = await db.select_all_admins()
    admins_list = []
    for i in admins:
        admins_list.append(i[1])
    if message.from_user.id in admins_list:
        await message.answer('Rasmni kiriting', reply_markup=back)
        await RekData.picture.set()


@dp.message_handler(content_types=['photo', 'text', 'video'], state=RekData.picture)
async def change_picture_(message: types.Message, state: FSMContext):
    admins = await db.select_all_admins()
    admins_list = []
    for i in admins:
        admins_list.append(i[1])
    if message.from_user.id in admins_list:
        if message.photo:
            photo = message.photo[-1].file_id
            elements = await db.get_elements()
            if elements:
                await db.update_photo(photo=photo)
                await message.answer('Yangilandi', reply_markup=admin_key)
                await state.finish()

            else:
                await db.add_photo(photo=photo)
                await message.answer('Qo`shildi', reply_markup=admin_key)
                await state.finish()

        elif message.text == '🔙️ Orqaga':
            await message.answer('Bosh menu')
            await state.finish()
        elif message.text == '/start':
            await message.answer('Bosh menu')
            await state.finish()

        else:
            await message.answer('Faqat rasm qabul qilamiz')


@dp.message_handler(text="O'yin haqida matn 🎮")
async def change_picture(message: types.Message):
    global admins
    if message.from_user.id in admins:
        await message.answer('Textni kiriting', reply_markup=back)
        await RekData.text.set()


@dp.message_handler(state=RekData.text)
async def change_picture_(message: types.Message, state: FSMContext):
    if message.text:
        elements = await db.get_elements()
        if elements:
            await db.update_game_text(game_text=message.text)
            await message.answer('Yangilandi', reply_markup=admin_key)
            await state.finish()
        elif message.text == '/start':
            await message.answer('Bosh menu')
            await state.finish()

        elif message.text == '🔙️ Orqaga':
            await message.answer('Bosh menu')
            await state.finish()

        else:
            await db.add_text(game_text=message.text)
            await message.answer('Qo`shildi', reply_markup=admin_key)
            await state.finish()
    else:
        await message.answer('Faqat Text qabul qilamiz')


@dp.message_handler(text="Referall Content")
async def change_picture(message: types.Message):
    admins = await db.select_all_admins()
    admins_list = []
    for i in admins:
        admins_list.append(i[1])
    if message.from_user.id in admins_list:
        await message.answer('Yuboring', reply_markup=back)
        await RekData.main_content.set()


@dp.message_handler(text="Adminni kiriting")
async def change_picture(message: types.Message):
    admins = await db.select_all_admins()
    admins_list = []
    for i in admins:
        admins_list.append(i[1])
    if message.from_user.id in admins_list:
        await message.answer('Yuboring', reply_markup=back)
        await RekData.gift.set()


@dp.message_handler(state=RekData.gift)
async def change_picture_(message: types.Message, state: FSMContext):
    if message.text:
        elements = await db.get_elements()
        if elements:
            await db.update_gift(gift=message.text)
            await message.answer('Yangilandi', reply_markup=admin_key)
            await state.finish()
        elif message.text == '/start':
            await message.answer('Bosh menu')
            await state.finish()

        else:
            await db.add_gift(gift=message.text)
            await message.answer('Qo`shildi', reply_markup=admin_key)
            await state.finish()

    elif message.text == '🔙️ Orqaga':
        await message.answer('Bosh menu')
        await state.finish()
    else:
        await message.answer('Faqat Text qabul qilamiz')


@dp.message_handler(text="Taklif miqdorini kiritish")
async def change_picture(message: types.Message):
    admins = await db.select_all_admins()
    admins_list = []
    for i in admins:
        admins_list.append(i[1])
    if message.from_user.id in admins_list:
        await message.answer('Faqat son kiriting', reply_markup=back)
        await RekData.score.set()


@dp.message_handler(state=RekData.score)
async def change_picture_(message: types.Message, state: FSMContext):
    try:
        text = int(message.text)

        if text:
            elements = await db.get_elements()
            if elements:
                await db.update_limit_score(limit_score=text)
                await message.answer('Yangilandi', reply_markup=admin_key)
                await state.finish()
        elif message.text == '/start':
            await message.answer('Bosh menu')
            await state.finish()

    except Exception as err:
        print(err)
        if message.text == '/start':
            await message.answer('Bosh menu')
            await state.finish()

        if message.text == '🔙️ Orqaga':
            await message.answer('Bosh menu', reply_markup=admin_key)
            await state.finish()
        else:
            await message.answer('Faqat Son qabul qilamiz')


@dp.message_handler(text="Taklif chegarasini kiritish")
async def limit_count(message: types.Message):
    admins = await db.select_all_admins()
    admins_list = []
    for i in admins:
        admins_list.append(i[1])
    if message.from_user.id in admins_list:
        await message.answer('Faqat son kiriting', reply_markup=back)
        await RekData.limit.set()


@dp.message_handler(state=RekData.limit)
async def limit(message: types.Message, state: FSMContext):
    try:
        text = int(message.text)

        if text:
            elements = await db.get_elements()
            if elements:
                await db.update_limit_require(limit_require=text)
                await message.answer('Yangilandi', reply_markup=admin_key)
                await state.finish()
            # else:
            # await db.add_text()
        elif message.text == '/start':
            await message.answer('Bosh menu')
            await state.finish()

        elif message.text == '🔙️ Orqaga':
            await message.answer('Bosh menu')
            await state.finish()
    except:
        if message.text == '/start':
            await message.answer('Bosh menu')
            await state.finish()

        if message.text == '🔙️ Orqaga':
            await message.answer('Bosh menu')
            await state.finish()
        else:
            await message.answer('Faqat Son qabul qilamiz')


@dp.message_handler(text="Hisobni 0 ga tushirish")
async def change_picture(message: types.Message):
    await message.answer('Aniqmi', reply_markup=back)
    await RekData.winners.set()


@dp.message_handler(state=RekData.winners)
async def change_picture_(message: types.Message, state: FSMContext):
    if message.text == '🔙️ Orqaga':
        await message.answer('Bosh menu')
        await state.finish()
    elif message.text == '/start':
        await message.answer('Bosh menu')
        await state.finish()
    elif message.text == 'Ha':
        await db.update_users_all_score()
        await message.answer('Hisob 0 ga tushirildi')
    else:
        await message.answer('Bekor qilindi')
        await state.finish()


@dp.message_handler(text='link 1')
async def show_channels(message: types.Message, state: FSMContext):
    expire_date = datetime.now() + timedelta(minutes=1)
    invitee_link = await bot.create_chat_invite_link(chat_id=-1001924263164, member_limit=1,
                                                     expire_date=expire_date)
    await bot.send_message(chat_id=message.from_user.id, text=invitee_link.invite_link, protect_content=True)


@dp.message_handler(text='link berish')
async def show_channels(message: types.Message, state: FSMContext):
    await message.answer('boshlandi')
    if_getter_link_user = await db.select_all_users()
    for i in if_getter_link_user:
        try:
            if int(i[4]) > 1:
                await bot.send_message(chat_id=i[6], text='https://t.me/+XciKZBFCH2k3OTE6', protect_content=True)
                await asyncio.sleep(0.05)
        except Exception as err:
            print(err)
    await message.answer('tugadi')


@dp.message_handler(text="Barcha ma'lumotlarni tozalash")
async def drop_lessons_db(message: types.Message):
    await db.drop_lessons()
    await db.create_table_lessons()
    await message.answer("Tozalandi")


@dp.message_handler(text='Remove File')
async def add_channel(message: types.Message):
    await message.answer(
        text="Barcha ma'lumotlar o'chadi\n\nBarchasiga rozimisiz\n\nHa bo'lsa file_unique_id ni kiriting",
        reply_markup=back
    )
    await Lesson.les_del.set()


@dp.message_handler(state=Lesson.les_del)
async def del_button(message: types.Message, state: FSMContext):
    txt = message.text
    unique_id = []

    lessons = await db.select_lessons()
    for i in lessons:
        unique_id.append(i['file_unique_id'])
    for lesson in lessons:
        unique_id.append(lesson[3])
    if txt == '🔙️ Orqaga':
        await message.answer('Admin panel', reply_markup=admin_key)
        await state.finish()
    elif message.text in unique_id:
        try:
            await db.delete_lesson(file_unique_id=message.text)
            await message.answer("O'chirildi", reply_markup=admin_key)
            await state.finish()
        except Exception as err:
            print(err)
            await message.answer('Bunday ma`lumot topilmadi')
    else:
        await message.answer('Xato\n\nBunday id yo`q\n\nChiqish uchun orqaga tugmasini bosing')
