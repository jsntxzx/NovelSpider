# -*- coding: utf-8 -*-

from datetime import datetime
from hashlib import md5
from scrapy import log
from scrapy.exceptions import DropItem
from twisted.enterprise import adbapi
from items import NovelItem, ChapterItem

class RequiredFieldsPipeline(object):
	"""A pipeline to ensure the item have the required fields."""

	def process_item(self, item, spider):
		if isinstance(item, NovelItem):
			required_fields = ('novel_name', 'novel_author', 'novel_category')
			for field in required_fields:
				if not item.get(field):
					raise DropItem("Field '%s' missing: %r" % (field, item))
			return item
		if isinstance(item, ChapterItem):
			required_fields = ('chapter_name', 'chapter_content')
			for field in required_fields:
				if not item.get(field):
					raise DropItem("Field '%s' missing: %r" % (field, item))
			return item


class MySQLStorePipeline(object):
	"""A pipeline to store the item in a MySQL database.
	This implementation uses Twisted's asynchronous database API.
	"""

	def __init__(self, dbpool):
		self.dbpool = dbpool

	@classmethod
	def from_settings(cls, settings):
		dbargs = dict(
			host=settings['MYSQL_HOST'],
			db=settings['MYSQL_DBNAME'],
			user=settings['MYSQL_USER'],
			passwd=settings['MYSQL_PASSWD'],
			charset='utf8',
			use_unicode=True,
		)
		dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
		return cls(dbpool)

	def process_item(self, item, spider):
		# run db query in the thread pool
		d = self.dbpool.runInteraction(self._do_upsert, item, spider)
		d.addErrback(self._handle_error, item, spider)
		# at the end return the item in case of success or failure
		d.addBoth(lambda _: item)
		# return the deferred instead the item. This makes the engine to
		# process next item (according to CONCURRENT_ITEMS setting) after this
		# operation (deferred) has finished.
		return d

	def _do_upsert(self, conn, item, spider):
		"""Perform an insert ."""
		if isinstance(item, NovelItem):
			conn.execute("""
				INSERT INTO novel_info (novel_name, novel_author,novel_category, novel_image, last_update, novel_abstract, novel_status, novel_booknum)
				VALUES (%s, %s, %s, %s, %s, %s, %s, %s)	""", (item['novel_name'], item['novel_author'], item['novel_category'] \
				, item['novel_image'], item['last_update'], item['novel_abstract'], item['novel_status'], item['novel_booknum']))
			spider.log("Item stored in db: %s" % item['novel_name'] )
		if isinstance(item, ChapterItem):
			conn.execute("""
				INSERT INTO chapter_info (chapter_name, chapter_booknum,chapter_order, chapter_content)
				VALUES (%s, %s, %s, %s)	""", (item['chapter_name'], item['chapter_booknum'], item['chapter_order'] , item['chapter_content']))
			spider.log("Item stored in db: %s" % item['chapter_name'] )


	def _handle_error(self, failure, item, spider):
		"""Handle occurred on db interaction."""
		# do nothing, just log
		log.err(failure)