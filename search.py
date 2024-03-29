import numpy as np
from text_processor import bag_of_words, prepare_text, filter_words
from common import read_file, read_articles
from scipy import sparse
from scipy.sparse import linalg
from flask import Flask, request, render_template

app = Flask(__name__)


def prepare_phrase(phrase, words):
    p = filter_words(prepare_text(phrase))
    bow = bag_of_words(p)
    return np.array([bow.get(w, 0) for w in words])


def correlation(phrase_words, article_words):
    return phrase_words.T @ article_words


def match(phrase_words, search_matrix):
    matches = []
    pw = phrase_words/(np.linalg.norm(phrase_words))
    for i, a_w in enumerate(search_matrix):
        if i % 1000 == 0:
            print("Searched in {0} articles".format(i))
        matches.append((i, correlation(pw, a_w.T)[0]))
        # matches.append((i, correlation(pw, a_w)))
    matches.sort(key=lambda x: x[1], reverse = True)
    return matches[:10]


# size=142572
# size = 1000
size = 10000
print("Loading words...")
words = np.array(read_file('words_{0}.txt'.format(size)).split(','))
words.sort()
print("Words loaded: " + str(len(words)))

print("Loading matrix...")
search_matrix = sparse.load_npz('matrix_{0}_normalized.npz'.format(size))
# search_matrix = np.load('matrix_{0}_denoised.npy'.format(size))
print("Matrix loaded: " + str(search_matrix.shape))

print("Loading articles...")
articles = read_articles()[1:]


def search(phrase):
    phrase_words = prepare_phrase(phrase, words)
    return [(i, c) for i, c in match(phrase_words, search_matrix)]


class Article:
    def __init__(self, title, content, correlation):
        self.title = title
        self.content = content
        self.correlation = correlation


@app.route("/", methods=['GET'])
def get_searches():
    phrase = request.args.get('phrase')
    response = []
    for i, c in search(phrase):
        article = Article(articles[i][2], articles[i][-1], c)
        response.append(article)
    return render_template('index.html', articles=response)