import matplotlib.pyplot as plt
from nltk import FreqDist
import nlp_config as config
import nlp_helpers as helpers
import preprocessing
import fuzzy
import numpy as np
import string

# constants
results_path = 'results/8a/'


# TASK DESCRIPTION
# Extra task, self-initiative.
# Use phonetic analysis to find rhyming. Match first words, last words and whole lines.
# If the phonetic distance between some of two analysed lines is bigger than a defined threshold, mark them as rhyming.
# Match distances across whole chapters, and mark the rhyming lines with the same letter.
# Plot the variety of occurrences for the top 10 reoccurring patterns per each ebook.


def rhyme_analysis(chapters: list, analysis_type: helpers.AnalysisTypes, threshold: float):

    rhyme_types = []

    for chapter in chapters:
        lengths = []

        if len(chapter) == 1:
            continue  # we skip chapters with 1 lines

        for line in chapter:
            text = helpers.prepare_string(line, analysis_type)
            lines_per_batch = []

            soundex = fuzzy.Soundex(len(text))
            try:
                length = soundex(text)
                lengths.append(length)
                lines_per_batch.append(text)
            except UnicodeEncodeError:
                print("Add exception character to nlp_config.trim_values: " + text)

        results_length = len(lengths)
        matches = np.zeros([results_length, results_length])
        for j in range(results_length):
            for k in range(results_length):
                if j == k:
                    matches[j][k] = 1
                else:
                    S = len(largest_common_substring(lengths[j], lengths[k], len(lengths[j]), len(lengths[k])))
                    try:
                        similarity = 2 * S / (len(lengths[j]) + len(lengths[k]))
                    except ZeroDivisionError:
                        similarity = 0
                    matches[j][k] = similarity

        unique_pattern_letters = string.ascii_uppercase
        current_pattern_letter_index = 0

        current_pattern = [""] * results_length
        current_pattern[0] = unique_pattern_letters[current_pattern_letter_index]
        next_letter = 1
        for j in range(results_length):
            br = False
            for k in range(results_length):
                if j != k:
                    if current_pattern[k] == "":
                        if matches[j][k] >= threshold:
                            current_pattern[k] = unique_pattern_letters[current_pattern_letter_index]
                            next_letter += 1
            if next_letter > 1:  # use a letter at least twice
                current_pattern_letter_index += 1
                next_letter = 0
                if current_pattern_letter_index >= len(unique_pattern_letters):
                    br = True
                    break
            if br:
                break

        for i in range(len(current_pattern)):
            if current_pattern[i] == "":
                current_pattern_letter_index += 1 * next_letter
                current_pattern[i] = unique_pattern_letters[current_pattern_letter_index]
                next_letter = 1

        rhyme_types.append("".join(current_pattern))

    return FreqDist(rhyme_types)


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
        # print("No Common Substring")
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


def task8a():
    raw_books = helpers.getBooks()

    for book_ref, raw_book in raw_books.items():
        title_ = config.books[book_ref]['title']
        chapters = preprocessing.book_to_verses(raw_book)

        for analysis_type in helpers.AnalysisTypes:
            # print("Analyzing for:" + analysis_type.value)
            threshold = config.similarity_threshold
            fd = rhyme_analysis(chapters, analysis_type, threshold)
            title = "Phonetic analysis for *" + analysis_type.value + "*, book: " + title_ +\
                    ", similarity threshold: " + str(threshold)
            plt.figure(figsize=(30, 20))
            fd.plot(config.display_top, cumulative=False, title=title)


if __name__ == "__main__":
    task8a()
