import nlp_config as config
import nlp_helpers as helpers
import preprocessing
from pylab import *
from collections import Counter

# constants
results_path = 'results/2/'


# TASK DESCRIPTION
# 2. Use the frequency of the words to fit the Zipf distribution for each ebook.
# Draw the zipf fitting cure for each ebook and comment on the goodness of fit.


def zipfs_law(book, book_ref):

    words = preprocessing.tokenize(book)

    tokens_with_count = Counter(words)

    counts = [count for count in tokens_with_count.values()]

    ranks = arange(1, len(counts) + 1)
    indices_ = argsort(counts)
    frequencies = [counts[index] for index in indices_]

    # plot
    plt.loglog(ranks, frequencies, marker=".")
    title_ = config.books[book_ref]['title']
    plt.title("Zipf plot for " + title_)
    plt.xlabel("Frequency rank of token")
    plt.ylabel("Absolute frequency of token")
    if config.action == 'save':
        path_ = results_path + book_ref + "_zipfs_law"
        plt.savefig(path_)
        plt.close()
    else:
        plt.grid(True)
        plt.show()


def task2():

    raw_books = helpers.getBooks()

    for book_ref, raw_book in raw_books.items():

        chapters = preprocessing.preprocess(raw_book)

        zipfs_law(chapters, book_ref)


if __name__ == "__main__":
    task2()
