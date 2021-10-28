from nltk import word_tokenize, pos_tag

import nlp_config as config
import nlp_helpers as helpers
import preprocessing
import matplotlib.pyplot as plt
import csv
from re import search
from nltk.corpus import brown
from nltk.corpus import words

# constants
results_path = 'results/7/'
lines_count = 5


# TASK DESCRIPTION
# 7. We would like to compare the usage of negation for each ebook.
# Write a program that allow you to identify the occurrence of negation in the text
# where the negation is identified through a set of preselected terms
# (i.e., single word like not, none, or as affix as in can(n‘t), (im)perfect)) using string matching method.
# Write a program that identifies the occurrence of negation in every set of five consecutive lines of the poem.
# Compare the frequency of occurrence of negation in each ebook.
# Use the code to identify the type of preposition tag-set (use Part-of-speech tag)
# that occur in the line where the negation is detected. Plot the frequency of each preposition tag in each ebook.


def count_negations(book, tags):
    negations_list = []
    negation_tags = []
    count_negatives = 0
    count_lines = 0
    for title, chapter in book.items():
        for line in chapter:
            count_lines += 1
            tokens = word_tokenize(line)
            if count_lines < lines_count:
                for token in tokens:
                    if token in config.negations or check_prefix(token):
                        count_negatives += 1
                        tag = pos_tag(word_tokenize(token))
                        negation_tags.append(tag[0][1])
            else:
                negations_list.append(count_negatives)
                count_lines = 0
                count_negatives = 0

                for token in tokens:
                    if token in config.negations or check_prefix(token):
                        count_negatives += 1
                        tag = pos_tag(word_tokenize(token))
                        negation_tags.append(tag[0][1])

    return negations_list, negation_tags

def check_prefix(word):
    if config.corpus == "brown":
        allwords = brown.words()
    elif config.corpus != "brown":
        allwords = words.words()
    for prefix in config.negation_prefix:
        s = search("\A"+prefix, word) # Only count if at the beginning of the string
        if s: 
            index = s.span()[1] # Take the starting index of the "actual word"
            if word[index:] in allwords: # Check if the word exists, so for example, *a*typical will be found to be negative, but *a*rrive will not
                return True

    return False

def task7():

    raw_books = helpers.getBooks()

    for book_ref, raw_book in raw_books.items():

        title_ = config.books[book_ref]['title']

        chapters = preprocessing.preprocess(raw_book)

        tags = []
        negations_list, tags = count_negations(chapters, tags)
        path1 = results_path + book_ref + "_negations_frequency.png"
        path2 = results_path + book_ref + "_negations_tags.png"
        plot(path1, path2, negations_list, tags, title_, chapters)
        
        save_to_CSV(negations_list, results_path + book_ref + "_negations_frequency")
        save_to_CSV(tags, results_path + book_ref + "_negations_tags")


def plot(path1: str, path2: str, negation_counts: list, negation_tags: list, title_: str, chapters: dict):
    unique_counts = list(set(negation_counts))
    freq_counts = []

    for u in unique_counts:
        c = negation_counts.count(u)
        freq_counts.append(c)

    freq_counts = [f / (helpers.totalLinesPerBook(chapters) / lines_count) * 100 for f in freq_counts]

    plt.bar(unique_counts, freq_counts)
    t = "Negations for every " + str(lines_count) + " lines " + title_
    plt.title(t)
    plt.xlabel("Amount of negations found in " + str(lines_count) + " consecutive line structure")
    plt.ylabel("Percentage of " + str(lines_count) + " consecutive lines")
    if config.action == "save":
        plt.savefig(path1)
    else:
        plt.show()

    unique_tags = list(set(negation_tags))

    freq_tags = []

    for u in unique_tags:
        c = negation_tags.count(u)
        freq_tags.append(c)

    zipped = zip(unique_tags, freq_tags)

    s = sorted(zipped, key=lambda x: x[1], reverse=True)

    for _ in s:
        plt.bar(_[0], _[1], color=config.plot_bar_color)
    t = "Negations part of speech tag " + title_
    plt.title(t)
    plt.xlabel("Part of speech tag")
    plt.ylabel("Frequency of part of speech tags")
    if config.action == "save":
        plt.savefig(path2)
    else:
        plt.show()

def save_to_CSV(data, path):
    with open(path + '.csv', mode='w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for pair in data:
            try:
                csv_writer.writerow([pair[0], pair[1]])
            except IndexError:
                csv_writer.writerow([pair])
            except TypeError:
                csv_writer.writerow([pair])

if __name__ == "__main__":
    task7()
