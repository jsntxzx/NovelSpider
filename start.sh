#!/bin/bash
mysql --user=root --password=root -e "source db.sql"

mkdir -pv run/biquge
nohup scrapy crawl biqugecrawler -s JOBDIR=run/biqugei >/dev/null 2>&1 &
