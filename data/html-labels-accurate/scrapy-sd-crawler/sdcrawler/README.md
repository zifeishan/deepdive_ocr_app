SDCrawler
====

This package is used to crawl 30k Paleo PDFs from www.sciencedirect.com.

The URLs to crawl is listed in urls.txt

Execute:

    $ bash run.sh

or:

    $ scrapy crawl sciencedirect

Output will be put in root directory as `JOURNAL_[JID].html`.



How to get page fragments
====

You can easily implement it without scrapy.

Say we are crawling the follow url:

    http://www.sciencedirect.com/science/article/pii/S0195667105001114/

Denote `urlname = 'S0195667105001114'`.

There is a line of code in sciencedirect pages that looks like this:

    SDM.pm.fat = '37900f54e69ae5958a57ba4c45b2df994a24e3212619979317a1b817b850a830797663bcca49b06fe821d4e3bd4f98b6bb97e7b5385c50cb78a6225a3d27530c0cc56612944497703e70a0a042d86e1972d995d611722ab9c7dae6e993e961ffbb2c9582a32d1134cc49f2dd12cdbdcd3ed8329c5edf92a3b7f18ce140a85288b22f9ffe2ad050d0201c69127c29e139cae21038f6d86ef32937727e62c3b877e9c82a608d13766521a09451574c21f1';

Denote `fragbase = '37900f54e69...'`. 

If we attach this string to the URL base: 'http://www.sciencedirect.com/science/frag/' + `urlname` + '/' + `fragbase` + '/frag_' + `fragID`, where  `fragID` is 1, 2, 3..., until the URL returns an empty page, we get URLs representing all document fragments we need to crawl.

e.g. a fragment URL looks like:

    www.sciencedirect.com/science/frag/S0195667105001114/37900f54e69ae5958a57ba4c45b2df994a24e3212619979317a1b817b850a830797663bcca49b06fe821d4e3bd4f98b6bb97e7b5385c50cb78a6225a3d27530c0cc56612944497703e70a0a042d86e1972d995d611722ab9c7dae6e993e961ffbb2c9582a32d1134cc49f2dd12cdbdcd3ed8329c5edf92a3b7f18ce140a85288b22f9ffe2ad050d0201c69127c29e139cae21038f6d86ef32937727e62c3b877e9c82a608d13766521a09451574c21f1/frag_1


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


