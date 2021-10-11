
from nltk.corpus import gutenberg, stopwords
from nltk import FreqDist, tokenize, pos_tag, word_tokenize
from collections import Counter
from itertools import *
from pylab import *

special_characters = [",", ".", "/", "\"", ";", "-", "_", "!", "?", "(", ")", "--", ".\"", "!--", ",\"", ".--", "'", ":", "*", '""', '"', "``", "''", "'d", "'s", "l.", "Cf", "Keats", "Lawrence", 'Cf']

def main():
    #book = gutenberg.words("lawrence.txt")
    with open("keats.txt", "r") as file:
        text = ""
        line = file.readline()
        while line:
            text += line.rstrip()
            line = file.readline()
        #print(text)
        tokens = word_tokenize(text)
    #print(tokens)
    list = get_most_frequent_words(tokens)
    part_of_speech(tokens)
    #for line in list:
    #    write_file(line[0], line[1], "keats.txt")
      
    #zipf(book)
    
def get_most_frequent_words(book):

    """
    Make a zipf law fitting line to the plot
    """
    #allWords = tokenize.word_tokenize(book)
    allWordDist = FreqDist(w.lower() for w in book)
    
    
    sw = stopwords.words('english')
    #print(sw)
    newList = list(book)
    for w in book:
        if w.lower() in sw or w.lower() in special_characters:
            newList.remove(w)
    #allWordExceptStopDist = FreqDist(w.lower() for w in book if w not in sw and w not in special_characters)
    allWordExceptStopDist = FreqDist(newList)
    allWordExceptStopDist.plot(30, cumulative=False)
    mostCommon = allWordExceptStopDist.most_common(30)
    #mostCommon
    print(mostCommon)
    
    return mostCommon
    
    
def write_file(word, frequency, file):
    with open(file, "a") as file:
        file.write(word+","+str(frequency)+"\n")

def poem_lines(poem):
    """
    Create something to extract the poems from the book, and then find the line lenghts of each poem (number of characters, so basically len(line))
    """
    
    
def part_of_speech(book):
    pos = pos_tag(book)
    freq = FreqDist(pos)
    print(pos)
    freq.plot(30, cumulative=False)
    
    for line in freq:
        write_file(line[0], line[1], "keats-pos.txt")
    
def zipf(book):
    """
    not working yet! most likely will never be used, the zipf law should probably be made into
    the get most_frequent_words function...
    """
    
    
    tokens_with_count = Counter(w.lower() for w in book)
    counts = array(tokens_with_count.values())
    print(tokens_with_count)
    print(counts)
    tokens = tokens_with_count.keys()
    print(len(counts))
    ranks = arange(1, len(counts)+1)
    indices = argsort(-counts)
    frequencies = counts[indices]
    loglog(ranks, frequencies, marker=".")
    title("Zipf plot for book tokens")
    xlabel("Frequency rank of token")
    ylabel("Absolute frequency of token")
    grid(True)
    for n in list(logspace(-0.5, log10(len(counts)), 20).astype(int)):
        dummy = text(ranks[n], frequencies[n], " " + tokens[indices[n]], 
                     verticalalignment="bottom",
                     horizontalalignment="left")

    show()

if __name__ == "__main__":
    main()