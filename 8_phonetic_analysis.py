import nlp_config as config
import nlp_helpers as helpers
import preprocessing
import fuzzy
import csv
import matplotlib.pyplot as plt
import statistics
from scipy.stats import kurtosis
from scipy.stats import skew

# constants
results_path = 'results/8/'


# TASK DESCRIPTION
# 8. Compare the phonetic of starting word and ending word of each line of the poem.
# Use the “Fuzzy” library in python to generate the character string that identifies phonetically similar words,
# and then use edit distance to compute the phonetic similarity between two words.
# Leave the size of the generated string open.
# The distance between the phonetic generated vectors corresponding to starting/ending word is generated like this:
# Assume L1 is the first word phonetic string, and L2 is the second word phonetic string generated by Fuzzy library.
# Then the phonetic association Sim(L1,L2)= 2*S/ (length(L1)+length(L2)) where S is the length of the largest substring,
# which is common to both L1 and L2.
# Calculate the value of Sim(L1,L2) for each line of the poem and size the result in excel file.
# Find out whether some curve fitting (polynomial, exponential or zipf can be fitted to the data).
# Motivate your answer and display appropriate plotting.


def phonetic(book, title_):
    phonetics = []
    for title, chapter in book.items():
        for line in chapter:
            first = line[0]
            last = line[1]
            s1 = fuzzy.Soundex(len(first))
            s2 = fuzzy.Soundex(len(last))
            #print(first, last)  # show what happens
            try:
                l1 = s1(first)  # These fail with non ascii characters
                l2 = s2(last)
                #print(l1, l2)

                S = len(largest_common_substring(l1, l2, len(l1), len(l2)))
                try:
                    similarity = 2 * S / (len(l1) + len(l2))
                except ZeroDivisionError as e:
                    similarity = 0
                phonetics.append(similarity)
            except UnicodeEncodeError:
                print("Error occurred with line")
                print(first, last)

    plot(results_path + title_ + "_f_l_phonetic.png", phonetics, title_ + " first and last word phonetics")


def four_line_phonetic(book, title):
    phoneticsAABB = []
    phoneticsABAB = []
    phoneticsABBA = []
    for lines in book:
        for line in lines:
            last_words = line
            #print(last_words)
            s0 = fuzzy.Soundex(len(last_words[0]))
            s1 = fuzzy.Soundex(len(last_words[1]))
            s2 = fuzzy.Soundex(len(last_words[2]))
            s3 = fuzzy.Soundex(len(last_words[3]))
            last_words[0] = last_words[0].replace("-","").replace("—", "").replace("Æ", "ae").replace("ü", "u").replace("ä", "a").replace("è", "e")
            last_words[1] = last_words[1].replace("-","").replace("—", "").replace("Æ", "ae").replace("ü", "u").replace("ä", "a").replace("è", "e")
            last_words[2] = last_words[2].replace("-","").replace("—", "").replace("Æ", "ae").replace("ü", "u").replace("ä", "a").replace("è", "e")
            last_words[3] = last_words[3].replace("-","").replace("—", "").replace("Æ", "ae").replace("ü", "u").replace("ä", "a").replace("è", "e")
            try:
                l0 = s0(last_words[0]) # These fail with non ascii characters
                l1 = s1(last_words[1])
                l2 = s2(last_words[2])
                l3 = s3(last_words[3])

                S0 = len(largest_common_substring(l0, l1, len(l0), len(l1))) # These two are AABB phonetics
                S1 = len(largest_common_substring(l2, l3, len(l2), len(l3)))

                S2 = len(largest_common_substring(l0, l2, len(l0), len(l2))) # These two are ABAB phonetics
                S3 = len(largest_common_substring(l1, l3, len(l1), len(l3)))

                S4 = len(largest_common_substring(l0, l3, len(l0), len(l3))) # These two are ABBA phonetics
                S5 = len(largest_common_substring(l1, l2, len(l1), len(l2)))
                similarity1 = 0
                similarity2 = 0
                try:
                    similarity1 = 2 * S0 / ( len(l0) + len(l1) )
                except ZeroDivisionError as e:
                    similarity1 = 0
                try:
                    similarity2 = 2 * S1 / ( len(l2) + len(l3) )
                except ZeroDivisionError as e:
                    similarity2 = 0

                similarityAABB = (similarity1 + similarity2) / 2
                #print(similarityAABB)
                phoneticsAABB.append(similarityAABB)
                similarity1 = 0
                similarity2 = 0
                try:
                    similarity1 = 2 * S2 / ( len(l0) + len(l2) )
                except ZeroDivisionError as e:
                    similarity1 = 0
                try:
                    similarity2= 2 * S3 / ( len(l1) + len(l3) )
                except ZeroDivisionError as e:
                    similarity2 = 0

                similarityABAB = (similarity1 + similarity2) / 2
                #print(similarityABAB)
                phoneticsABAB.append(similarityABAB)
                similarity1 = 0
                similarity2 = 0
                try:
                    similarity1 = 2 * S4 / ( len(l0) + len(l3) )
                except ZeroDivisionError as e:
                    similarity1 = 0
                try:
                    similarity2 = 2 * S5 / ( len(l1) + len(l2) )
                except ZeroDivisionError as e:
                    similarity2 = 0

                similarityABBA = (similarity1 + similarity2) / 2
                #print(similarityABBA)
                phoneticsABBA.append(similarityABBA)
            except UnicodeEncodeError: # Dont do anything if any Soundex failed 
                print("Error occurred with soundex")
                print(last_words)
                print("\nSome of these words failed")
    
    #print(phoneticsAABB)

    plot(results_path + title + "_AABB_phonetic.png", phoneticsAABB, title + " AABB phonetics")
    plot(results_path + title + "_ABAB_phonetic.png", phoneticsABAB, title + " ABAB phonetics")
    plot(results_path + title + "_ABBA_phonetic.png", phoneticsABBA, title + " ABBA phonetics")

    print(title)
    print("AABB\n")
    stats(phoneticsAABB)
    print("ABAB\n")
    stats(phoneticsABAB)
    print("ABBA\n")
    stats(phoneticsABBA)

