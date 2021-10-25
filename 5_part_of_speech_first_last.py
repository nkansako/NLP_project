import nlp_config as config
import nlp_helpers as helpers
import preprocessing
import csv

# constants
results_path = 'results/5/'


# TASK DESCRIPTION
# 5. Investigate the structure of poem in terms of category of starting word and ending word in each line of the poem.
# Investigate the variation of the part-of-speech tag of starting and ending word (excluding punctuation characters)
# across all lines of the poem in both ebooks. How this variation takes place across different chapters.
# Use corresponding illustrations to justify your answers. Comment on the phonetic compatibility of poem in each ebook.


def task5():

    raw_books = helpers.getBooks()

    for book_ref, raw_book in raw_books.items():

        title_ = config.books[book_ref]['title']

        chapters = preprocessing.preprocess(raw_book)
        # TODO


if __name__ == "__main__":
    task5()
