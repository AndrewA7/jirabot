from __future__ import annotations
import asyncio
import sqlite3

from aiogram import Bot, Dispatcher

from all_functions import request_last_task, request_all_tasks, truncate_table, tasks_in_db, does_bot_working
from config import TELEGRAM_TOKEN, LINK_TO_JIRA, JIRA_API_TOKEN, LOGIN
from jira import JIRA

jira = JIRA(basic_auth=(LOGIN, JIRA_API_TOKEN), server=LINK_TO_JIRA)
boards = jira.boards()

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

conn = sqlite3.connect(database="jira_database.sqlite", check_same_thread=False)
cur = conn.cursor()

cur.execute("")


async def schedule_last_bug(*args, **kwargs):
    while True:
        await request_last_task()
        await asyncio.sleep(10)
        # await tasks_in_db()


async def schedule_all_bugs(*args, **kwargs):
    while True:
        # await request_last_task()
        await request_all_tasks()
        await truncate_table()
        await asyncio.sleep(10)


async def print_data_in_db(*args, **kwargs):
    while True:
        await tasks_in_db()
        await asyncio.sleep(300)


async def bot_checking(*args, **kwargs):
    while True:
        await asyncio.sleep(3600)
        await does_bot_working()



async def startup(*args, **kwargs):
    asyncio.create_task(schedule_all_bugs())
    asyncio.create_task(print_data_in_db())
    asyncio.create_task(schedule_last_bug())
    asyncio.create_task(bot_checking())


