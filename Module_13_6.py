from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
import aiogram
from pyexpat.errors import messages

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = InlineKeyboardMarkup()
button = InlineKeyboardButton(text="Рассчитать норму калорий", callback_data='calories')
button1 = InlineKeyboardButton(text="Формулы расчета", callback_data='formulas')
kb.add(button, button1)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(text="Привет!")
async def hello(message):
    await message.answer("Введите команду /start, что бы начать общение")

@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer("Привет. Я бот помогающий твоему здоровью.")



@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer("Выберите опцию:", reply_markup=kb)


@dp.callback_query_handler(text="formulas")
async def get_formulas(call):
    await call.message.answer("10*вес(кг)+6,25*рост(см)-5*возраст(г)-161")
    await call.answer()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer("Привет! Я бот помогающий твоему здоровью")


@dp.callback_query_handler(text="calories")
async def set_age(call):
    await call.message.answer('Введите ваш возраст:')
    await call.answer()
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=int(message.text))
    await message.answer("Введите свой рост:")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=int(message.text))
    await message.answer("Введите свой вес:")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=int(message.text))
    data = await state.get_data()
    result = 10 * data.get("weight") + 6.25 * data.get("growth") - 5 * data.get("age") - 161
    await message.answer(f"Ваша норма калорий: {result}")
    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
