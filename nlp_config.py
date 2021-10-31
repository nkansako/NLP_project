# sources
books = dict(
    keats_lamia=dict(
        title='Keats 1820',
        author='Keats',
        path='keats.txt',
    ),
    blake_songs_of_innocence=dict(
        title='Songs of innocence',
        author='Blake',
        path='blake.txt',
    ),
)

# actions
action = 'save'  # 'save' to save plots into files, any other value to visualize results
plot_bar_color = 'blue'

# preprocessing data
special_characters = [",", ".", "/", "\"", ";", "-", "_", "!", "?", "(", ")", "--", ".\"", "!--", ",\"", ".--", "'", ":", "*", '""', '"', "``", "''", "'d", "'s", "l.", "Cf", "Keats", "Lawrence", 'Cf', '’', '—', '‘']
negations = ["no", "none", "never", "isn't", "ain't", "doesn't", "wont", "nothing", "don't", "nowhere", "not", "hasn't", "hadn't", "couldn't", "shouldn't", "wouldn't", "didn't", "aren't", "mightn't", "wasn't", "weren't", "mustn't", "needn't", "shan't", "nor", "needn't", "nobody", "nothing", "neither", "none", "hardly", "scarcely", "barely", "cannot"]
trim_values = ["'", "\"", "-", ",", ".", ";", ":", "?", "!", "Æ", 'ü', '’', '—', "”", "è", "æ", "é", "ä", "ç"]

# phonetic analysis
similarity_threshold = .5
display_top = 10
negation_prefix = ["im", "non", "un", "in", "de", "dis", "a", "anti", "il", "ir"]

#Select corpus
corpus = "bown" # Can be slow, default to nltk.corpus.words if not specified to be brown
