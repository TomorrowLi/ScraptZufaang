# -*- coding: utf-8 -*-
import scrapy
from ..items import ZufangScrapyItem
class ZufangSpider(scrapy.Spider):
    name = 'zufang'
    city_url='http://zu.sh.fang.com/cities.aspx'
    def start_requests(self):
        yield scrapy.Request(self.city_url,callback=self.get_city)
    def city_parse(self, response):
        zufang = response.xpath('//div[@class="houseList"]')
        for fangzi in zufang:
            title=fangzi.xpath('//p[@class="title"]/a/text()').extract()
            area =fangzi.xpath('//p[@class="gray6 mt20"]/a[1]/span[1]/text()').extract()
            rent_style = fangzi.xpath('//p[@class="font16 mt20 bold"]/text()[1]').extract()
            house_type= fangzi.xpath('//p[@class="font16 mt20 bold"]/text()[2]').extract()
            house_area = fangzi.xpath('//p[@class="font16 mt20 bold"]/text()[3]').extract()
            if fangzi.xpath('//p[@class="font16 mt20 bold"]/text()[4]'):
                orientation = fangzi.xpath('//p[@class="font16 mt20 bold"]/text()[4]').extract()
            else:
                orientation=''
            price = fangzi.xpath('//p[@class="mt5 alingC"]/span/text()').extract()
            for i in range(len(title)):
                item = ZufangScrapyItem()
                item['title']=title[i]
                item['area']=area[i]
                item['rent_style']=rent_style[i].strip()
                item['house_type']=house_type[i]
                item['house_area']=house_area[i]
                item['orientation']=orientation[i].strip()
                item['price']=price[i]
                yield item
    def get_city(self,response):
        url=response.xpath('/html/body/div[3]/div[1]/a/@href').extract()
        for i in url:
            product={
                'city':i
            }
            yield scrapy.Request(product['city'],callback=self.city_parse, dont_filter=True)
            for j in range(2,10):
                next_url=product['city']+'house/i3%s'%j
                yield scrapy.Request(next_url,callback=self.city_parse,dont_filter=True)

