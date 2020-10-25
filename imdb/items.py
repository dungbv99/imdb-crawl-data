# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ImdbItem(scrapy.Item):
    storyLine = scrapy.Field()
    cast = scrapy.Field()
    averageRating = scrapy.Field()
    budget = scrapy.Field()
    cumulative = scrapy.Field()
    director = scrapy.Field()
    writer = scrapy.Field()
    stars = scrapy.Field()
    country = scrapy.Field()

