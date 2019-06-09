import unittest
from collections import Counter

from request_processor import get_decades_words_info

class Article:
    def __init__(self, id, title, published):
        self.id = id
        self.title = title
        self.published = published

class TestFeed:
    feed = {"title": 'ArXiv Query: search_query=all:pollutants&id_list=&start=0&max_results=5'}
    entries = [Article("http://arxiv.org/abs/random_link",
                       "The content of pollutants of petroleum origin in the wastewater of petroleum processing plants",
                        '2006-03-29T00:16:49Z'),
               Article("http://arxiv.org/abs/random_link2",
                        "Distribution of the content of organochlorine pollutants in natural waters",
                        '2008-06-06T00:17:42Z'),
               Article("http://arxiv.org/abs/random_link3",
                        "Correlation of the concentration of organochlorine compounds with the content of pollutants of petroleum origin in sea waters",
                        '2007-06-06T00:17:42Z'),
               Article("http://arxiv.org/abs/random_link4",
                        "The influence of pollutants of petroleum origin on the distribution of the concentration of heavy metals in natural waters",
                        '2002-06-02T00:19:42Z')
                ]


class MyTest(unittest.TestCase):
    def test_one_decade(self):
        test_feed = TestFeed()


        test_ans = {2000: Counter({'pollutant': 4,
                'petroleum': 4,
                'content': 3,
                'origin': 3,
                'water': 3,
                'distribution': 2,
                'organochlorine': 2,
                'natural': 2,
                'concentration': 2,
                'sea': 1,
                'influence': 1,
                'heavy': 1,
                'metal': 1,
                'wastewater': 1,
                'processing': 1,
                'compound': 1,
                'plant': 1,
                'correlation': 1
        })}

        self.assertEqual(get_decades_words_info(test_feed), test_ans)
