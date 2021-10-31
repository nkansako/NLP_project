from nltk.sentiment.vader import SentimentIntensityAnalyzer
import csv
import nlp_config as config
import nlp_helpers as helpers
import preprocessing
import matplotlib.pyplot as plt

# constants
results_path = 'results/6/'
sia = SentimentIntensityAnalyzer()


# TASK DESCRIPTION
# 6. Sentiment analysis
# We want to investigate the variation of the sentiment across lines of poem and chapters.
# Use NLTK sentiment analyzer of your choice to calculate the overall sentiment of each line of the poem
# as well as sentiment of starting word and ending word of each line.
# Save your response in an excel file.
# Use illustrations of your choice to visualize the sentiment across lines and chapters,
# and another illustration to visualize the possible compatibility of starting and ending word in each line of the poem


def analyze_the_sentiment_of_structure(book_: dict, sentiments: list = helpers.Sentiments) -> dict:
    retval = dict()
    for sentiment in sentiments:
        sentiment = sentiment.value
        retval[sentiment] = []
    # this can surely be initiated in a better python way

    # iterate through books
    for title, chapter in book_.items():
        for line in chapter:
            # analysis per LINES
            scores = sia.polarity_scores(line)
            # {'neg': 0.0, 'neu': 0.295, 'pos': 0.705, 'compound': 0.8012}

            for sentiment in sentiments:
                sentiment = sentiment.value
                retval[sentiment].append(scores[sentiment])
    return retval


def analyze_the_sentiment_of_structure_2(book_: dict, sentiments: list = helpers.Sentiments) -> list:
    retval = [dict(), dict()]
    for sentiment in sentiments:
        retval[0][sentiment.value] = []
        retval[1][sentiment.value] = []
    # this can surely be initiated in a better python way

    # iterate through chapters
    for title, chapter in book_.items():
        for words in chapter:
            # analysis per FIRST WORD and LAST WORD
            scores_first = sia.polarity_scores(words[0])
            scores_last = sia.polarity_scores(words[1])
            # example: {'neg': 0.0, 'neu': 0.295, 'pos': 0.705, 'compound': 0.8012}

            for sentiment in sentiments:
                retval[0][sentiment.value].append(scores_first[sentiment.value])
                retval[1][sentiment.value].append(scores_last[sentiment.value])
    return retval


def save_to_CSV(structure: dict, name: str):
    with open(name + '.csv', mode='w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for score_type, score in structure.items():
            i = 0
            for rows in score:
                if i == 0:
                    csv_writer.writerow([type_ for type_ in structure.keys()])
                csv_writer.writerow([structure[type_][i] for type_ in structure.keys()])
                i += 1
            break


def save_to_CSV_2(structure: list, name: str):
    with open(name + '.csv', mode='w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for i in range(len(structure[0]['neg'])):
            if i == 0:
                csv_writer.writerow(
                    [row_name + " first" for row_name, content in structure[0].items()] +
                    [row_name + " last" for row_name, content in structure[1].items()]
                )
            csv_writer.writerow([structure[0][type_][i] for type_ in structure[0].keys()]
                                + [structure[1][type_][i] for type_ in structure[1].keys()])
            i += 1


def calculate_mid_values(sentiments: dict, lines_count) -> dict:
    results = dict()
    for sent_type in helpers.Sentiments:
        results[sent_type.value] = sum(score for score in sentiments[sent_type.value]) / lines_count
    return results


def calculate_mid_values_2(sentiments: list, lines_count) -> list:
    results = [dict(), dict()]
    for sent_type in helpers.Sentiments:
        results[0][sent_type.value] = sum(score for score in sentiments[0][sent_type.value]) / lines_count
        results[1][sent_type.value] = sum(score for score in sentiments[1][sent_type.value]) / lines_count
    return results


def task6():
    raw_books = helpers.getBooks()

    for book_ref, raw_book in raw_books.items():
        title_ = config.books[book_ref]['title']
        chapters = preprocessing.preprocess(raw_book)
        first_last_words = preprocessing.only_first_and_last_words(chapters)

        chapters_sentiment = analyze_the_sentiment_of_structure(chapters)
        # print(chapters_sentiment)
        results_lines = calculate_mid_values(chapters_sentiment, helpers.totalLinesPerBook(chapters))

        save_to_CSV(chapters_sentiment, results_path + book_ref + "_sentiment_per_line")

        first_last_words_sentiment = analyze_the_sentiment_of_structure_2(first_last_words)
        save_to_CSV_2(first_last_words_sentiment, results_path + book_ref + "_sentiment_f_l_word")

        # visualize results

        # sentiment analysis per each row
        path = results_path + book_ref + '_sentiment_analysis_per_row'
        title = title_ + ' sentiment analysis per each row'
        x = [key for key in results_lines.keys()]
        helpers.plotting(path=path, y=results_lines.values(), x=x, title=title, fn="bar", ylabel="Sentiment score",
                         xlabel="Sentiment type")

        # # sentiment analysis per first word in lines
        path = results_path + book_ref + '_sentiment_analysis_per_first_vs_last_words'
        results_lines_2 = calculate_mid_values_2(first_last_words_sentiment, helpers.totalLinesPerBook(chapters))

        plt.bar(x, results_lines_2[0].values(), color='blue', alpha=0.3)
        plt.bar(x, results_lines_2[1].values(), color='red', alpha=0.7)
        title = title_ + ' sentiment analysis per first(blue) vs last(red) words'
        plt.title(title)
        plt.ylabel("Sentiment score")
        plt.xlabel("Sentiment type")
        if config.action == 'save':
            plt.savefig(path)
            plt.close()
        else:
            plt.show()


if __name__ == "__main__":
    task6()
