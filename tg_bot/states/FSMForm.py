from aiogram.fsm.state import State, StatesGroup


class FSMFillForm(StatesGroup):
    # Создаем экземпляры класса State, последовательно
    # перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодействия с пользователем
    start = State()  # Состояние опроса
    answer = State()  # Состояние ожидания ответа
    legal = State()  # Состояние вопросов правовой защиты
    keep_answers = State()  # Состояние сохранения списка ответов
