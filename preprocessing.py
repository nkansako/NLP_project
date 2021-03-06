from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nlp_config as config
import re


def remove_stop_words(line: str, repeat: int = 1, keep_negations: bool = False) -> str:
    # return line
    words = word_tokenize(line)
    sw = stopwords.words('english')
    for word in words:
        lower = word.lower()
        if lower in config.special_characters or \
                lower in sw or (not keep_negations and lower in config.negations):
            # we want to remove stopwords which are not negations (negations impact the sentiment)
            words = list(filter(word.__ne__, words))
    result = ' '.join(words)
    if repeat > 0:
        # due to complex word structure, the stop words removal will be ran multiple times
        result = remove_stop_words(result, repeat - 1)
    return result


def only_first_and_last_words(book_: dict) -> dict:
    retval = dict()
    for title, chapter in book_.items():
        new_chapter = []
        for line in chapter:
            # removing stopwords, since they don't contribute to the sentiment
            line_ = remove_stop_words(line)  # run twice for better efficiency
            tokens = line_.split(' ')
            new_chapter.append([tokens[0], tokens[len(tokens) - 1]])
        retval[title] = new_chapter
    return retval


def preprocess(raw_book: str) -> dict:
    # cleanup
    chapters = dict()
    text_buffer = []  # this variable is used to save lines into an array before putting them into a chapter
    chapter_name = ''  # name of the current chapter
    for line in raw_book.splitlines():
        line_cleaned = re.sub(' +', ' ', line).strip()  # removing multiple & first-last whitespaces from the line
        if line_cleaned:
            # not an empty line
            if line_cleaned.isupper():
                # all upper case defines a beginning of a new chapter
                if text_buffer:
                    # if the buffer contains lines, save them as a new chapter
                    chapters[chapter_name] = text_buffer
                    text_buffer = []
                chapter_name = line_cleaned
            else:
                # not uppercase - normal text
                # some lines end with a number; remove the numbers
                tokens = line_cleaned.split(' ')
                if tokens[len(tokens) - 1].isnumeric():
                    tokens.pop()  # remove last token
                text_buffer.append(' '.join(tokens))
            chapters[chapter_name] = text_buffer
    return chapters


def book_to_verses(raw_book: str) -> list:
    # cleanup
    verses = list()
    text_buffer = []  # this variable is used to save lines into an array before putting them into a chapter
    i = 0
    for line in raw_book.splitlines():
        line_cleaned = re.sub(' +', ' ', line).strip()  # removing multiple & first-last whitespaces from the line
        i += 1
        if line_cleaned:
            # not an empty line
            if not line_cleaned.isupper():
                # not uppercase - normal text
                # some lines end with a number; remove the numbers
                tokens = line_cleaned.split(' ')
                if tokens[len(tokens) - 1].isnumeric():
                    tokens.pop()  # remove last token
                text_buffer.append(' '.join(tokens))
        elif len(text_buffer):
            verses.append(text_buffer)
            text_buffer = []
        else:
            if len(text_buffer):
                verses.append(text_buffer)
                text_buffer = []
    if len(text_buffer):
        verses.append(text_buffer)
    return verses


def tokenize(book, keep_stopwords: bool = False):
    # break down a preprocessed book into words
    all_words = ""
    for title, chapter in book.items():
        for line in chapter:
            newline = remove_stop_words(line, keep_stopwords)
            all_words += newline
    return word_tokenize(all_words)


def remove_non_ASCII(string: str) -> str:  # removes all non-ASCII characters from the given string
    return ''.join([i if ord(i) < 128 else '' for i in string])


def four_line_structure(book):
    book = only_first_and_last_words(book)

    counter = 0
    retval = []

    lines = []
    all_lines = []
    for title, chapter in book.items():
        for line in chapter:
            if counter == 4:
                counter = 0
                all_lines.append(lines)
                lines = []

            counter += 1
            lines.append(line[1])
    retval.append(all_lines)

    return retval
