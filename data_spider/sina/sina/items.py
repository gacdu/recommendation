# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SinaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    news_number = scrapy.Field()
    news_title = scrapy.Field()
    news_desc = scrapy.Field()
    news_time = scrapy.Field()
    news_type = scrapy.Field()
    news_url = scrapy.Field()
