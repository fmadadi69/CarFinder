import re

from django.core.management.base import BaseCommand
from django.utils import timezone

from CarRecomender.models import Car, ScrapingReport
import time as t
import datetime
import khayyam

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def clean_mileage(mileage):
    cleaned = re.sub(r'\b(کیلومتر|کارکرد|km)\b', '', mileage)
    cleaned = re.sub(r'\bصفر\b', '0', cleaned)
    cleaned = re.sub(r'\bکارکرده\b', '300000', cleaned)
    cleaned = re.sub(r',', '', cleaned)
    return cleaned.strip()


def detect_and_convert_year(year):
    solar_date = khayyam.JalaliDatetime.now()
    solar_year = solar_date.year
    threshold_year = 1500
    if int(year) >= threshold_year:
        converted_year = khayyam.JalaliDatetime(datetime.datetime(int(year), 1, 1))
        return converted_year.year
    else:
        return year


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

    card_content = browser.find_elements(By.XPATH, "//a[contains(@class, 'bama-ad')]")
    # print(f'Number of carcontent is :{len(card_content)}')
    for car in card_content:

        make = car.find_element(By.XPATH, ".//p[contains(@class, 'bama-ad__title')]")
        cars_info_dict['make'] = make.text

        # time = car.find_element(By.XPATH, ".//div[contains(@class , 'bama-ad__title-row')]")
        # cars_info_dict['time'] = time.text.split('\n')[1]

        year = car.find_element(By.XPATH, ".//div[contains(@class , 'bama-ad__detail-row')]")
        cars_info_dict['year'] = detect_and_convert_year(year.text.split('\n')[0])

        mileage = car.find_element(By.XPATH, ".//div[contains(@class , 'bama-ad__detail-row')]")
        cars_info_dict['mileage'] = clean_mileage(mileage.text.split('\n')[1])

        condition = car.find_element(By.XPATH, ".//div[contains(@class , 'bama-ad__detail-row')]")
        cars_info_dict['condition'] = condition.text.split('\n')[2]

        location = car.find_element(By.XPATH, ".//div[contains(@class , 'bama-ad__address')]")
        city_pattern = re.compile(r"^\w+(?: \w+)?")
        match = city_pattern.search(location.text)
        if match:
            city = match.group(0)
        else:
            city = location.text
        cars_info_dict['location'] = city

        price = car.find_element(By.XPATH, ".//div[contains(@class , 'bama-ad__price-holder')]")
        cars_info_dict['price'] = re.sub(r',', '', price.text).strip()

        # print(cars_info_dict)
        if str(cars_info_dict) != str(last_retrieved_item):
            cars_info_list.append(dict(cars_info_dict))
        elif str(cars_info_dict) == str(last_retrieved_item):
            break

    return cars_info_list


if ScrapingReport.objects.count() == 0:
    last_car = {'make': 'پورشه، کاین',
                'year': '2013',
                'mileage': '72,000 کیلومتر',
                'condition': '6 سیلندر',
                'location': 'تهران / شهرک غرب',
                'price': '9,000,000,000'}
elif ScrapingReport.objects.count() > 0:
    last_car = ScrapingReport.objects.order_by("-report_date")[0].last_retrieve_car


# last_car_obj = Cars.objects.get(pk=latest_report.last_retrieve_car)


class Command(BaseCommand):
    help = 'Insert a list of cars into the database'

    def handle(self, *args, **kwargs):
        cars_list = get_data(100, last_car)
        if len(cars_list) != 0:
            for car in cars_list:
                Car.objects.create(**car)
            ScrapingReport.objects.create(report_date=timezone.now(), counts=len(cars_list),
                                          last_retrieve_car=cars_list[0])
            self.stdout.write(self.style.SUCCESS('Successfully inserted cars into database.'))
        else:
            return 'There is no new Car info'
