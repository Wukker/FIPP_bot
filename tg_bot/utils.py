from typing import List

from constants.facts import FACTS
from constants.rules import RULES


def print_rules(answers: List[str]) -> None:
    answers = list(dict.fromkeys(answers))  # удаляем возможные дубликаты
    for i, r in enumerate(RULES):
        if r[0] in answers and r[1] in answers and r[0] != r[1]:
            print(
                f"Сработало правило номер {i + 1}: \nЕсли {FACTS[r[0]]} и {FACTS[r[1]]} то {FACTS[r[2]]}\n",
            )
        elif r[0] in answers and r[1] in answers:
            print(
                f"Сработало правило номер {i + 1}: \nЕсли {FACTS[r[0]]} то {FACTS[r[2]]}\n",
            )
