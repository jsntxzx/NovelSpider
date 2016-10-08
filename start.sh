#!/bin/bash
mysql --user=root --password=root -e "source db.sql"

scrapy crawl biqugecrawler -s JOBDIR=run/biquge
