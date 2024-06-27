from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    ReplyKeyboardRemove,
)

from keyboard import (
    choose_answer_markup,
    show_facts_and_rules_keyboard,
)
from constants.facts import FACTS
from utils import (
    print_rules,
)
from states.FSMForm import FSMFillForm
from constants.questions import (
    QUESTIONS_BASIC,
    QUESTIONS_LEGAL,
)
from constants.rules import RULES

router = Router()


@router.message(
    F.text.lower() == "начать опрос!",
    StateFilter(FSMFillForm.start),
)
async def start_questions(
    message: Message,
    state: FSMContext,
) -> None:
    await state.update_data(question=0)
    await state.update_data(answers=[])
    await message.answer(
        f"{QUESTIONS_BASIC[0][0]}",
        reply_markup=choose_answer_markup(QUESTIONS_BASIC, 0),
    )
    await state.set_state(FSMFillForm.answer)


@router.message(
    StateFilter(FSMFillForm.answer),
)
async def process_answer_press(
    message: Message,
    state: FSMContext,
) -> None:
    ans = message.text
    data = await state.get_data()
    question = data["question"]
    answers = data["answers"]
    if ans == "Да":
        answers.append(QUESTIONS_BASIC[question][2])
    elif ans == "Нет":
        answers.append(QUESTIONS_BASIC[question][4])
    else:
        message.answer(
            text="Для ответа на вопросы следует использовать кнопки.\n"
            "Для справки напишите /help.",
        )
    if "Ф23" in answers:
        await message.answer(
            f"{QUESTIONS_LEGAL[0][0]}",
            reply_markup=choose_answer_markup(QUESTIONS_LEGAL, 0),
        )
        await state.update_data(question=0)
        await state.set_state(FSMFillForm.legal)
        return
    for r in RULES:
        if r[0] in answers and r[1] in answers:
            answers.append(r[2])
    if "Ф1" in answers or "Ф2" in answers or "Ф3" in answers:
        await message.answer(text="Опрос завершен!", reply_markup=ReplyKeyboardRemove())
        print_rules(answers)  # Вывод списка сработавших правил
        if "Ф1" in answers:
            await message.answer(
                text="Подходящая вам форма защиты: ПУБЛИКАЦИЯ",
                reply_markup=show_facts_and_rules_keyboard(),
            )
        elif "Ф2" in answers:
            await message.answer(
                text="Подходящая вам форма защиты: КОММЕРЧЕСКАЯ ТАЙНА",
                reply_markup=show_facts_and_rules_keyboard(),
            )
        elif "Ф3" in answers:
            await message.answer(
                text="Подходящая вам форма защиты: ПАТЕНТОВАНИЕ",
                reply_markup=show_facts_and_rules_keyboard(),
            )
        await state.set_state(FSMFillForm.keep_answers)
        return
    if question + 1 < len(QUESTIONS_BASIC):
        question = question + 1
        await message.answer(
            f"{QUESTIONS_BASIC[question][0]}",
            reply_markup=choose_answer_markup(QUESTIONS_BASIC, question),
        )
        await state.update_data(question=question)
        await state.update_data(answers=answers)
    else:
        await message.answer(text="Опрос завершен!", reply_markup=ReplyKeyboardRemove())
        print_rules(answers)
        await message.answer(
            text="Не удалось определить лучшую форму защиты. \n\nНапишите /start чтобы попробовать еще раз.",
            reply_markup=show_facts_and_rules_keyboard(),
        )
        await state.set_state(FSMFillForm.keep_answers)


@router.message(
    StateFilter(FSMFillForm.legal),
)
async def process_answer_press_legal(
    message: Message,
    state: FSMContext,
) -> None:
    ans = message.text
    data = await state.get_data()
    question = data["question"]
    answers = data["answers"]
    if ans == "Да":
        answers.append(QUESTIONS_LEGAL[question][2])
    elif ans == "Нет":
        answers.append(QUESTIONS_LEGAL[question][4])
    else:
        message.answer(
            text="Для ответа на вопросы следует использовать кнопки.\n\n"
            "Для справки напишите /help.",
        )
    for r in RULES:
        if r[0] in answers and r[1] in answers:
            answers.append(r[2])
    if "Ф1" in answers or "Ф2" in answers or "Ф3" in answers:
        await message.answer(text="Опрос завершен!", reply_markup=ReplyKeyboardRemove())
        print_rules(answers)
        if "Ф1" in answers:
            await message.answer(
                text="Подходящая вам форма защиты: ПУБЛИКАЦИЯ",
                reply_markup=show_facts_and_rules_keyboard(),
            )
        elif "Ф2" in answers:
            await message.answer(
                text="Подходящая вам форма защиты: КОММЕРЧЕСКАЯ ТАЙНА",
                reply_markup=show_facts_and_rules_keyboard(),
            )
        elif "Ф3" in answers:
            await message.answer(
                text="Подходящая вам форма защиты: ПАТЕНТОВАНИЕ",
                reply_markup=show_facts_and_rules_keyboard(),
            )
        await state.set_state(FSMFillForm.keep_answers)
        return
    if question + 1 < len(QUESTIONS_LEGAL):
        question = question + 1
        await message.answer(
            f"{QUESTIONS_LEGAL[question][0]}",
            reply_markup=choose_answer_markup(QUESTIONS_LEGAL, question),
        )
        await state.update_data(question=question)
        await state.update_data(answers=answers)
    else:
        await message.answer(text="Опрос завершен!", reply_markup=ReplyKeyboardRemove())
        print_rules(answers)
        await message.answer(
            text="Не удалось определить лучшую форму защиты. \nНапишите /start чтобы попробовать еще раз.",
            reply_markup=show_facts_and_rules_keyboard(),
        )
        await state.set_state(FSMFillForm.keep_answers)


@router.message(
    F.text.lower() == "показать факты",
    StateFilter(FSMFillForm.keep_answers),
)
async def process_show_facts(
    message: Message,
    state: FSMContext,
) -> None:
    data = await state.get_data()
    answers = data["answers"]
    answers = list(dict.fromkeys(answers))  # удаляем возможные дубликаты
    text = ""
    for i, elm in enumerate(answers):
        text = text + f"Факт номер {i + 1}: {FACTS[elm]}.\n\n"
    text = text + "Чтобы пройти опрос еще раз напишите /start."
    await message.answer(text=text)


@router.message(
    F.text.lower() == "показать правила",
    StateFilter(FSMFillForm.keep_answers),
)
async def process_show_rules(
    message: Message,
    state: FSMContext,
) -> None:
    data = await state.get_data()
    answers = data["answers"]
    answers = list(dict.fromkeys(answers))  # удаляем возможные дубликаты
    for i, r in enumerate(RULES):
        if r[0] in answers and r[1] in answers and r[0] != r[1]:
            text = f"Сработало правило номер {i + 1}: \nЕсли {FACTS[r[0]]} и {FACTS[r[1]]} то {FACTS[r[2]]}\n"
            await message.answer(text=text)
        elif r[0] in answers and r[1] in answers:
            text = f"Сработало правило номер {i + 1}: \nЕсли {FACTS[r[0]]} то {FACTS[r[2]]}\n"
            await message.answer(text=text)
    await message.answer(text="Чтобы пройти опрос еще раз напишите /start.")
