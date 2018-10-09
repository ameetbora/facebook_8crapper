import sys
import comment
from help import cookies, url
import scrapy
from scrapy import CrawlerRunner

user_id = 100029134355964
page_name = sys.argv[1]
page_id = sys.argv[2]

database = db.db()
supplier_id = database.save_supplier(page_name, page_id)
database.commit()

cookies = cookies.get_facebook_cookie("sallymuntzy@outlook.com", "r34hge%V&BF3ghf")
base_url = url.page_url(page_id, user_id)

runner = CrawlerRunner()
runner.crawl("comments", base_url, cookies, supplier_id)

