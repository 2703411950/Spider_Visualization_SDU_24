# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
import codecs
import csv


# 保存到CSV文件中
class CsvPipeline(object):

    def __init__(self):
        self.file = codecs.open('data.csv', 'w', encoding='utf_8_sig')

    def process_item(self, item, spider):
        fieldnames = ['company', 'salary', 'city', 'education', 'job', 'details']
        w = csv.DictWriter(self.file, fieldnames=fieldnames)
        w.writerow(item)
        return item

    def close_spider(self, spider):
        self.file.close()
