import asyncio
from aiogram.utils import executor
from jira import Issue

import handlers
from all_functions import request_all_tasks
from db_file import cur
from bugs_bot import dp, startup


def main():
    issue: Issue = request_all_tasks()
    print(issue.fields.issuetype)
    cur.execute("SELECT key FROM issues ORDER BY id DESC LIMIT 1;")
    f"INSERT INTO issues (key) VALUES ({issue.key}"
    last_bug_key = cur.fetchone()[0]
    print(last_bug_key, issue.key)
    if issue.key == last_bug_key:
        print("Last issue is - ", last_bug_key)


if __name__ == '__main__':
    executor.start_polling(skip_updates=True, dispatcher=dp, on_startup=startup)
