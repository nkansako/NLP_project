
from nltk.corpus import gutenberg, stopwords
from nltk import FreqDist, tokenize
from collections import Counter
from itertools import *
from pylab import *

special_characters = [",", ".", "/", "\"", ";", "-", "_", "!", "?", "(", ")", "--", ".\"", "!--", ",\"", ".--", "'", ":"]

def main():
    book = gutenberg.words("lawrence.txt")
    list = get_most_frequent_words(book)
    #for line in list:
    #    write_file(line[0], line[1])
      
    zipf(book)
    
def get_most_frequent_words(book):
    #allWords = tokenize.word_tokenize(book)
    allWordDist = FreqDist(w.lower() for w in book)
    
    
    sw = stopwords.words('english')
    allWordExceptStopDist = FreqDist(w.lower() for w in book if w not in special_characters and w not in sw)
    allWordExceptStopDist.plot(30, cumulative=False)
    mostCommon = allWordExceptStopDist.most_common(30)
    
    print(mostCommon)
    
    return mostCommon
    
    
def write_file(word, frequency):
    with open("words.txt", "a") as file:
        file.write(word+","+str(frequency)+"\n")


def zipf(book):
    """
    not working yet!
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