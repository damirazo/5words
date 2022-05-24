import os
from typing import Iterator

import requests

RUSSIAN_WORDS_TXT = (
    'https://raw.githubusercontent.com/Harrix/'
    'Russian-Nouns/main/dist/russian_nouns.txt')
RUSSIAN_WORDS_PLACE = os.path.join(os.getcwd(), 'russian_nouns.txt')


def main(pattern: str, excludes: str = '', another_place: str = ''):
    words = all_russian_words(len(pattern))

    result = []
    for word in words:
        if excludes and any((x in excludes for x in word)):
            continue

        has_char = True
        for x in another_place:
            if x not in word:
                has_char = False
                break

        if not has_char:
            continue

        appropriate_word = True
        for i, char in enumerate(pattern):
            if char != '*' and char != word[i]:
                appropriate_word = False
                continue

        if appropriate_word:
            result.append(word)

    for row in result:
        print(row)


def all_russian_words(length: int) -> Iterator:
    rows = None
    if not os.path.exists(RUSSIAN_WORDS_PLACE):
        response = requests.get(RUSSIAN_WORDS_TXT)
        rows = response.text

        with open(RUSSIAN_WORDS_PLACE, 'w+') as f:
            f.write(rows)

        rows = rows.split('\n')

    if rows is None:
        with open(RUSSIAN_WORDS_PLACE, 'r') as f:
            rows = f.readlines()

    return (
        row.lower().strip('\n')
        for row in rows
        if len(row.strip('\n')) == length
        and not row.startswith('-')
    )


def self_test():
    main('у***а', 'скринго', 'д')


self_test()
