# sources
books = dict(
    keats_lamia=dict(
        title='LAMIA',
        author='Keats',
        path='keats.txt',
    ),
    blake_songs_of_innocence=dict(
        title='SONGS OF INNOCENCE',
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
