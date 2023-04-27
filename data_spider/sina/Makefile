# Description: Makefile for sina_spider

test:
	scrapy crawl sina_spider --nolog

debug:
	scrapy crawl sina_spider

save:
	scrapy crawl sina_spider -O news.json
	scrapy crawl film_spider -O film.json