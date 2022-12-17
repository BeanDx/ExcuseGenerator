from aiogram import types, executor, Dispatcher, Bot
import random

# потом почистить не нужное, хотя нет, мне лень, если ты это читаешь, почисти, мне больно смотреть на такой список.
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor
# потом почистить не нужное, хотя нет, мне лень, если ты это читаешь, почисти, мне больно смотреть на такой список.


from config import *
from list import list # импорт списка отмазок

Bot = Bot(TOKEN_API)
storage = MemoryStorage()
dp = Dispatcher(Bot, storage=storage)


class Form(StatesGroup): # машина состояний
    generation = State()


async def on_startup(_):  # текст при запуске
    print('~~~БОТ БЫЛ ЗАПУЩЕН~~~')

START_COMMAND = '''<b>Привет! Я бот для генерации отмазок! Больше нету нужды ходить в школу!</b>\n
<em>Введите /gen для генерации отмазки!</em>'''

TEXT_GENERATION = '''<b>Введите имя, от кого отмазываемся:</b>'''

commands = {'/start': 'Нажмите для запуска бота', '/help': 'Нажмите для просмотра доступных команд'}

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer(text=START_COMMAND,
                         parse_mode='html')


@dp.message_handler(commands=['gen']) # команда /gen
async def generation(message: types.Message):
    await Form.generation.set()

    await message.answer(text=TEXT_GENERATION,
                         parse_mode='html')


@dp.message_handler(state=Form.generation)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['generation'] = message.text

    data = await state.get_data()
    gener = data.get('generation')

    test = random.choice(list)
    await message.answer(f'{gener}' + str(test))

    # await message.answer(f'ок, твое имя {gener}')
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp,
                           skip_updates=True,
                           on_startup=on_startup)

# message.from_user.id
# await Bot.send_message(message.from_user.id, 'text')
