from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from aiogram.fsm.state import StatesGroup, State

router = Router()



class Form(StatesGroup):
    waiting_for_name = State()

@router.message(F.text == "/start")
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(Form.waiting_for_name)
    await message.answer("Your name?")

@router.message(Form.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(f"Hi, {message.text}!")
