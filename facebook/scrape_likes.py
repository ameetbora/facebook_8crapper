import sys
import time
from likers import steps
from likers import save
from likers import setup

page_name = sys.argv[1]
page_id = sys.argv[2]

if page_id is None or page_name is None:
    raise ValueError("No page id or page name provided. Sort yourself out m8.")

user_email = "sallymuntzy@outlook.com"
user_password = "r34hge%V&BF3ghf"

likers_url = "https://m.facebook.com/search/{}/likers".format(page_id)

driver = setup.driver()

steps.login(driver, user_email, user_password)

driver.get(likers_url)

steps.keep_scrolling(driver, 100)

save.save_likers(driver.page_source, page_name, page_id)

print("Hell yeah")

