import time

def login(driver, user_email: str, user_password: str):
    driver.get("https://www.facebook.com")
    
    email = driver.find_element_by_id("email")
    password = driver.find_element_by_id("pass")
    submit = driver.find_element_by_id("loginbutton")

    email.send_keys(user_email)
    password.send_keys(user_password)
    submit.click()

def keep_scrolling(driver, times: int = 99999999999):
    while times > 0:
        times -= 1
        results_end_notifiers = driver.find_elements_by_xpath("//div[text()='End of results']")
        if len(results_end_notifiers) > 0:
            print("Looks like we found all the likers.")
            return True

        else:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight + 1000);")
            time.sleep(3)

def get_likers(driver):
    likers = []
    links = [link.get_attribute("href") for link in driver.find_elements_by_xpath("//table[@role='presentation']//tr//td[position()=2]//a[not(@class)]")]
    names = [name.text for name in driver.find_elements_by_xpath("//table[@role='presentation']//tr//td[position()=2]//a[not(@class)]/div/div")]

    if len(names) > 0 and len(names) == len(links):
        for i in range(len(links)):
            likers.append({
                "name": names[i],
                "link": links[i],
            })
    else:
        print("The names And links didn't match, something is wrong with our xpathing.")
    
    return likers

def get_next_likers(driver):
    next_page_link = driver.find_elements_by_xpath("//div[@id='see_more_pager']/a")

    if len(next_page_link) > 0:
        next_page_link[0].click()
        return True

    return False


def get_facebook_warning(driver):
    warning = driver.find_elements_by_xpath("//div[contains(text(), 'It looks like you’re using this feature in a way it wasn’t meant to be used.')]")

    return len(warning) > 0