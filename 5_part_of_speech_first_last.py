import nlp_config as config
import nlp_helpers as helpers
import preprocessing
import csv
from nltk import pos_tag
import matplotlib.pyplot as plt


# constants
results_path = 'results/5/'


# TASK DESCRIPTION
# 5. Investigate the structure of poem in terms of category of starting word and ending word in each line of the poem.
# Investigate the variation of the part-of-speech tag of starting and ending word (excluding punctuation characters)
# across all lines of the poem in both ebooks. How this variation takes place across different chapters.
# Use corresponding illustrations to justify your answers. Comment on the phonetic compatibility of poem in each ebook.

def tag_words(book, title_):

    tags = []

    for title, chapter in book.items():
        for line in chapter:     
            print(line)    
            try:   
                tag = pos_tag(line)
                write_txt(tag[0], title_)
                write_txt(tag[1], title_)
                tags.append((tag[0][1], tag[1][1]))
            except IndexError as e:
                print(e)
    
    return tags


def write_txt(obj: tuple, title: str):
    with open("5_pos_tags_" + title + ".txt", "a") as file:
        line = obj[0] + "," + obj[1] + "\n"
        file.write(line)

def save_to_CSV(data, path):
    with open(path + '.csv', mode='w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for pair in data:
            csv_writer.writerow([pair[0], pair[1]])

def plot(path: str, structure: list, title: str):
    unique = list(set(structure))

    freq = []

    for u in unique:
        c = structure.count(u)
        freq.append(c)

    zipped = zip(unique, freq)
    
    s = sorted(zipped, key=lambda x: x[1], reverse=True)
    
    for _ in s:
        plt.bar(_[0][0], _[1], color="blue")

    
    plt.xlabel("Part of speech tag last word")
    plt.ylabel("Frequency")
    plt.title(title)
    
    if config.action == "save":
        plt.savefig(path)
    else:
        plt.show()

    for _ in s:
        plt.bar(_[0][1], _[1], color="blue")

    
    plt.xlabel("Part of speech tag last word")
    plt.ylabel("Frequency")
    plt.title(title)
    
    if config.action == "save":
        plt.savefig(path)
    else:
        plt.show()

def task5():

    raw_books = helpers.getBooks()

    for book_ref, raw_book in raw_books.items():

        title_ = config.books[book_ref]['title']

        chapters = preprocessing.preprocess(raw_book)

        first_last = preprocessing.only_first_and_last_words(chapters)

        tags = tag_words(first_last, title_)

        #save_to_CSV(tags, results_path + book_ref + "_pos_f_l")

        title = book_ref + " first and last word part of speech tag"

        plot(results_path + book_ref + "_f_l_pos.png", tags, title)


if __name__ == "__main__":
    task5()
