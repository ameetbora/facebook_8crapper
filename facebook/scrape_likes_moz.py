import sys
import time
import random
from likers import steps
from likers import save
from likers import setup
from facebook import db

page_name = sys.argv[1]
page_id = sys.argv[2]

if page_id is None or page_name is None:
    raise ValueError("No page id or page name provided. Sort yourself out m8.")

user_email = "hontyfonty@yandex.com"
user_password = "HY67ccc881"

likers_url = "https://m.facebook.com/search/260823190756616/likers".format(page_id)

driver = setup.driver_moz()

steps.login(driver, user_email, user_password)

driver.get(likers_url)

database = db.db()
supplier_id = database.save_supplier(page_name, page_id)

while True:
    try:
        likers = steps.get_likers(driver)
        for liker in likers:
            database.save_like(liker, supplier_id)
    except Exception as e:
        print(e)
        database.rollback()
        continue
        
    warning = steps.get_facebook_warning(driver)
    if warning:
        print("Looks like they're onto us. Time to stop.")
        break

    success = steps.get_next_likers(driver)
    if not success:
        print("looks like we reached the end")
        break

    time.sleep(1)

print("Hell yeah")