def plot(path, data, title):
    unique = list(set(data))

    freq = []
    
    for u in unique:
        c = data.count(u)
        freq.append(c)

    plt.bar(unique, freq, align="center", width=0.02)

    plt.title(title)
    plt.xlabel("Edit distance")
    plt.ylabel("Frequency")
    if config.action == "save":
        plt.savefig(path)
        plt.close()
    else:
        plt.show()

def largest_common_substring(X, Y, m, n):
    LCSuff = [[0 for i in range(n + 1)]
              for j in range(m + 1)]

    # To store length of the
    # longest common substring
    length = 0

    # To store the index of the cell
    # which contains the maximum value.
    # This cell's index helps in building
    # up the longest common substring
    # from right to left.
    row, col = 0, 0

    # Following steps build LCSuff[m+1][n+1]
    # in bottom up fashion.
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 or j == 0:
                LCSuff[i][j] = 0
            elif X[i - 1] == Y[j - 1]:
                LCSuff[i][j] = LCSuff[i - 1][j - 1] + 1
                if length < LCSuff[i][j]:
                    length = LCSuff[i][j]
                    row = i
                    col = j
            else:
                LCSuff[i][j] = 0

    # if true, then no common substring exists
    if length == 0:
        print("No Common Substring")
        return ""

    # allocate space for the longest
    # common substring
    resultStr = ['0'] * length

    # traverse up diagonally form the
    # (row, col) cell until LCSuff[row][col] != 0
    while LCSuff[row][col] != 0:
        length -= 1
        resultStr[length] = X[row - 1]  # or Y[col-1]

        # move diagonally up to previous cell
        row -= 1
        col -= 1

    # required longest common substring
    # print(''.join(resultStr))

    return ''.join(resultStr)

def stats(l):
    print("Median: ", statistics.median(l))
    print("Mean: ", statistics.mean(l))
    print("Standard deviation: ", statistics.stdev(l))
    print("Kurtosis: ", kurtosis(l))
    print("Skewness: ", skew(l))
    print("Maximum value: ", max(l))


def task8():

    raw_books = helpers.getBooks()

    

    for book_ref, raw_book in raw_books.items():

        title_ = config.books[book_ref]['title']

        chapters = preprocessing.preprocess(raw_book)

        first_last_words = preprocessing.only_first_and_last_words(chapters)

        four_lines = preprocessing.four_line_structure(chapters)

        phonetic(first_last_words, title_)

        four_line_phonetic(four_lines, title_)


if __name__ == "__main__":
    task8()
