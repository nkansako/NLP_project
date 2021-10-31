from enum import Enum

import nlp_config as config
import preprocessing
import numpy as np
import matplotlib.pyplot as plt
import os
from nltk.tokenize import word_tokenize


def plotting(path, y, x=None, title='', fn='plot', ylabel="", xlabel=""):
    if x is None:
        x = np.linspace(0, len(y) - 1, len(y))
    if fn == 'bar':
        plt.bar(x, y)
    else:
        plt.plot(x, y)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
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


def chapters_to_lines(chapters):
    lines = []
    for chapter_title, chapter_content in chapters.items():
        for line in chapter_content:
            lines.append(line)
    # print(lines[:4])
    return lines


def strip_string(string: str, to_strip: list) -> str:
    for value in to_strip:
        string = string.replace(value, "")
    return string


class Sentiments(Enum):
    NEGATIVE = 'neg'
    POSITIVE = 'pos'
    NEUTRAL = 'neu'
    COMPOUND = 'compound'


class AnalysisTypes(Enum):
    LINE = 'lines'
    FIRST_WORD = 'first words'
    LAST_WORD = 'last words'


def prepare_string(line: str, analysis_type: AnalysisTypes) -> str:
    retval = preprocessing.remove_non_ASCII(line)
    if analysis_type == AnalysisTypes.LAST_WORD:
        retval = strip_string(retval, config.trim_values)
        retval = word_tokenize(retval)
        retval = retval[-1]
    elif analysis_type == AnalysisTypes.FIRST_WORD:
        retval = strip_string(retval, config.trim_values)
        retval = word_tokenize(retval)
        retval = retval[0]
    return retval
