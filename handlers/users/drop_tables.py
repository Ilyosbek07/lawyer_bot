from aiogram import types

from data.config import ADMINS
from loader import dp, db


@dp.message_handler(text="dropppp_users")
async def drop_req(message: types.Message):
    await db.drop_users()
    await db.create_table_users()
    await message.answer('Done ✅')
