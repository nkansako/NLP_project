import nlp_config as config
import nlp_helpers as helpers
import matplotlib.pyplot as plt
import preprocessing
from nltk import FreqDist
import csv


# constants
results_path = 'results/1/'
most_common_count = 30


# TASK DESCRIPTION
# 1. Use appropriate NLTK coding (you can inspire from coding examples of the online NLTK book)
# in order to plot the histogram of the thirty most frequent words in each ebook. Save the result on excel file.


def most_frequent_words(book):
    words = preprocessing.tokenize(book)
    return FreqDist(words)


def save_to_CSV(data, path):
    with open(path + '.csv', mode='w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for pair in data:
            csv_writer.writerow([pair[0], pair[1]])


def plot(path, data, title):
    if config.action == "save":
        plt.ion()
    data.plot(most_common_count, cumulative=False, title="Most frequent words " + title)
    if config.action != "save":
        plt.savefig(path)
    else:
        plt.ioff()
    plt.close()


def task1():

    raw_books = helpers.getBooks()

    for book_ref, raw_book in raw_books.items():

        title_ = config.books[book_ref]['title']

        chapters = preprocessing.preprocess(raw_book)
        fd = most_frequent_words(chapters)   # tuples of all most common words, sorted DESC

        n_most_common_words = fd.most_common(most_common_count)  # take top N words to further analysis

        save_to_CSV(n_most_common_words, results_path + book_ref + '_most_freq_words')
        plot(path=results_path + book_ref + '_most_freq_words', data=fd, title=title_)


if __name__ == "__main__":
    task1()
