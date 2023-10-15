from django.contrib import admin

# Register your models here.
from .models import ScrapingReport, Cars
import re
import time as t
import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def get_data(pages, last_retrieved_item):
    browser = webdriver.Chrome()
    # browser = webdriver.Firefox()

    cars_info_list = []
    cars_info_dict = dict()
    browser.get(f"https://bama.ir/car?priced=1")

    body = browser.find_element(By.TAG_NAME, 'body')

    no_pages = pages
    while no_pages:
        body.send_keys(Keys.END)
        t.sleep(0.5)
        no_pages -= 1

    card_content = browser.find_elements(By.XPATH, "//a[@class = 'bama-ad']")
    for car in card_content:

        make = car.find_element(By.XPATH, ".//p[contains(@class, 'bama-ad__title')]")
        cars_info_dict['make'] = make.text
        # print(title.text)

        time = car.find_element(By.XPATH, ".//div[@class = 'bama-ad__title-row']")
        cars_info_dict['time'] = time.text.split('\n')[1]

        year = car.find_element(By.XPATH, ".//div[@class = 'bama-ad__detail-row']")
        cars_info_dict['year'] = year.text.split('\n')[0]

        mileage = car.find_element(By.XPATH, ".//div[@class = 'bama-ad__detail-row']")
        cars_info_dict['mileage'] = mileage.text.split('\n')[1]

        condition = car.find_element(By.XPATH, ".//div[@class = 'bama-ad__detail-row']")
        cars_info_dict['condition'] = condition.text.split('\n')[2]

        location = car.find_element(By.XPATH, ".//div[@class = 'bama-ad__address']")
        cars_info_dict['location'] = location.text

        price = car.find_element(By.XPATH, ".//div[@class = 'bama-ad__price-holder']")
        cars_info_dict['price'] = price.text

        # print(cars_info_dict)
        # print("///////////////////////////////////////////////////////////////////")
        if cars_info_dict != last_retrieved_item:
            cars_info_list.append(dict(cars_info_dict))
        else:
            break
        # print(len(cars_info_list))

    return cars_info_list, len(cars_info_list)


last_item = {'make': 'پورشه، کاین',
             'time': 'لحظاتی پیش',
             'year': '2013',
             'mileage': '72,000 کیلومتر',
             'condition': '6 سیلندر',
             'location': 'تهران / شهرک غرب',
             'price': '9,000,000,000'}


# print(get_data(100, last_item))


class ScrapingReportAdmin(admin.ModelAdmin):
    actions = [get_data(100, last_item)]
    model = ScrapingReport


admin.site.register(ScrapingReport, ScrapingReportAdmin)
