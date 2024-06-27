from typing import List

from aiogram.types import (
    ReplyKeyboardMarkup,
)
from aiogram.utils.keyboard import (
    ReplyKeyboardBuilder,
)


def choose_answer_markup(
    questions: List[List[str]],
    question: int,
) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text=f"{questions[question][1]}")
    builder.button(text=f"{questions[question][3]}")
    return builder.as_markup(resize_keyboard=True)


def start_questions_markup() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(
        text="Начать опрос!",
    )
    return builder.as_markup(one_time_keyboard=True, resize_keyboard=True)


def show_facts_and_rules_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text="Показать факты")
    builder.button(text="Показать правила")
    return builder.as_markup(resize_keyboard=True)
