from nltk.sentiment import SentimentIntensityAnalyzer
import csv
import nlp_config as config
import nlp_helpers as helpers
import preprocessing


# constants
results_path = 'results/6/'

# TASK DESCRIPTION
# 6. Sentiment analysis
# We want to investigate the variation of the sentiment across lines of poem and chapters.
# Use NLTK sentiment analyzer of your choice to calculate the overall sentiment of each line of the poem
# as well as sentiment of starting word and ending word of each line.
# Save your response in an excel file.
# Use illustrations of your choice to visualize the sentiment across lines and chapters,
# and another illustration to visualize the possible compatibility of starting and ending word in each line of the poem


def analyze_the_sentiment_of_structure(book_: dict, sentiments: list) -> dict:
    retval = dict()
    for sentiment in sentiments:
        retval[sentiment] = []
    # this can surely be initiated in a better python way

    sia = SentimentIntensityAnalyzer()
    # iterate through books
    for title, chapter in book_.items():
        for line in chapter:
            scores = sia.polarity_scores(line)
            # {'neg': 0.0, 'neu': 0.295, 'pos': 0.705, 'compound': 0.8012}

            for sentiment in sentiments:
                retval[sentiment].append(scores[sentiment])
    return retval


def analyze_the_sentiment_of_structure_2(book_: dict, sentiments: list) -> dict:
    retval = dict()
    for sentiment in sentiments:
        retval[sentiment] = [[], []]
    # this can surely be initiated in a better python way

    sia = SentimentIntensityAnalyzer()
    # iterate through chapters
    for title, chapter in book_.items():
        for words in chapter:
            scores_first = sia.polarity_scores(words[0])
            scores_last = sia.polarity_scores(words[1])
            # example: {'neg': 0.0, 'neu': 0.295, 'pos': 0.705, 'compound': 0.8012}

            for sentiment in sentiments:
                retval[sentiment][0].append(scores_first[sentiment])
                retval[sentiment][1].append(scores_last[sentiment])
    return retval


def save_to_CSV(structure: list, name: str):
    with open(name + '.csv', mode='w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for score in structure:
            csv_writer.writerow([str(score)])


def save_to_CSV_2(structure: list, name: str):
    with open(name + '.csv', mode='w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for score in structure:
            csv_writer.writerow(score)


def prepare_for_CSV(structures: list) -> [list]:
    retval = [[] for i in range(len(structures[0]))]
    for structure in structures:
        for i, value in enumerate(structure):
            retval[i].append(structure[i])
    for val in retval:
        val = ','.join(str(val))
    return retval


def task6():
    raw_books = helpers.getBooks()
    sentiment_type = helpers.Sentiments.COMPOUND.value

    for book_ref, raw_book in raw_books.items():
        title_ = config.books[book_ref]['title']
        chapters = preprocessing.preprocess(raw_book)
        first_last_words = preprocessing.only_first_and_last_words(chapters)

        chapters_sentiment = analyze_the_sentiment_of_structure(chapters, [sentiment_type])
        save_to_CSV(chapters_sentiment[sentiment_type], results_path + book_ref + "_sentiment_per_line")

        first_last_words_sentiment = analyze_the_sentiment_of_structure_2(first_last_words, [sentiment_type])
        first_last_words_sentiment_prepared = prepare_for_CSV(first_last_words_sentiment[sentiment_type])
        save_to_CSV_2(first_last_words_sentiment_prepared, results_path + book_ref + "_sentiment_f_l_word")

        # visualize results

        # sentiment analysis per each row
        path = results_path + book_ref + '_sentiment_analysis_per_row'
        title = title_ + ' sentiment analysis per each row'
        helpers.plotting(path=path, y=chapters_sentiment[sentiment_type], title=title)

        # sentiment analysis per first word in lines
        path = results_path + book_ref + '_sentiment_analysis_per_first_word'
        title = title_ + ' sentiment analysis per first words'
        helpers.plotting(path=path, y=first_last_words_sentiment[sentiment_type][0], title=title)

        # sentiment analysis per last word in lines
        path = results_path + book_ref + '_sentiment_analysis_per_last_word'
        title = title_ + ' sentiment analysis per last words'
        helpers.plotting(path=path, y=first_last_words_sentiment[sentiment_type][1], title=title)


if __name__ == "__main__":
    task6()
