from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:

    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        username varchar(255) NULL,
        phone varchar(55),
        score INT DEFAULT 0,
        oldd INT DEFAULT 0,
        telegram_id BIGINT NOT NULL UNIQUE,
        user_args varchar(55) NULL
        );
        """
        await self.execute(sql, execute=True)

    async def create_table_chanel(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Channel (
        id SERIAL PRIMARY KEY,
        chanelll VARCHAR(301) NOT NULL,
        url varchar(301) NOT NULL,
        channel_name TEXT NULL
                );
        """
        await self.execute(sql, execute=True)

    async def create_table_admins(self):
        sql = """
        CREATE TABLE IF NOT EXISTS admins (
        id SERIAL PRIMARY KEY,
        telegram_id BIGINT NOT NULL UNIQUE
        );
        """
        await self.execute(sql, execute=True)

    async def create_table_chanel_element(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Elementt (
        id SERIAL PRIMARY KEY,
        photo TEXT NULL,
        gifts TEXT NULL,
        game_text TEXT NULL,
        shartlar TEXT NULL,
        min_salary INT DEFAULT 1,
        one_child INT DEFAULT 1,
        two_children INT DEFAULT 1,
        three_children INT DEFAULT 1,
        first_min INT DEFAULT 1,
        second_min INT DEFAULT 1,
        three_min INT DEFAULT 1,
        limit_require INT DEFAULT 5,
        winners INT DEFAULT 20,
        bot_url varchar(255)
                );
        """
        await self.execute(sql, execute=True)

    async def create_table_buttons(self):
        sql = """
        CREATE TABLE IF NOT EXISTS buttons (
        id SERIAL PRIMARY KEY,
        button_name VARCHAR(301) NOT NULL
                );
        """
        await self.execute(sql, execute=True)

    async def create_table_lessons(self):
        sql = """
        CREATE TABLE IF NOT EXISTS lessons (
        id SERIAL PRIMARY KEY,
        button_name VARCHAR(301) NOT NULL,
        type VARCHAR(301) NOT NULL,
        file_id VARCHAR(301) NULL,
        file_unique_id VARCHAR(301) NOT NULL,
        description TEXT NULL 
                );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_user(self, full_name, telegram_id, username):
        sql = "INSERT INTO users (full_name, telegram_id, username) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, full_name, telegram_id, username, fetchrow=True)

    async def add_userrr(self, full_name, telegram_id, username, phone, score):
        sql = "INSERT INTO users (full_name, telegram_id, username, phone, score) VALUES($1, $2, $3, $4, $5) returning *"
        return await self.execute(sql, full_name, telegram_id, username, phone, score, fetchrow=True)

    async def add_userr(self, full_name, telegram_id, username, score):
        sql = "INSERT INTO users (full_name, telegram_id, username, score) VALUES($1, $2, $3,$4) returning *"
        return await self.execute(sql, full_name, telegram_id, username, score, fetchrow=True)

    async def add_lesson_text(self, button_name, type, file_unique_id, description):
        sql = "INSERT INTO lessons (button_name,type,file_unique_id,description) VALUES($1,$2,$3,$4) returning *"
        return await self.execute(sql, button_name, type, file_unique_id, description, fetchrow=True)

    async def add_json_file_user(self, full_name, username, phone, telegram_id, score):
        sql = "INSERT INTO users (full_name, username, phone, telegram_id, score) VALUES($1, $2, $3,$4,$5) returning *"
        return await self.execute(sql, full_name, username, phone, telegram_id, score, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def select_top_users(self, lim_win):
        sql = f"SELECT * FROM Users WHERE score IS NOT NULL ORDER BY score DESC LIMIT {lim_win}"
        return await self.execute(sql, fetch=True)

    async def select_top_users_list(self):
        sql = f"SELECT * FROM Users WHERE score IS NOT NULL ORDER BY score DESC"
        return await self.execute(sql, fetch=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)

    async def update_user_name(self, name, telegram_id):
        sql = "UPDATE Users SET full_name=$1 WHERE telegram_id=$2"
        return await self.execute(sql, name, telegram_id, execute=True)

    async def update_user_username(self, username, telegram_id):
        sql = "UPDATE Users SET username=$1 WHERE telegram_id=$2"
        return await self.execute(sql, username, telegram_id, execute=True)

    async def update_user_oldd(self, oldd, telegram_id):
        sql = "UPDATE Users SET oldd=$1 WHERE telegram_id=$2"
        return await self.execute(sql, oldd, telegram_id, execute=True)

    async def update_user_args(self, user_args, telegram_id):
        sql = "UPDATE Users SET user_args=$1 WHERE telegram_id=$2"
        return await self.execute(sql, user_args, telegram_id, execute=True)

    async def update_user_phone(self, phone, telegram_id):
        sql = "UPDATE Users SET phone=$1 WHERE telegram_id=$2"
        return await self.execute(sql, phone, telegram_id, execute=True)

    async def update_user_score(self, score, telegram_id):
        sql = "UPDATE Users SET score=$1 WHERE telegram_id=$2"
        return await self.execute(sql, score, telegram_id, execute=True)

    async def update_users_all_score(self):
        sql = "UPDATE Users SET score=0"
        return await self.execute(sql, execute=True)

    async def delete_users(self, telegram_id):
        sql = "DELETE FROM Users WHERE telegram_id=$1"
        await self.execute(sql, telegram_id, execute=True)

    async def delete_admin(self, admin_id):
        sql = "DELETE FROM admins WHERE admin_id=$1"
        await self.execute(sql, admin_id, execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE Users", execute=True)

    async def delete_channel(self, chanel):
        sql = "DELETE FROM Channel WHERE chanelll=$1"
        await self.execute(sql, chanel, execute=True)

    async def select_chanel(self):
        sql = "SELECT * FROM Channel"
        return await self.execute(sql, fetch=True)

    async def add_chanell(self, chanelll, url, channel_name):
        sql = "INSERT INTO Channel (chanelll, url,channel_name) VALUES($1, $2,$3) returning *"
        return await self.execute(sql, chanelll, url, channel_name, fetchrow=True)

    async def get_chanel(self, channel):
        sql = f"SELECT * FROM Channel WHERE chanelll=$1"
        return await self.execute(sql, channel, fetch=True)

    async def get_admins(self):
        sql = f"SELECT * FROM admins"
        return await self.execute(sql, fetch=True)

    async def drop_Chanel(self):
        await self.execute("DROP TABLE Channel", execute=True)

    async def delete_channel(self, chanel):
        sql = "DELETE FROM Channel WHERE chanelll=$1"
        await self.execute(sql, chanel, execute=True)

    async def select_chanel(self):
        sql = "SELECT * FROM Channel"
        return await self.execute(sql, fetch=True)

    async def add_photo(self, photo):
        sql = "INSERT INTO Elementt (photo) VALUES($1) returning *"
        return await self.execute(sql, photo, fetchrow=True)

    async def add_gift(self, gift):
        sql = "INSERT INTO Elementt (gifts) VALUES($1) returning *"
        return await self.execute(sql, gift, fetchrow=True)

    async def add_shartlar(self, shartlar):
        sql = "INSERT INTO Elementt (shartlar) VALUES($1) returning *"
        return await self.execute(sql, shartlar, fetchrow=True)

    async def add_text(self, bot_url):
        sql = "INSERT INTO Elementt (bot_url) VALUES($1) returning *"
        return await self.execute(sql, bot_url, fetchrow=True)

    async def add_bot_url(self, bot_url):
        sql = "INSERT INTO Elementt (bot_url) VALUES($1) returning *"
        return await self.execute(sql, bot_url, fetchrow=True)

    async def update_photo(self, photo):
        sql = "UPDATE Elementt SET photo=$1 WHERE id=1"
        return await self.execute(sql, photo, execute=True)

    async def update_limit_score(self, limit_score):
        sql = "UPDATE Elementt SET limit_score=$1 WHERE id=1"
        return await self.execute(sql, limit_score, execute=True)

    async def update_min_salary(self, min_salary):
        sql = "UPDATE Elementt SET min_salary=$1 WHERE id=1"
        return await self.execute(sql, min_salary, execute=True)

    async def update_first_min(self, first_min):
        sql = "UPDATE Elementt SET first_min=$1 WHERE id=1"
        return await self.execute(sql, first_min, execute=True)

    async def update_second_min(self, second_min):
        sql = "UPDATE Elementt SET second_min=$1 WHERE id=1"
        return await self.execute(sql, second_min, execute=True)

    async def update_three_min(self, three_min):
        sql = "UPDATE Elementt SET three_min=$1 WHERE id=1"
        return await self.execute(sql, three_min, execute=True)

    async def update_one_child(self, one_child):
        sql = "UPDATE Elementt SET one_child=$1 WHERE id=1"
        return await self.execute(sql, one_child, execute=True)

    async def update_two_children(self, two_children):
        sql = "UPDATE Elementt SET two_children=$1 WHERE id=1"
        return await self.execute(sql, two_children, execute=True)

    async def update_three_children(self, three_children):
        sql = "UPDATE Elementt SET three_children=$1 WHERE id=1"
        return await self.execute(sql, three_children, execute=True)

    async def update_limit_require(self, limit_require):
        sql = "UPDATE Elementt SET limit_require=$1 WHERE id=1"
        return await self.execute(sql, limit_require, execute=True)

    async def winners(self, winners):
        sql = "UPDATE Elementt SET winners=$1 WHERE id=1"
        return await self.execute(sql, winners, execute=True)

    async def update_game_text(self, game_text):
        sql = "UPDATE Elementt SET game_text=$1 WHERE id=1"
        return await self.execute(sql, game_text, execute=True)

    async def bot_url(self, bot_url):
        sql = "UPDATE Elementt SET bot_url=$1 WHERE id=1"
        return await self.execute(sql, bot_url, execute=True)

    async def update_gift(self, gift):
        sql = "UPDATE Elementt SET gifts=$1 WHERE id=1"
        return await self.execute(sql, gift, execute=True)

    async def update_shartlar(self, shartlar):
        sql = "UPDATE Elementt SET shartlar=$1 WHERE id=1"
        return await self.execute(sql, shartlar, execute=True)

    async def get_elements(self):
        sql = f"SELECT * FROM Elementt WHERE id=1"
        return await self.execute(sql, fetch=True)

    async def drop_elements(self):
        await self.execute("DROP TABLE Elementt", execute=True)

    async def drop_lessons(self):
        await self.execute("DROP TABLE lessons", execute=True)

    ### Lessons DB Commands
    async def add_button(self, button_name):
        sql = "INSERT INTO buttons (button_name) VALUES($1) returning *"
        return await self.execute(sql, button_name, fetchrow=True)

    async def delete_button_name(self, button_name):
        sql = "DELETE FROM buttons WHERE button_name=$1"
        await self.execute(sql, button_name, execute=True)

    async def select_buttons(self):
        sql = "SELECT * FROM buttons"
        return await self.execute(sql, fetch=True)

    async def add_lesson(self, button_name, type, file_id, file_unique_id, description=None):
        sql = "INSERT INTO lessons (button_name,type,file_id,file_unique_id,description) VALUES($1,$2,$3,$4,$5) returning *"
        return await self.execute(sql, button_name, type, file_id, file_unique_id, description, fetchrow=True)

    async def delete_lesson(self, file_unique_id):
        sql = "DELETE FROM lessons WHERE file_unique_id=$1"
        await self.execute(sql, file_unique_id, execute=True)

    async def delete_related_lesson(self, button_name):
        sql = "DELETE FROM lessons WHERE button_name=$1"
        await self.execute(sql, button_name, execute=True)

    async def select_lessons(self):
        sql = "SELECT * FROM lessons"
        return await self.execute(sql, fetch=True)

    async def select_related_lessons(self, button_name):
        sql = "SELECT * FROM lessons WHERE button_name=$1"
        return await self.execute(sql, button_name, fetch=True)

    async def add_admin(self, telegram_id):
        sql = "INSERT INTO admins (telegram_id) VALUES($1) returning *"
        return await self.execute(sql, telegram_id, fetchrow=True)

    async def select_all_admins(self):
        sql = "SELECT * FROM admins"
        return await self.execute(sql, fetch=True)

    async def delete_admins(self, telegram_id):
        sql = "DELETE FROM admins WHERE telegram_id=$1"
        await self.execute(sql, telegram_id, execute=True)

    async def drop_admins(self):
        await self.execute("DROP TABLE admins", execute=True)
