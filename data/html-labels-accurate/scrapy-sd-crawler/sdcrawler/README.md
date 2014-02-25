SDCrawler
====

This package is used to crawl 30k Paleo PDFs from www.sciencedirect.com.

The URLs to crawl is listed in urls.txt

Execute:

    $ bash run.sh

or:

    $ scrapy crawl sciencedirect

Output will be put in root directory as `JOURNAL_[JID].html`.


Parameter
====

Modify `spiders/sdspider.py` for waiting between requests (for 1 spider):

    SLEEP_BETWEEN_REQUEST = 0

Change `0` to `10` to let the spider wait 10 seconds between two
continuous crawls. This DO NOT guarantee waiting time since there might
be multiple threads crawling together (launched by Scrapy).


Dependencies
====

- scrapy: `$ pip install scrapy`
- pyquery: `$ pip install pyquery`


