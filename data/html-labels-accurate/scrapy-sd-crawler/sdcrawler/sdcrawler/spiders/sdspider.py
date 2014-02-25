from scrapy.spider import Spider
import time
from pyquery import PyQuery
import codecs

SLEEP_BETWEEN_REQUEST = 0

def ReadURL(url):
  trytime = 0
  pq = None
  while (trytime < 3):
    try:
      pq = PyQuery(url = url)
      break
    except Exception as e:
      print 'Exception!', url
      trytime += 1
      raise e
      time.sleep(SLEEP_BETWEEN_REQUEST)
  if pq == None or pq.html() == None:
    return ''
  return pq.html()
  # return pq.text()


class SDSpider(Spider):
  name = "sciencedirect"
  CRAWL_MAX = 1
  allowed_domains = ["sciencedirect.com"]
  start_urls = []
  urlname_jid = {}

  def __init__(self):
    print 'Reading URLs...'
    lines = [l.strip().split('\t') for l in open('urls.txt').readlines()]
    
    for l in lines[ : SDSpider.CRAWL_MAX]:
      urlname = l[1].split("/")[-2]
      # print l[0], urlname
      SDSpider.urlname_jid[urlname] = l[0]
      SDSpider.start_urls.append(l[1])

    print 'Done reading URLs. #URLs:', len(SDSpider.start_urls)

  def parse(self, response):
    urlname = response.url.split("/")[-2]
    filename = SDSpider.urlname_jid[urlname]
    for line in response.body.split('\n'):
      if line.startswith('SDM.pm.fat'):
        fragbase = line.strip(';')[len('SDM.pm.fat') : ].strip(' =\'')
        urlbase = 'http://www.sciencedirect.com/science/frag/'+urlname+'/' + fragbase + '/frag_'

        fragid = 0
        tothtml = ''
        while True:
          # print '................Sleeping................'
          time.sleep(SLEEP_BETWEEN_REQUEST)
          fragid += 1
          url = urlbase + str(fragid)

          html = ReadURL(url)

          if html == '' or 'Fragment not found' in html or fragid > 100:
            break

          tothtml += html
          

        # open(filename, 'wb').write(tothtml)
        fout = codecs.open(filename+'.html', "w", "utf-8")
        fout.write(tothtml)
        fout.close()
