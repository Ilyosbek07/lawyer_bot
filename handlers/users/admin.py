import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import ADMINS
from keyboards.default.rekKeyboards import back, admin_key
from loader import dp, db
from states.rekStates import RekData


@dp.message_handler(text='Post Yuborish 🗒')
async def bot_start(msg: types.Message):
    await msg.answer("<b>Xabarni yuboring</b>", reply_markup=back)
    await RekData.choice.set()


@dp.message_handler(content_types=['video', 'audio', 'voice', 'photo', 'document', 'text'],
                    state=RekData.choice)
async def contumum(msg: types.Message, state: FSMContext):
    if msg.text == '🔙️ Orqaga':
        await msg.answer('Bekor qilindi', reply_markup=admin_key)
        await state.finish()

    elif msg.video or msg.audio or msg.voice or msg.document or msg.photo or msg.text:
        if msg.text == 'Barchaga Xabar Yuborish 🗒':
            await msg.answer('Adashdingiz Shekilli\n\n'
                             'To`g`ri ma`lumot kirting')
        else:
            await state.finish()

            users = await db.select_all_users()
            count_baza = await db.count_users()
            count_err = 0
            count = 0
            await msg.answer('Xabar yuborish boshlandi.')
            for user in users:
                user_id = user[6]
                try:
                    await msg.send_copy(chat_id=user_id)
                    count += 1
                    await asyncio.sleep(0.05)
                except Exception as err:
                    count_err += 1
                    await asyncio.sleep(0.05)
                    continue

            await msg.answer(f"Ҳабар юборилганлар: <b>{count}</b> та."
                             f"\n\nЮборилмаганлар: <b>{count_err}</b> та."
                             f"\n\nБазада жами: <b>{count_baza}</b> та"
                             f" фойдаланувчи мавжуд.", reply_markup=admin_key
                             )



@dp.message_handler(state='*')
async def back_all(message: types.Message, state: FSMContext):
    if message.text == 'Back':
        await message.answer(text='Bosh menu')
        await state.finish()
