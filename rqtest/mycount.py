import requests
def get_100():
    print 'im in in '
    return 100
def count_words_at_url(url):
    print 'im in'
    resp = requests.get(url)
    return len(resp.text.split())

