from selenium import webdriver

def get_facebook_cookie(user_email: str, user_password: str) -> dict:
    driver = webdriver.Chrome("/usr/local/bin/chromedriver")
    driver.get("https://www.facebook.com")
    
    email = driver.find_element_by_id("email")
    password = driver.find_element_by_id("pass")
    submit = driver.find_element_by_id("loginbutton")

    email.send_keys(user_email)
    password.send_keys(user_password)
    submit.click()

    cookies = {}
    for cookie in driver.get_cookies():
        cookies[cookie["name"]] = cookie["value"]
    
    return cookies