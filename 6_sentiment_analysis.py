from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
from enum import Enum
import re
import os
import csv
from nltk.tokenize import word_tokenize

import main


class Sentiments(Enum):
    NEGATIVE = 'neg'
    POSITIVE = 'pos'
    NEUTRAL = 'neu'
    COMPOUND = 'compound'


# 6. Sentiment analysis
# We want to investigate the variation of the sentiment across lines of poem and chapters.
# Use NLTK sentiment analyzer of your choice to calculate the overall sentiment of each line of the poem
# as well as sentiment of starting word and ending word of each line.
# Save your response in an excel file.
# Use illustrations of your choice to visualize the sentiment across lines and chapters,
# and another illustration to visualize the possible compatibility of starting and ending word in each line of the poem


def analyze_the_sentiment_of_structure(book_: dict, sentiments: list) -> dict:
    retval = dict()
    for sentiment in sentiments:
        retval[sentiment.value] = []
    # this can surely be initiated in a better python way

    sia = SentimentIntensityAnalyzer()
    # iterate through books
    for title, chapter in book_.items():
        for line in chapter:
            scores = sia.polarity_scores(line)
            # {'neg': 0.0, 'neu': 0.295, 'pos': 0.705, 'compound': 0.8012}

            for sentiment in sentiments:
                retval[sentiment.value].append(scores[sentiment.value])
    return retval


def analyze_the_sentiment_of_structure_2(book_: dict, sentiments: list) -> dict:
    retval = dict()
    for sentiment in sentiments:
        retval[sentiment.value] = [[], []]
    # this can surely be initiated in a better python way

    sia = SentimentIntensityAnalyzer()
    # iterate through chapters
    for title, chapter in book_.items():
        for words in chapter:
            scores_first = sia.polarity_scores(words[0])
            scores_last = sia.polarity_scores(words[1])
            # example: {'neg': 0.0, 'neu': 0.295, 'pos': 0.705, 'compound': 0.8012}

            for sentiment in sentiments:
                retval[sentiment.value][0].append(scores_first[sentiment.value])
                retval[sentiment.value][1].append(scores_last[sentiment.value])
    return retval


def only_first_and_last_words(book_: dict) -> dict:
    retval = dict()
    for title, chapter in book_.items():
        new_chapter = []
        for line in chapter:
            # removing stopwords, since they don't contribute to the sentiment
            line_ = remove_stop_words(remove_stop_words(line)) # run twice for better efficiency
            tokens = line_.split(' ')
            new_chapter.append([tokens[0], tokens[len(tokens)-1]])
        retval[title] = new_chapter
    return retval


def remove_stop_words(line: str) -> str:
    # return line
    words = word_tokenize(line)
    sw = stopwords.words('english')
    for word in words:
        if word.lower() in sw or word.lower() in main.special_characters:
            words.remove(word)
    return ' '.join(words)


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
                if tokens[len(tokens)-1].isnumeric():
                    tokens.pop()  # remove last token
                text_buffer.append(' '.join(tokens))
            chapters[chapter_name] = text_buffer
    return chapters


def save_to_CSV(structure: list, name: str):
    with open(name + '.csv', mode='w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for score in structure:
            csv_writer.writerow([str(score)])


# TODO: merge these two into one function
def save_to_CSV_2(structure: list, name: str):
    with open(name + '.csv', mode='w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for score in structure:
            csv_writer.writerow(score)


def prepare_for_CSV(structures: list) -> [list]:
    retval = [[] for i in range(len(structures[0]))]
    for structure in structures:
        # print(structure)
        for i, value in enumerate(structure):
            # print(i)
            retval[i].append(structure[i])
    for val in retval:
        val = ','.join(str(val))
    return retval


def books() -> list:
    # books_path = ['blake.txt']
    # books_path = ['keats.txt']
    books_path = ['keats.txt', 'blake.txt']  # TODO: should be read from a config file
    books_ = [] # TODO: make this an associative array: book_name -> book_content
    for book_path in books_path:
        with open(book_path, "r", encoding="UTF-8") as file:
            text = ""
            line = file.readline()
            while line:
                text += line.strip() + os.linesep
                line = file.readline()
            books_.append(text)
    return books_


def task6():
    raw_books = books()
    cnt = 1
    for raw_book in raw_books:
        chapters = preprocess(raw_book)
        first_last_words = only_first_and_last_words(chapters)

        chapters_sentiment = analyze_the_sentiment_of_structure(chapters, [Sentiments.COMPOUND])
        save_to_CSV(chapters_sentiment[Sentiments.COMPOUND.value], "results/6/Book_" + str(cnt) + "_sentiment_per_line")

        first_last_words_sentiment = analyze_the_sentiment_of_structure_2(first_last_words, [Sentiments.COMPOUND])
        first_last_words_sentiment_prepared = prepare_for_CSV(first_last_words_sentiment[Sentiments.COMPOUND.value])
        save_to_CSV_2(first_last_words_sentiment_prepared, "results/6/Book_" + str(cnt) + "_sentiment_f_l_word")

        # TODO: visualize

        # TODO: currently calculating COMPOUND scores; check with TA if that's what's expected



        cnt = cnt + 1


if __name__ == "__main__":
    task6()


# TODO: export helper functions to a separate file

