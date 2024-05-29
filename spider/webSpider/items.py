# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EmployItem(scrapy.Item):
    company = scrapy.Field()
    salary = scrapy.Field()
    city = scrapy.Field()
    education = scrapy.Field()
    job = scrapy.Field()
    details = scrapy.Field()