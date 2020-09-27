# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Job2Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    movie_title = scrapy.Field()
    movie_types = scrapy.Field()
    movie_date = scrapy.Field()
