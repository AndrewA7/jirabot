from __future__ import annotations
import asyncio
import sqlite3

from aiogram import Bot, Dispatcher

from all_functions import request_last_task, request_all_tasks, truncate_table, tasks_in_db
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
        await truncate_table()




async def schedule_all_bugs(*args, **kwargs):
    while True:
        await asyncio.sleep(500)
        await request_all_tasks()
        await truncate_table()
        await tasks_in_db()


async def startup(*args, **kwargs):
    asyncio.create_task(schedule_all_bugs())
    asyncio.create_task(schedule_last_bug())

