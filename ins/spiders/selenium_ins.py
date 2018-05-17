from time import sleep
import math,jsonpickle
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from ..settings import IMAGES_STORE

chrome_options = Options()
chrome_options.add_argument('--dns-prefetch-disable')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--lang=en-US')
chrome_options.add_argument('--headless')
chrome_options.add_experimental_option('prefs', {'intl.accept_languages': 'en-US'})
browser = webdriver.Chrome('./assets/chromedriver', chrome_options=chrome_options)

# SETTINGS:
# set limit of posts to analyze:
limit_amount = 12000

# makes sure slower connections work as well
print("Waiting 10 sec")
browser.implicitly_wait(10)
limit_amount = 12000

def extract_information(username,browser=browser, limit_amount=limit_amount):
    browser.get('https://www.instagram.com/' + username)
    try:
        body_elem = browser.find_element_by_tag_name('body')
        container = browser.find_element_by_class_name('_mesn5')
        infos = container.find_elements_by_class_name('_t98z6')
        num_of_posts = int(infos[0].text.split(' ')[0].replace(',', ''))
        num_of_posts = min(limit_amount, num_of_posts)
        # load_button = body_elem.find_element_by_xpath\
        #  ('//a[contains(@class, "_1cr2e _epyes")]')
        # body_elem.send_keys(Keys.END)
        # sleep(3)

        # load_button.click()

        links = []
        links2 = []

        # list links contains 30 links from the current view, as that is the maximum Instagram is showing at one time
        # list links2 contains all the links collected so far

        previouslen = 0
        breaking = 0

        print("Getting only first", 12 * math.ceil(num_of_posts / 12),
              "posts only, if you want to change this limit, change limit_amount value in crawl_profile.py\n")
        while (len(links2) < num_of_posts):

            prev_divs = browser.find_elements_by_tag_name('main')
            links_elems = [div.find_elements_by_tag_name('a') for div in prev_divs]
            links = sum([[link_elem.get_attribute('href')
                          for link_elem in elems] for elems in links_elems], [])
            for link in links:
                if "/p/" in link:
                    links2.append(link)
            links2 = list(set(links2))
            print("Scrolling profile ", len(links2), "/", 12 * math.ceil(num_of_posts / 12))
            body_elem.send_keys(Keys.END)
            sleep(1.5)

            ##remove bellow part to never break the scrolling script before reaching the num_of_posts
            if (len(links2) == previouslen):
                breaking += 1
                print("breaking in ", 4 - breaking,
                      "...\nIf you believe this is only caused by slow internet, increase sleep time in line 149 in extractor.py")
            else:
                breaking = 0
            if breaking > 3:
                print("\nNot getting any more posts, ending scrolling.")
                sleep(2)
                break
            previouslen = len(links2)
            ##

    except NoSuchElementException as err:
        print('- Something went terribly wrong\n')

    count = 1
    with open(IMAGES_STORE.split('/')[-1], 'w')as fw:
        for link in links2:
            print("parse ", count, "/", 12 * math.ceil(num_of_posts / 12))
            print("\nScrapping link: ", link)
            fw.write(link+'\n')
            yield link
            count += 1



extract_information(browser,'dorosiwa',limit_amount)