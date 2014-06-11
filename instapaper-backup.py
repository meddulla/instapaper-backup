from readability.readability import Document
import urllib
import csv
import os
import feedparser

FILENAME = 'instapaper-export.csv'
SAVE_DIR = 'articles/'
RSS_URL = 'https://www.instapaper.com/rss/128118/kyinK0o0llflyQS05qeC1RzZ5E'


def clean(s):
   return "".join([c for c in s if c.isalpha() or c.isdigit() or c == ' ']).rstrip()


def parse_rss():
    urls_list = []
    d = feedparser.parse(RSS_URL)
    for post in d.entries:
        p = {'Title': post.title, 'URL': post.link, 'Folder': 'Unread'}
        yield p


def get_article(url):
    try:
        html = urllib.urlopen(url).read()
        if html:
            readable_article = Document(html).summary().encode('utf-8', 'ignore')
            readable_title = Document(html).short_title().encode('utf-8', 'ignore')
            return readable_title, readable_article
    except EOFError:
        print 'Error fetching %s: %s' % (url, EOFError)
    except Exception as e:
        print 'Error fetching %s: %s' % (url, e)
    return None, None


def urls():
    with open(FILENAME) as file_obj:
        reader = csv.DictReader(file_obj, delimiter=',')
        for line in reader:
            yield line


def process_all(fn):
    for r in fn():
        title, body = get_article(r['URL'])
        if not title or not body:
            continue
        safe_title = clean(title)
        directory = SAVE_DIR
        if r['Folder'] != 'Unread':
            directory = '{dir}/{sub}'.format(dir=SAVE_DIR, sub=clean(r['Folder']))
            # create dir if not exists
            if not os.path.exists(directory):
                os.makedirs(directory)

        # only save if article is not saved yet
        filepath = '{dir}/{title}.html'.format(dir=directory, title=safe_title)
        if not os.path.isfile(filepath):
            with open(filepath, 'w') as article:
                print 'saving article %s' % title
                article.write(body)
        else:
            print 'skipping %s' % title


def start(rss=True):
    process_all(parse_rss if rss else urls)


if __name__ == "__main__":
    start(rss=True)
    print 'done!'

