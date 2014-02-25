# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


# import json

# class JsonWriterPipeline(object):

#     def __init__(self):
#         self.file = open('items.jl', 'wb')

#     def process_item(self, item, spider):
#         line = json.dumps(dict(item)) + "\n"
#         self.file.write(line)
#         return item

        
from scrapy.exceptions import DropItem

class SDPipeline(object):
  def process_item(self, item, spider):
    return item

  # vat_factor = 1.15

  # def process_item(self, item, spider):
  #   if item['price']:
  #     if item['price_excludes_vat']:
  #       item['price'] = item['price'] * self.vat_factor
  #     return item
  #   else:
  #     raise DropItem("Missing price in %s" % item)