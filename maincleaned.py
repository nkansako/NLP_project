from nltk.corpus import gutenberg, stopwords
from nltk import FreqDist, tokenize, pos_tag, word_tokenize
from collections import Counter
import matplotlib.pyplot as plt
import sys
import os
import re
from scipy.stats import kurtosis
from scipy.stats import skew
import statistics
from scipy.optimize import curve_fit
from scipy.special import zetac
import fuzzy

def f(x, a):
    return (x**-a)/zetac(a)

special_characters = [",", ".", "/", "\"", ";", "-", "_", "!", "?", "(", ")", "--", ".\"", "!--", ",\"", ".--", "'", ":", "*", '""', '"', "``", "''", "'d", "'s", "l.", "Cf", "Keats", "Lawrence", 'Cf', '’', '‘', '’']

negations = ["no", "none", "never", "isn't", "ain't", "doesn't", "wont", "nothing", "don't", "nowhere", "not", "hasn't", "hadn't", "couldn't", "shouldn't", "wouldn't", "didn't", "aren't", "mightn't", "wasn't", "weren't", "mustn't", "needn't", "shan't", "nor", "needn't", "nobody", "nothing", "neither", "none", "hardly", "scarcely", "barely", "cannot"]

def main():
    b = books()
    
    for book in b:
        chapters = preprocess(book)
        first_last = only_first_and_last_words(chapters)
        #most_frequent_words(chapters)
        #part_of_speech(chapters)
        #line_lenghts(chapters)
        #count_negations(chapters)
        #newFreq(chapters)
        phonetic(first_last)
        
def most_frequent_words(book):
    allwords = ""
    name = ""
    try: 
        a = book["LAMIA."]
        name = "Keats"
    except KeyError as e:
        name = "Blake"
    for title, chapter in book.items():
        for line in chapter:
            newline = remove_stop_words(remove_stop_words(remove_stop_words(line))).lower()
            
            allwords += newline
    
    words = word_tokenize(allwords)
    
    fd = FreqDist(words)
    fd.plot(30, cumulative=False, title="Most frequent words "+name)
    
    
def part_of_speech(book):
    allwords = ""
    name = ""
    try: 
        a = book["LAMIA."]
        name = "Keats"
    except KeyError:
        name = "Blake"
    for title, chapter in book.items():
        for line in chapter:
            newline = remove_stop_words(remove_stop_words(remove_stop_words(line))).lower()
            
            allwords += newline
    
    words = word_tokenize(allwords)
    
    pos = pos_tag(words)
    tags = []
    for _ in pos:
        tags.append(_[1])
    #print(tags)
    unique = list(set(tags))
    freq = []
    new = []
    for u in unique:
        c = tags.count(u)
        freq.append(c)
        new.append(u)
    
    zipped = zip(unique, freq)
    
    s = sorted(zipped, key=lambda x: x[1], reverse=True)
    
    for _ in s:
        #plt.bar(unique, freq)
        plt.bar(_[0], _[1], color="blue")
    t = "Part of speech frequency "+name
    plt.title(t)
    plt.show()
    
def preprocess(raw_book: str) -> dict:
    # cleanup
    chapters = dict()
    text_buffer = []  # this variable is used to save lines into an array before putting them into a chapter
    chapter_name = ''  # name of the current chapter
    for line in raw_book.splitlines():
        line_cleaned = re.sub(' +', ' ', line).strip()  # removing multiple & first-last whitespaces from the line
        if line_cleaned:
            # not an empty line
            if line_cleaned.isupper():
                # all upper case defines a beginning of a new chapter
                if text_buffer:
                    # if the buffer contains lines, save them as a new chapter
                    chapters[chapter_name] = text_buffer
                    text_buffer = []
                chapter_name = line_cleaned
            else:
                # not uppercase - normal text
                # some lines end with a number; remove the numbers
                tokens = line_cleaned.split(' ')
                if tokens[len(tokens)-1].isnumeric():
                    tokens.pop()  # remove last token
                text_buffer.append(' '.join(tokens))
            chapters[chapter_name] = text_buffer
          
    return chapters

def remove_stop_words(line: str) -> str:
    # return line
    words = word_tokenize(line)
    sw = stopwords.words('english')
    for word in words:
        if word.lower() in sw or word.lower() in special_characters:
            words.remove(word)
            
    return ' '.join(words)


def books() -> list:
    books_path = ['keats.txt', 'blake.txt']  # TODO: should be read from a config file
    books_ = [] # TODO: make this an associative array: book_name -> book_content
    for book_path in books_path:
        with open(book_path, "r", encoding="UTF-8") as file:
            text = ""
            line = file.readline()
            while line:
                text += line.strip() + os.linesep
                line = file.readline()
            books_.append(text)
            
    return books_
    
def line_lenghts(book):
    name = ""
    lengths = []
    lengths_no_space = []
    try: 
        a = book["LAMIA."]
        name = "Keats"
    except KeyError:
        name = "Blake"
    for title, chapter in book.items():
        for line in chapter:
            length = len(line)
            length2 = len(line.replace(" ",""))
            if length > 1:
                lengths.append(length)
                
            if length2 > 1:
                lengths_no_space.append(length2)
                
    uniquel1 = list(set(lengths))
    
    uniquel2 = list(set(lengths_no_space))
    
    freq = []
    
    freq_no_space = []
    
    for u in uniquel1:
        c = lengths.count(u)
        
        freq.append(c)
        
    for u in uniquel2:
        c = lengths_no_space.count(u)
        
        freq_no_space.append(c)
        
    
    plt.plot(uniquel1, freq)
    t = "Line length frequency with space "+name
    plt.title(t)
    plt.xlabel("Line length")
    plt.ylabel("Frequency")
    plt.show()
    
    
    plt.plot(uniquel2, freq_no_space)
    t = "Line length frequency without space "+name
    plt.title(t)
    plt.xlabel("Line length")
    plt.ylabel("Frequency")
    plt.show()
        
    stats(uniquel1)
    stats(uniquel2)
    
