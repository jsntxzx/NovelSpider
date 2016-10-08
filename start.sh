#!/bin/bash
mysql --user=root --password=root -e "source db.sql"

mkdir -pv run/biquge
scrapy crawl biqugecrawler -s JOBDIR=run/biquge
