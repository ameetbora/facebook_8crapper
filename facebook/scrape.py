import sys
import scrapy
import time
from scrapy import spiderloader
from scrapy.utils import project
from scrapy.crawler import CrawlerProcess
from facebook import db
from facebook.help import cookies, url

settings = project.get_project_settings()
spider_loader = spiderloader.SpiderLoader.from_settings(settings)
comment_spider = spider_loader.load("comments")

user_id = 100029134355964
page_name = sys.argv[1]
page_id = sys.argv[2]

database = db.db()
supplier_id = database.save_supplier(page_name, page_id)

cookies = cookies.get_facebook_cookie("sallymuntzy@outlook.com", "r34hge%V&BF3ghf")
base_url = url.page_url(page_id, user_id)

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(comment_spider, base_url, cookies, supplier_id)
process.start()