from datetime import datetime
from collections import Counter
from pandas import Series, DataFrame
from arxiv_feed_getter import get_feed
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

stop_words = set(stopwords.words('english'))
top_results = 10
decade_period = 10


def start_year_to_interval(x):
    return str(x) + " — " + str(x + (decade_period - 1))


def to_view_format(word_info):
    word, frequency = word_info
    word_view = "%s (%s)" % (word, str(frequency))
    return word_view


def add_title(decade_start, title, decades):
    if decade_start not in decades:
        decades[decade_start] = Counter()

    word_tokens = word_tokenize(title.lower())
    filtered_words = [w for w in word_tokens if (w.isalpha()) and (not w in stop_words)]
    decades[decade_start].update(filtered_words)


def get_top_results(decades):
    decades_top_words = {}
    for decade_start in decades:
        num_words = min(top_results, len(decades[decade_start]))
        most_common_words = decades[decade_start].most_common(num_words)
        decades_top_words[decade_start] = [to_view_format(most_common_words[i]) for i in range(num_words)]

    return decades_top_words


def get_decades_words_info(feed):
    decades = {}
    for article in feed.entries:
        year = datetime.strptime(article.published,'%Y-%m-%dT%H:%M:%SZ').year
        cur_decade_start = year - year % decade_period
        add_title(cur_decade_start, article.title, decades)

    return decades


def convert_to_data_frame(decades):
    decades_df = DataFrame(dict([(k, Series(v)) for k, v in decades.items()])).fillna('')
    decades_df = decades_df.reindex(sorted(decades_df.columns), axis=1)
    decades_df.rename(start_year_to_interval, axis='columns', inplace=True)
    decades_df.rename(lambda x: x + 1, axis='rows', inplace=True)
    return decades_df


def prepare_table(search_request):
    feed = get_feed(search_request)
    decades_all_words = get_decades_words_info(feed)
    decades_top_words = get_top_results(decades_all_words)
    decades_df = convert_to_data_frame(decades_top_words)
    num_articles = len(feed.entries)

    return decades_df, num_articles
