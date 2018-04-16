# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import urllib.error
import pymongo
class ZufangScrapyPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(host="127.0.0.1",user="root",passwd="",db="zufang",charset="utf8")
        self.cur = self.conn.cursor()

    def process_item(self, item, spider):
          try:
              title = item['title']
              area = item['area']
              rent_style = item['rent_style']
              house_type = item['house_type']
              house_area = item['house_area']
              orientation = item['orientation']
              price = item['price']
              self.cur.execute("INSERT INTO zufang(title,area,rent_style,house_type,house_area,orientation,price) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                        (title,area,rent_style,house_type,house_area,orientation,price))
              self.conn.commit()
          except Exception as e:
              pass
          return item

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()
class MongoPipeline(object):

    collection_name = 'scrapy_items'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(dict(item))
        return item