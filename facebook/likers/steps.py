import time

def login(driver, user_email: str, user_password: str):
    driver.get("https://www.facebook.com")
    
    email = driver.find_element_by_id("email")
    password = driver.find_element_by_id("pass")
    submit = driver.find_element_by_id("loginbutton")

    email.send_keys(user_email)
    password.send_keys(user_password)
    submit.click()

def keep_scrolling(driver):
    results_end_notifiers = driver.find_elements_by_xpath("//div[text()='End of results']")
    if len(results_end_notifiers) > 0:
        print("Looks like we found all the likers.")
        return True

    else:
        loading_boxes = driver.find_elements_by_xpath("//span[text()='Loading more results...']")
        if len(loading_boxes) > 0:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight + 1000);")
            time.sleep(1)
            keep_scrolling(driver)

        else:
            print("We couldn't find the end results notifier or the loading box. Something probably went wrong. Maybe the Zucc is onto us.")
            return False