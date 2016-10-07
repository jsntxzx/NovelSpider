# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NovelItem(scrapy.Item):
	novel_name = scrapy.Field()
	novel_author = scrapy.Field()
	last_update = scrapy.Field()
	novel_image = scrapy.Field()
	novel_abstract = scrapy.Field()
	novel_status = scrapy.Field()
	novel_category = scrapy.Field()
	novel_booknum = scrapy.Field()


class ChapterItem(scrapy.Item):
	chapter_booknum = scrapy.Field()
	chapter_name = scrapy.Field()
	chapter_order = scrapy.Field()
	chapter_content = scrapy.Field()
