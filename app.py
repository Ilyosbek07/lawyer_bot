from aiogram import executor

from loader import dp, db
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    await db.create()
    await db.create_table_chanel()
    await db.create_table_admins()
    await db.create_table_users()
    await db.create_table_lessons()
    await db.create_table_buttons()
    await db.create_table_chanel_element()
    await set_default_commands(dispatcher)
    await on_startup_notify(dispatcher)
    admins = await db.select_all_admins()
    try:
        if 935795577 == admins[0][1]:
            print('>>> qo`shilgan')
            print(f'>>> Hozirgi adminlar - {admins}')
    except Exception as err:
        print(err)
        await db.add_admin(telegram_id=935795577)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