def count_negations(book):
    negations_list = []
    count_negatives = 0
    count_lines = 0
    tags = []
    fd = FreqDist()
    try: 
        a = book["LAMIA."]
        name = "Keats"
        b = 4101
    except KeyError:
        name = "Blake"
        b = 845
    for title, chapter in book.items():
        for line in chapter:
            count_lines += 1
            tokens = word_tokenize(line)
            if count_lines < 5:
                for token in tokens:
                    if token in negations:
                        count_negatives += 1
                        tag = pos_tag(word_tokenize(token))
                        tags.append(tag[0][1])
            else:
                negations_list.append(count_negatives)
                count_lines = 0
                count_negatives = 0
                
                for token in tokens:
                    if token in negations:
                        count_negatives += 1
                        tag = pos_tag(word_tokenize(token))
                        tags.append(tag[0][1])
    #print(negations_list)
    #print(tags)
    unique = list(set(negations_list))
    
    freq = []
    
    for u in unique:
        c = negations_list.count(u)
        freq.append(c)
    
    freq = [f / (b / 5) * 100 for f in freq]
    
    #result = curve_fit(f, unique, freq)
    #print(result)
    
    plt.bar(unique, freq)
    t = "Negations for every 5 lines "+name 
    plt.title(t)
    plt.xlabel("Amount of negations found in 5 consecutive line structure")
    plt.ylabel("Percentage of 5 consecutive lines")
    plt.show()
    
    uniquetags = list(set(tags))
    
    freqtags = []
    
    for u in uniquetags:
        c = tags.count(u)
        freqtags.append(c)
    
    zipped = zip(uniquetags, freqtags)
    
    s = sorted(zipped, key=lambda x: x[1], reverse=True)
    
    for _ in s:
        #plt.bar(unique, freq)
        plt.bar(_[0], _[1], color="blue")
    
    #plt.bar(uniquetags, freqtags)
    t = "Negations part of speech tag "+name 
    plt.title(t)
    plt.xlabel("Part of speech tag")
    plt.ylabel("Frequency of part of speech tags")
    plt.show()
    
    
def newFreq(book):
    """
    This was a test to try this out, doesnt seem to work 
    """
    fd = FreqDist()
    try: 
        a = book["LAMIA."]
        name = "Keats"
        b = 4101
    except KeyError:
        name = "Blake"
        b = 845
    for title, chapter in book.items():
        for line in chapter:
            newline = remove_stop_words(remove_stop_words(remove_stop_words(line))).lower()
            words = word_tokenize(newline)
            for word in words:
               fd[word] += 1 
   
    ranks = []
    freqs = []
   
    for rank, word in enumerate(fd):
        ranks.append(rank+1)
        freqs.append(fd[word])
        
    t = "Most frequent words "+name
    plt.loglog(ranks, freqs)
    plt.title(t)
    plt.xlabel('frequency(f)', fontsize=14, fontweight='bold')
    plt.ylabel('rank(r)', fontsize=14, fontweight='bold')
    plt.grid(True)
    plt.show()
    
def stats(l):
    print("Median: ", statistics.median(l))
    print("Mean: ", statistics.mean(l))
    print("Standard deviation: ", statistics.stdev(l))
    print("Kurtosis: ", kurtosis(l))
    print("Skewness: ", skew(l))
    print("Maximum value: ", max(l))


def only_first_and_last_words(book_: dict) -> dict:
    retval = dict()
    for title, chapter in book_.items():
        new_chapter = []
        for line in chapter:
            # removing stopwords, since they don't contribute to the sentiment
            line_ = remove_stop_words(remove_stop_words(remove_stop_words(line))) # run twice for better efficiency
            tokens = line_.split(' ')
            new_chapter.append([tokens[0], tokens[len(tokens)-1]])
        retval[title] = new_chapter
    return retval
    
def phonetic(book):
    print(book)
    phonetics = []
    try: 
        a = book["LAMIA."]
        name = "Keats"
    except KeyError:
        name = "Blake"
    for title, chapter in book.items():
        for line in chapter:
            first = line[0]
            last = line[1]
            s1 = fuzzy.Soundex(len(first))
            s2 = fuzzy.Soundex(len(last))
            print(first, last) #show what happens
            l1 = s1(first) # These fail with non ascii characters
            l2 = s2(last)
            print(l1, l2)
            
            S = len(largest_common_substring(l1, l2, len(l1), len(l2)))
            try:
                similarity = 2 * S / ( len(l1) + len(l2) )
            except ZeroDivisionError as e:
                similarity = 0
            phonetics.append(similarity)
        
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
        resultStr[length] = X[row - 1] # or Y[col-1]
 
        # move diagonally up to previous cell
        row -= 1
        col -= 1
 
    # required longest common substring
    #print(''.join(resultStr))
    
    return ''.join(resultStr)
    
if __name__ == "__main__":
    main()