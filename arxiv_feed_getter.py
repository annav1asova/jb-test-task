import urllib.request
import feedparser

base_url = 'http://export.arxiv.org/api/query?'
extra_url = 'search_query=all:%s&start=%i&max_results=%i'

start = 0
max_results = 1000

quote_code = '%22'
space_code = '+'

feedparser._FeedParserMixin.namespaces['http://a9.com/-/spec/opensearch/1.1/'] = 'opensearch'
feedparser._FeedParserMixin.namespaces['http://arxiv.org/schemas/atom'] = 'arxiv'


def prepare_query(search_request):
    search_request = search_request.replace(' ', space_code).replace('"', quote_code)

    # print(search_request)
    query = extra_url % (search_request, start, max_results)
    return query


def get_feed(search_request):
    query = prepare_query(search_request)
    response = urllib.request.urlopen(base_url + query).read()
    feed = feedparser.parse(response)
    return feed
