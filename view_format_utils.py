from pandas import DataFrame, Series

top_results = 10

def convert_to_data_frame(decades):
    """
    take info about frequency of all words for each decade and converts it to data frame, which would be seen by users
    :param decades: dict, keys are start years of different decades, values are Counters of words
    """
    decades_top_words = get_top_results(decades)
    decades_df = DataFrame(dict([(k, Series(v)) for k, v in decades_top_words.items()])).fillna('')
    decades_df = decades_df.reindex(sorted(decades_df.columns), axis=1)
    decades_df.rename(start_year_to_interval, axis='columns', inplace=True)
    decades_df.rename(lambda x: x + 1, axis='rows', inplace=True)
    return decades_df


def get_top_results(decades):
    """
    remain only top of most frequently used words
    :return: cropped version of param decades, each decade contains at most 10 words
    """
    decades_top_words = {}
    for decade_start in decades:
        num_words = min(top_results, len(decades[decade_start]))
        most_common_words = decades[decade_start].most_common(num_words)
        decades_top_words[decade_start] = [cell_format(most_common_words[i]) for i in range(num_words)]

    return decades_top_words


def cell_format(word_info):
    word, frequency = word_info
    word_view = "%s (%i)" % (word, frequency)
    return word_view


def start_year_to_interval(x, period=10):
    return str(x) + " — " + str(x + (period - 1))
