import nlp_config as config
import nlp_helpers as helpers
import preprocessing
import csv

# constants
results_path = 'results/4/'


# TASK DESCRIPTION
# 4. We would like to find out the structure of the poems in terms of length of each line of the poem.
# Write down a program that calculates the length of each line of the poem in terms of number characters.
# Save the result in an excel file. Next, plot the frequency of the various length values.
# Find out whether a polynomial, exponential, Zipfs law fitting can be achieved? Motivate your answer.


def line_lengths(book, with_space=True):
    lengths = []
    for title, chapter in book.items():
        for line in chapter:
            if with_space:
                length = len(line)
            else:
                length = len(line.replace(" ", ""))
            if length > 1:
                lengths.append(length)
    return lengths


def save_to_CSV(data, path):
    with open(path + '.csv', mode='w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for item in data:
            csv_writer.writerow([item])


def task4():
    raw_books = helpers.getBooks()

    for book_ref, raw_book in raw_books.items():

        title_ = config.books[book_ref]['title']

        chapters = preprocessing.preprocess(raw_book)

        # analyze with and without spaces
        for has_spaces in [True, False]:
            lengths = line_lengths(chapters, has_spaces)
            uniquel = list(set(lengths))

            freq = []

            for u in uniquel:
                c = lengths.count(u)
                freq.append(c)

            path = results_path + book_ref + "line_lengths_with" + ("out" if has_spaces else "") + "_spaces"

            # csv
            save_to_CSV(freq, path)

            # plot
            title = "Line length frequency with" + ("out" if has_spaces else "") + " spaces " + title_
            helpers.plotting(path=path, x=uniquel, y=freq, title=title)

            helpers.stats(uniquel)


if __name__ == "__main__":
    task4()
