from selenium import webdriver

def driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-extensions')
    options.add_argument("-incognito")
    options.add_argument("--disable-popup-blocking")

    return webdriver.Chrome(chrome_options=options)