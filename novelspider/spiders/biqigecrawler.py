# -*- coding: utf-8 -*-
import scrapy
from novelspider.items import NovelItem, ChapterItem


class BiqugecrawlerSpider(scrapy.Spider):
	name = "biqugecrawler"
	allowed_domains = ["biquge.la"]
	base = "http://www.biquge.la"
	start_urls = (
		'http://www.biquge.la/xiaoshuodaquan/',
	)

	def parse(self, response):
		for data in response.css("div.novellist > ul > li"):
			url = data.css("a::attr(href)").extract_first()
			if url is not None:
				is_done = 0
				if "完" in data.css("text").extract():
					is_done = 1
				r = scrapy.Request(url=self.base+url, callback=self.parse_novel)
				r.meta['is_done'] = is_done
				r.meta['number'] = int(url.split('/')[-2])
				yield r


	def parse_novel(self, response):
		status_data = response.meta['is_done']
		book_num = response.meta['number']
		n = NovelItem()
		n['novel_name'] = response.css("div#info > h1::text").extract_first()
		n['novel_author'] = response.css("#info > p:nth-child(2)::text").extract_first().strip(u'\u4f5c\xa0\xa0\xa0\xa0\u8005\uff1a')
		n['last_update'] = response.css("#info > p:nth-child(4)::text").extract_first().strip(u'\u6700\u540e\u66f4\u65b0\uff1a')
		n['novel_image'] = response.css("div#fmimg > img::attr(src)").extract_first()
		n['novel_abstract'] = '\n'.join(response.css("div#intro > p::text").extract()[:-1])
		n['novel_status'] = status_data
		n['novel_category'] = response.css("div.con_top::text").extract()[2].split('>')[1].strip(' ')
		n['novel_booknum'] = book_num
		yield n
		for i, chapter in enumerate(response.css("div#list > dl > dd")):
			url = chapter.css("a::attr(href)").extract_first()
			if url is not None:
				r = scrapy.Request(url=response.url+url, callback=self.parse_chapter, priority=1)
				r.meta['chapter_order'] = i
				r.meta['chapter_booknum'] = book_num
				yield r


	def parse_chapter(self, response):
		chapter_order = response.meta['chapter_order']
		chapter_booknum = response.meta['chapter_booknum']
		c = ChapterItem()
		c['chapter_name'] = response.css("div.bookname > h1::text").extract_first()
		c['chapter_content'] = response.css("#content").extract_first()\
					.strip(u'<div id="content"><script>readx();</script>\xa0\xa0\xa0\xa0')\
					.strip(u'</div>')
		c['chapter_order'] = chapter_order
		c['chapter_booknum'] = chapter_booknum
		yield c

