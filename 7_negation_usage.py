from nltk import word_tokenize, pos_tag

import nlp_config as config
import nlp_helpers as helpers
import preprocessing
import matplotlib.pyplot as plt

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
    count_negatives = 0
    count_lines = 0
    for title, chapter in book.items():
        for line in chapter:
            count_lines += 1
            tokens = word_tokenize(line)
            if count_lines < lines_count:
                for token in tokens:
                    if token in config.negations:
                        count_negatives += 1
                        tag = pos_tag(word_tokenize(token))
                        tags.append(tag[0][1])
            else:
                negations_list.append(count_negatives)
                count_lines = 0
                count_negatives = 0

                for token in tokens:
                    if token in config.negations:
                        count_negatives += 1
                        tag = pos_tag(word_tokenize(token))
                        tags.append(tag[0][1])
    # print(negations_list)
    # print(tags)
    return negations_list


def task7():

    raw_books = helpers.getBooks()

    for book_ref, raw_book in raw_books.items():

        title_ = config.books[book_ref]['title']

        chapters = preprocessing.preprocess(raw_book)

        tags = []
        negations_list = count_negations(chapters, tags)

        unique = list(set(negations_list))

        freq = []

        for u in unique:
            c = negations_list.count(u)
            freq.append(c)

        freq = [f / (helpers.totalLinesPerBook(chapters) / lines_count) * 100 for f in freq]

        # result = curve_fit(f, unique, freq)
        # print(result)

        plt.bar(unique, freq)
        t = "Negations for every " + str(lines_count) + " lines " + title_
        plt.title(t)
        plt.xlabel("Amount of negations found in " + str(lines_count) + " consecutive line structure")
        plt.ylabel("Percentage of " + str(lines_count) + " consecutive lines")
        plt.show()

        uniquetags = list(set(tags))

        freqtags = []

        for u in uniquetags:
            c = tags.count(u)
            freqtags.append(c)

        zipped = zip(uniquetags, freqtags)

        s = sorted(zipped, key=lambda x: x[1], reverse=True)

        for _ in s:
            # plt.bar(unique, freq)
            plt.bar(_[0], _[1], color=config.plot_bar_color)

        # plt.bar(uniquetags, freqtags)
        t = "Negations part of speech tag " + title_
        plt.title(t)
        plt.xlabel("Part of speech tag")
        plt.ylabel("Frequency of part of speech tags")
        plt.show()


if __name__ == "__main__":
    task7()
