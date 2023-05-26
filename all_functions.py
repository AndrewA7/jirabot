import sqlite3

from aiogram import Bot
from aiogram.types import ParseMode

from config import LINK_TO_JIRA, JIRA_API_TOKEN, LOGIN, CURRENT_STREAM, TASK_TYPE, TASK_STATUS, TELEGRAM_TOKEN, CHAT_ID
from jira import JIRA

jira = JIRA(basic_auth=(LOGIN, JIRA_API_TOKEN), server=LINK_TO_JIRA)
bot = Bot(token=TELEGRAM_TOKEN)
conn = sqlite3.connect(database="jira_database.sqlite", check_same_thread=False)
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS db_jira_issues (task_key STR, task_summary STR, "
            "task_type STR, task_status STR, task_reporter STR)")
last_issue = ""


async def tasks_in_db():
    cur.execute("SELECT key FROM issues;")
    conn.commit()
    print(f"Tasks in DB - {[x[0] for x in cur.fetchall()]}")


async def request_all_tasks():
    cur.execute("SELECT key FROM issues;")
    list_of_issues = [x[0] for x in cur.fetchall()]
    for singleIssue in jira.search_issues(jql_str=f"project = {CURRENT_STREAM} AND type = {TASK_TYPE} "
                                                  f"AND status IN {TASK_STATUS} ORDER BY updated DESC, created DESC",
                                          maxResults=20):
        if singleIssue.key not in list_of_issues:
            message = f"<b>We have one more bug</b> \n" \
                              f"<a href = 'https://ajaxsystems.atlassian.net/jira/software/c/projects/INTRUSION/" \
                              f"issues/{singleIssue.key}/'" \
                              f">{singleIssue.fields.summary}</a> \n" \
                              f"<i>Author: {singleIssue.fields.reporter.displayName}</i> \n" \
                              f"<i>Status: {singleIssue.fields.status}</i>"
            await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode=ParseMode.HTML,
                                   disable_web_page_preview=True)
            # await request_last_task()


        # list_of_issues.append(singleIssue.key)
        # cur.execute(f"INSERT INTO issues (key) VALUES (\"{singleIssue.key}\");")
        # conn.commit()


async def truncate_table():
    cur.execute("DELETE FROM issues;")
    conn.commit()

    for singleIssue in jira.search_issues(jql_str=f"project = {CURRENT_STREAM} AND type = {TASK_TYPE} "
                                                  f"AND status IN {TASK_STATUS} ORDER BY updated DESC, created DESC",
                                          maxResults=50):
        cur.execute(f"REPLACE INTO issues (key) VALUES (\"{singleIssue.key}\");")
    conn.commit()


async def request_last_task():
    global last_issue
    for singleIssue in jira.search_issues(jql_str=f"project = {CURRENT_STREAM} AND type = {TASK_TYPE} "
                                                  f"AND status IN {TASK_STATUS} ORDER BY updated DESC, created DESC",
                                          maxResults=1):
        if singleIssue.key != last_issue:
            print(f"last issue is {singleIssue.key}, type - {singleIssue.fields.issuetype}")
            last_issue = singleIssue.key


async def does_bot_working():
    print("-------------diagnostic started--------------")
    cur.execute("SELECT key FROM issues;")
    list_of_issues = [x[0] for x in cur.fetchall()]

    jira_list = []
    for singleIssue in jira.search_issues(jql_str=f"project = {CURRENT_STREAM} AND type = {TASK_TYPE} "
                                                  f"AND status IN {TASK_STATUS} ORDER BY updated DESC, created DESC",
                                          maxResults=50):
        jira_list.append(singleIssue.key)
    # print(f"Tasks in Jira - {jira_list}")
    compare_lists = (list_of_issues == jira_list)
    # print(compare_lists)
    # print(list_of_issues)
    # print(jira_list)
    if compare_lists:
        print("-------------bot works correctly--------------")
    else:
        await bot.send_message(chat_id=CHAT_ID, text="@Andrew_Dzhulay Something goes wrong. Reboot me please",
                               parse_mode=ParseMode.HTML)
        print("-------------bot does not works--------------")

