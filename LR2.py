import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, F, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, ReplyKeyboardRemove

TOKEN = "7577828027:AAG35ggRmkLoYADC_4KFsNdM28itH9fcojA"

storage = MemoryStorage()
bot_router = Router()

# Вопросы для викторины "Кто хочет стать миллионером"
quiz_data = [
    {
        "question": "Саммый массовый пассажирский авиалайнер в мире",
        "options": ["Tupolev 154", "Airbus A320", "Boeing 737", "Comac C919"],
        "answer": "Boeing 737"
    },
    {
        "question": "Сколько цилиндров максимум используется в рядном двигателе",
        "options": ["5", "6", "7", "8"],
        "answer": "6"
    },
    {
        "question": "Какой троллейбус в Омске всегда старый",
        "options": ["2", "3", "7", "12"],
        "answer": "2"
    },
    {
        "question": "Сколько в Омске станций метро",
        "options": ["0", "1", "5", "17"],
        "answer": "1"
    },
    {
        "question": "Кто основал GNU",
        "options": ["Richard Matthew Stallman", "Bill Gates", "Linus Benedict Torvalds", "Alexander Anatoliev"],
        "answer": "Richard Matthew Stallman"
    }
]


class Quiz(StatesGroup):
    waiting_for_answer = State()


async def send_question(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    index = data.get("index", 0)

    if index < len(quiz_data):
        current = quiz_data[index]
        options_markup = ReplyKeyboardRemove()
        text = f"Вопрос {index + 1}: {current['question']}\n" + \
               "\n".join(f"{i + 1}. {opt}" for i, opt in enumerate(current['options']))

        await message.answer(text)
        await state.set_state(Quiz.waiting_for_answer)
        await state.update_data(answer=current['answer'])
    else:
        score = data.get("score", 0)
        await state.clear()
        await message.answer(f"Игра окончена! Ваш результат: {score} из {len(quiz_data)}")


@bot_router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(
        "Привет! Пиши команду /game и начни игру!"
    )


@bot_router.message(Command("cancel"))
@bot_router.message(F.text.casefold() == "cancel")
async def cmd_cancel(message: Message, state: FSMContext) -> None:
    current = await state.get_state()
    if current:
        await state.clear()
        await message.answer("Игра отменена.", reply_markup=ReplyKeyboardRemove())


@bot_router.message(Command("game"))
async def cmd_quiz(message: Message, state: FSMContext) -> None:
    await state.set_data({"index": 0, "score": 0})
    await message.answer("Начинаем игру!")
    await asyncio.sleep(1)
    await send_question(message, state)


@bot_router.message(Quiz.waiting_for_answer)
async def process_answer(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    index = data.get("index", 0)
    score = data.get("score", 0)
    correct = data.get("answer", "")

    if message.text.strip() == correct:
        score += 1
        await message.answer("Правильно!")
    else:
        await message.answer(f"Неправильно! Правильный ответ: {correct}")

    index += 1
    await state.update_data(index=index, score=score)

    await asyncio.sleep(1)
    await send_question(message, state)


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=storage)

    dp.include_router(bot_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())