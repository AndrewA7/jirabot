from aiogram import types

from bugs_bot import dp


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer(text="Hi")


@dp.message_handler(commands=["FUCK_YOU"])
async def start_x(message: types.Message):
    await message.answer(text="Потринди мені тут... морда кожана")


@dp.message_handler(commands=["get_task_status"])
async def get_task_status(message: types.Message):
    await message.answer(text="In Development. Will be done soon")
