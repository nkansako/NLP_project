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

special_characters = [",", ".", "/", "\"", ";", "-", "_", "!", "?", "(", ")", "--", ".\"", "!--", ",\"", ".--", "'", ":", "*", '""', '"', "``", "''", "'d", "'s", "l.", "Cf", "Keats", "Lawrence", 'Cf', '’', '‘', '’']

negations = ["no", "none", "never", "isn't", "ain't", "doesn't", "wont", "nothing", "don't", "nowhere", "not", "hasn't", "hadn't", "couldn't", "shouldn't", "wouldn't", "didn't", "aren't", "mightn't", "wasn't", "weren't", "mustn't", "needn't", "shan't", "nor", "needn't", "nobody", "nothing", "neither", "none", "hardly", "scarcely", "barely", "cannot"]

def main():
    b = books()
    
    for book in b:
        chapters = preprocess(book)
        #most_frequent_words(chapters)
        #part_of_speech(chapters)
        #line_lenghts(chapters)
        count_negations(chapters)

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
   
    plt.bar(unique, freq)
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
            else:
                negations_list.append(count_negatives)
                count_lines = 0
                count_negatives = 0
                
                for token in tokens:
                    if token in negations:
                        count_negatives += 1
    #print(negations_list)
    
    unique = list(set(negations_list))
    
    freq = []
    
    for u in unique:
        c = negations_list.count(u)
        freq.append(c)
    
    freq = [f / (b / 5) * 100 for f in freq]
    
    plt.bar(unique, freq)
    t = "Negations for every 5 lines "+name 
    plt.title(t)
    plt.xlabel("Amount of negations found in 5 consecutive line structure")
    plt.ylabel("Percentage of 5 consecutive lines")
    plt.show()
    
def stats(l):
    print("Median: ", statistics.median(l))
    print("Mean: ", statistics.mean(l))
    print("Standard deviation: ", statistics.stdev(l))
    print("Kurtosis: ", kurtosis(l))
    print("Skewness: ", skew(l))
    print("Maximum value: ", max(l))

if __name__ == "__main__":
    main()