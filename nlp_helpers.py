from enum import Enum

import nlp_config as config
import numpy as np
import matplotlib.pyplot as plt
import os


def plotting(path, y, x=None, title=''):
    if x is None:
        x = np.linspace(0, len(y) - 1, len(y))
    plt.plot(x, y)
    plt.title(title)
    if config.action == 'save':
        plt.savefig(path)
        plt.close()
    else:
        plt.show()


def getBooks() -> dict:
    books_path = {book_ref: book_data['path'] for book_ref, book_data in config.books.items()}
    books_ = {}
    for book_ref, book_path in books_path.items():
        with open("books/" + book_path, "r", encoding="UTF-8") as file:
            text = ""
            line = file.readline()
            while line:
                text += line.strip() + os.linesep
                line = file.readline()
            books_[book_ref] = text
    return books_


def totalLinesPerBook(chapters):
    return sum(len(chapter) for chapter_title, chapter in chapters.items())


class Sentiments(Enum):
    NEGATIVE = 'neg'
    POSITIVE = 'pos'
    NEUTRAL = 'neu'
    COMPOUND = 'compound'
