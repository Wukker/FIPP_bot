from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import any_state, default_state
from aiogram.types import (
    Message,
)

from keyboard import (
    start_questions_markup,
)
from states.FSMForm import FSMFillForm

router = Router()


@router.message(Command(commands=["start"]), StateFilter(any_state))
async def process_start_command(
    message: Message,
    state: FSMContext,
) -> None:
    await state.clear()
    await message.answer(
        text="👋Привет, клиент! Данный бот поможет вам определить какую форму охраны выбрать для "
        "вашей интеллектуальной собственности! Ответив на пару вопросов мы сможем вам подсказать, "
        "какую из 3 форм охраны интеллектуальной собственности, Патентование, Публикация или "
        "Коммерческая тайна вам больше подойдет. \nДля продолжения нажмите на кнопку.",
        reply_markup=start_questions_markup(),
    )
    await state.set_state(FSMFillForm.start)


@router.message(Command(commands=["help"]), StateFilter(any_state))
async def process_help_command(
    message: Message,
    state: FSMContext,
) -> None:
    await message.answer(
        text="Это бот предназначен для помощи вам в выборе формы охраны для вашей интеллектуальной собственности. "
        "Доступно три варианта охраны: 1️⃣ Патентование, 2️⃣ Публикация и 3️⃣ Коммерческая тайна.\n\n"
        "Напишите '/start', чтобы бот помог вам выбрать форму охраны "
        "или чтобы запустить опрос заново.",
    )
    await state.set_state(default_state)
