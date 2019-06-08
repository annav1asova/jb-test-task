from datetime import datetime
from collections import Counter
from arxiv_feed_getter import get_feed
from view_format_utils import convert_to_data_frame

import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()
decade_period = 10


def prepare_table(search_request):
    """
    take search request and returns data frame that has to be displayed for this request.
    value at this data frame for row x and column y: word (z)
    where "word" is the x-th most frequently used word at the article names of period y.
    z is this word frequency
    also return number of found articles
    """
    add_extra_stopwords()
    feed = get_feed(search_request)
    decades = get_decades_words_info(feed)
    decades_df = convert_to_data_frame(decades)
    num_articles = len(feed.entries)

    return decades_df, num_articles


def get_decades_words_info(feed):
    """
    count word frequency based on feed
    :return: dict, keys are start years of different decades, values are Counters of words
    """
    decades = {}
    for article in feed.entries:
        year = datetime.strptime(article.published,'%Y-%m-%dT%H:%M:%SZ').year
        cur_decade_start = year - year % decade_period
        add_title(cur_decade_start, article.title, decades)

    return decades


def add_title(decade_start, title, decades):
    if decade_start not in decades:
        decades[decade_start] = Counter()

    word_tokens = word_tokenize(title.lower())
    filtered_words = [normalize(w) for w in word_tokens if (w.isalpha()) and (not w in stop_words)]
    decades[decade_start].update(filtered_words)


def add_extra_stopwords():
    roman_numerals = ['i', 'ii', 'iii', 'iv', 'v', 'x'] # common roman numerals
    stop_words.update(roman_numerals)


def normalize(word):
        return lemmatizer.lemmatize(word)
