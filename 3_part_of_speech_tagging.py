import nlp_config as config
import nlp_helpers as helpers
import matplotlib.pyplot as plt
import preprocessing
from nltk import pos_tag

# constants
results_path = 'results/3/'


# TASK DESCRIPTION
# 3. Identify Part-of-speech tagging of all words of the two ebooks using NLTK part-of-speech tagger
# and save the result on an Excel file. Trace the frequency of the various of part-of-speech tags.
# Find out whether a Zipf law can be fitted for each book. Explain your reasoning using statistical evidence.


def part_of_speech(book):
    words = preprocessing.tokenize(book)

    pos = pos_tag(words)
    tags = []
    for _ in pos:
        tags.append(_[1])
    unique = list(set(tags))
    freq = []
    new = []
    for u in unique:
        c = tags.count(u)
        freq.append(c)
        new.append(u)

    zipped = zip(unique, freq)

    return sorted(zipped, key=lambda x: x[1], reverse=True)


def plot(path, sorted_pos, title):
    action = config.action

    for _ in sorted_pos:
        plt.bar(_[0], _[1], color=config.plot_bar_color)
    plt.title(title)

    if action == 'save':
        plt.savefig(path)
        plt.close()
    else:
        plt.show()


def task3():

    raw_books = helpers.getBooks()

    for book_ref, raw_book in raw_books.items():

        title_ = config.books[book_ref]['title']

        chapters = preprocessing.preprocess(raw_book)
        sorted_pos = part_of_speech(chapters)

        path = results_path + book_ref + '_part_of_speech_tagging'
        plot(path=path, sorted_pos=sorted_pos, title="Part of speech frequency " + title_)


if __name__ == "__main__":
    task3()
