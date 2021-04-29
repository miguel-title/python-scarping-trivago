import selenium
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from bs4 import BeautifulSoup

from selenium.common.exceptions import TimeoutException
import datetime
import calendar
import requests
import random
import time
import csv
import sys
import os
from random import choice
import json
if sys.version_info >= (3, 0):
    import configparser as ConfigParser
else:
    import ConfigParser


input_header = [
    'city_name',
    'starting_period',
    'ending_period',
    'camera',
    'adulti',
    'bambini',
    'eta dei bambini1',
    'eta dei bambini2',
    'eta dei bambini3',
    'eta dei bambini4',
    'pricing',
    'sistemazione',
    'order'
]

order = {
    'Consigliati':'1',
    'Valutazione e consigliati':'7',
    'Prezzo e consigliati':'5',
    'Distanza e consigliati':'6',
    'Solo valutazione':'4',
    'Solo prezzo':'2',
    'Solo distanza':'3'
}

output_header = [
    'merchant',
    'scraping_date',
    'city_name',
    'hotel_name',
    'star',
    'Starting_period',
    'Ending_period',
    'Camera',
    'Price 1',
    'Price 2',
    'Price 3',
    'Price 4',
    'Price 5',
    'currency'
]

lst_price = {
    '50': 24,
    '55': 29,
    '60': 40,
    '65': 53,
    '70': 61,
    '75': 69,
    '80': 80,
    '85': 87,
    '90': 94,
    '95': 99,
    '100': 107,
    '110': 115,
    '120': 128,
    '130': 138,
    '140': 149,
    '150': 158,
    '160': 167,
    '170': 177,
    '180': 180,
    '190': 187,
    '200': 196,
    '210': 203,
    '220': 208,
    '230': 216,
    '240': 220,
    '250': 226,
    '260': 230,
    '270': 235,
    '280': 240,
    '290': 242,
    '300': 247,
    '310': 253,
    '320': 256,
    '330': 259,
    '340': 265,
    '350': 267,
    '360': 271,
    '370': 275,
    '380': 280,
    '390': 283,
    '400': 286,
    '410': 289,
    '420': 291,
    '430': 295,
    '440': 298,
    '450': 301,
    '460': 304,
    '470': 306,
    '480': 308,
    '490': 311,
    '500': 315
}

str_date = datetime.datetime.now().strftime('%Y-%m-%d')

def load_config():
    defaults = {
        'input_path': '',
        'out_path': '',
        'suffix_excelfile_name': ''
    }
    _settings_dir = "."
    config_file = os.path.join(_settings_dir, "config.ini")
    if os.path.exists(config_file):
        try:
            # config = ConfigParser.SafeConfigParser()
            config = ConfigParser.ConfigParser()
            config.read(config_file)
            if config.has_section("global"):
                config_items = dict(config.items("global"))
                defaults['input_path'] = config_items['input_path']
                defaults['out_path'] = config_items['out_path']
                defaults['suffix_excelfile_name'] = config_items['suffix_excelfile_name']
                defaults['out_path'] = '{}/{}_{}.csv'.format(defaults['out_path'], str_date, defaults['suffix_excelfile_name'])



        except ConfigParser.Error as e:
            print("\nError parsing config file: " + config_file)
            print(str(e))
            exit(1)

    return defaults

def time_sleep(type):
    if type == 1:
        sleeptime = random.randrange(10,100)/100
    elif type == 2:
        sleeptime = random.randrange(70, 200)/100
    elif type == 3:
        sleeptime = random.randrange(100, 300)/100
    elif type == 4:
        sleeptime = random.randrange(150, 400)/100
    elif type == 5:
        sleeptime = random.randrange(400, 500)/100
    elif type == 401:
        sleeptime = random.randrange(60, 100)
    time.sleep(sleeptime)

def random_headers():
    desktop_agents = [
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0']
    return {'User-Agent': choice(desktop_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}

def get_request(url,count=0):

    r = requests.get(url,headers=random_headers())
    time_sleep(2)
    if r.status_code == 200:
        return BeautifulSoup(r.content, 'html.parser')
    elif count < 5:
        print('error code: {}, url: {}'.format(r.status_code,url))
        print(' . . . time sleep . . .')
        time_sleep(401)
        count += 1
        return get_request(url, count)

    return BeautifulSoup(r.content, 'html.parser')

def get_seleniumdriver(url, count=0):
    options = Options()
    if os.name == "nt":
        #options.add_argument("--start-maximized")
        #options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        #options.add_argument("--disable-dev-shm-usage")
        #options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(options=options)
    else:
        #options.add_argument("--start-maximized")
        #options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        #options.add_argument("--disable-dev-shm-usage")
        #options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(chrome_options=options, executable_path='./chromedriver')
    driver.get(url)
    driver.implicitly_wait(10)
    time_sleep(1)

    return driver

def get_query(input_path):
    lst_query = []
    with open(input_path) as csv_file:
        records = csv.reader(csv_file, delimiter=';')
        for row in records:
            lst_query.append(row)
    return lst_query

def get_data(driver, query, writer):
    print("-query:{}".format(query))
    try:
        input_datein = datetime.datetime.strptime(query[1], "%d/%m/%Y").date()
        max_date = datetime.date(input_datein.year+1, input_datein.month, calendar.monthrange(input_datein.year+1, input_datein.month)[1])
        if input_datein < datetime.datetime.now().date():
            print("wrong query: " + "starting_period is low current date : " + query[1])
            return False
        elif input_datein > max_date:
            print("wrong query: " + "starting_period is low max date : " + query[1])
            return False

        input_dateout = datetime.datetime.strptime(query[2], "%d/%m/%Y").date()
        nyear = input_dateout.year
        nmonth = input_dateout.month + 2
        if input_dateout.month + 2 > 12:
            nyear += 1
            nmonth = nmonth - 12
        max_date = datetime.date(nyear, nmonth, calendar.monthrange(nyear, nmonth)[1])
        if input_dateout < input_datein:
            print("wrong query: " + "ending_period is low starting_period + 3month : " + query[2])
            return False
        elif input_dateout > max_date:
            print("wrong query: " + "ending_period is low max date : " + query[2])
            return False



        '''run query'''
        querytext = driver.find_element_by_id('querytext')
        driver.implicitly_wait(30)
        querytext.clear()
        querytext.send_keys(query[0])
        time_sleep(1)
        querytext.send_keys(Keys.ENTER)
        # select date-in

        btn_date_in = driver.find_element_by_class_name('calendar-button-wrapper--checkin')
        btn_date_in.click()
        btn_date_in.click()
        time_sleep(1)
        df_container_calendars = driver.find_elements_by_class_name('df_container_calendar')
        n_df = len(df_container_calendars)
        while (n_df == 0):
            btn_date_in.click()
            # btn_date_in.click()
            time_sleep(1)
            df_container_calendars = driver.find_elements_by_class_name('df_container_calendar')
            n_df = len(df_container_calendars)

        df_container_calendar = df_container_calendars[0]
        td_days = df_container_calendar.find_elements_by_class_name('cal-day-wrap')
        td_time = td_days[10].find_element_by_tag_name('time').get_attribute('datetime')
        td_time = datetime.datetime.strptime(td_time, "%Y-%m-%d")
        n_step = 0
        if td_time.month != input_datein.month or td_time.year != input_datein.year:
            if input_datein.year > td_time.year:
                n_step = input_datein.month + (12 - td_time.month)

            elif input_datein.year < td_time.year:
                n_step = 0 - td_time.month - (12 - input_datein.month)
            else:
                n_step = input_datein.month - td_time.month
        if n_step > 0:
            btn_next = df_container_calendar.find_element_by_class_name('cal-btn-next')
            for i in range(n_step):
                btn_next.click()
                time_sleep(1)
        elif n_step < 0:
            btn_prev = df_container_calendar.find_element_by_class_name('cal-btn-prev')
            n_step = abs(n_step)
            for i in range(n_step):
                btn_prev.click()
                time_sleep(1)

        td_days = df_container_calendar.find_elements_by_class_name('cal-day-wrap')
        for td_day in td_days:
            td_time = td_day.find_element_by_tag_name('time').get_attribute('datetime')
            td_time = datetime.datetime.strptime(td_time, "%Y-%m-%d").date()
            if td_time == input_datein:
                td_day.click()
                break
        time_sleep(1)


        btn_date_in = driver.find_element_by_class_name('calendar-button-wrapper--checkout')
        btn_date_in.click()
        time_sleep(1)
        btn_date_in.click()
        time_sleep(1)
        df_container_calendars = driver.find_elements_by_class_name('df_container_calendar')
        n_df = len(df_container_calendars)
        while (n_df == 0):
            btn_date_in.click()
            # btn_date_in.click()
            time_sleep(1)
            df_container_calendars = driver.find_elements_by_class_name('df_container_calendar')
            n_df = len(df_container_calendars)

        df_container_calendar = df_container_calendars[0]
        td_days = df_container_calendar.find_elements_by_class_name('cal-day-wrap')
        td_time = td_days[10].find_element_by_tag_name('time').get_attribute('datetime')
        td_time = datetime.datetime.strptime(td_time, "%Y-%m-%d")
        

        n_step = 0
        if td_time.month != input_dateout.month or td_time.year != input_dateout.year:
            if input_dateout.year > td_time.year:
                n_step = input_dateout.month + (12 - td_time.month)

            elif input_dateout.year < td_time.year:
                n_step = 0 - td_time.month - (12 - input_dateout.month)
            else:
                n_step = input_dateout.month - td_time.month


        if n_step > 0:
            btn_next = df_container_calendar.find_element_by_class_name('cal-btn-next')
            for i in range(n_step):
                btn_next.click()
                time_sleep(1)
        elif n_step < 0:
            btn_prev = df_container_calendar.find_element_by_class_name('cal-btn-prev')
            n_step = abs(n_step)
            for i in range(n_step):
                btn_prev.click()
                time_sleep(1)

        td_days = df_container_calendar.find_elements_by_class_name('cal-day-wrap')
        for td_day in td_days:
            td_time = td_day.find_element_by_tag_name('time').get_attribute('datetime')
            td_time = datetime.datetime.strptime(td_time, "%Y-%m-%d").date()
            if td_time == input_dateout:
                td_day.click()
                break
        time_sleep(1)

        """selecting camera"""
        btn_camera = driver.find_element_by_class_name('dealform-button--guests')
        btn_camera.click()
        btn_camera.click()
        time_sleep(1)
        df_overlays = driver.find_elements_by_class_name('df_overlay')

        n_df = len(df_overlays)
        while (n_df == 0):
            btn_camera.click()
            time_sleep(1)
            df_overlays = driver.find_elements_by_class_name('df_overlay')

            n_df = len(df_overlays)

        btn_roomtypes = df_overlays[0].find_elements_by_class_name('roomtype-btn')
        if 'camera singola'.lower() in query[3].lower():
            btn_roomtypes[0].click()
            time_sleep(1)
            btn_search = driver.find_element_by_class_name('search-button')
            btn_search.click()
        elif 'camera doppia'.lower() in query[3].lower():
            btn_roomtypes[1].click()
            time_sleep(1)
            btn_search = driver.find_element_by_class_name('search-button')
            btn_search.click()
        elif 'camere familiari'.lower() in query[3].lower():
            btn_roomtypes[2].click()
            time_sleep(1)
            if query[4]:
                dealform_extRooms = driver.find_element_by_id('dealform_extRooms')
                adultiitem = None
                try:
                    adultiitem = WebDriverWait(dealform_extRooms, 5).until(ec.visibility_of_element_located((By.ID, "select-num-adults-2")))
                except TimeoutException:
                    adultiitem = WebDriverWait(dealform_extRooms, 5).until(ec.visibility_of_element_located((By.ID, "select-num-adults-0")))


                select = Select(adultiitem)

                select.select_by_value(query[4])
                if query[5]:

                    childtem = None
                    try:
                        childtem = WebDriverWait(dealform_extRooms, 5).until(ec.visibility_of_element_located((By.ID, "select-num-children-2")))
                    except TimeoutException:
                        childtem = WebDriverWait(dealform_extRooms, 5).until(ec.visibility_of_element_located((By.ID, "select-num-children-0")))

                    select = Select(childtem)
                    select.select_by_value(query[5])
                    time_sleep(1)
                    select_ages = dealform_extRooms.find_elements_by_class_name('js-select-child-age')
                    i = 0
                    for select_age in select_ages:
                        i += 1
                        if query[5+ i]:
                            select = Select(select_age)
                            select.select_by_value(query[5 + i])
                        else:
                            print("wrong query: " + "eta dei bambini{} is empty : ".format(str(i)) + query[5 + i])
                            return False
                btn_confirm = dealform_extRooms.find_element_by_class_name('confirm')
                btn_confirm.click()

            else:
                print("wrong query: " + "adulti is not correct : " + query[4])
                return False

        elif 'camera multiple'.lower() in query[3].lower():
            btn_roomtypes[3].click()
            time_sleep(1)
            if query[4]:
                dealform_extRooms = driver.find_element_by_id('dealform_extRooms')
                select = Select(dealform_extRooms.find_element_by_id('select-num-adults-2'))
                select.select_by_value(query[4])
                if query[5]:
                    select = Select(dealform_extRooms.find_element_by_id('select-num-children-2'))
                    select.select_by_value(query[5])
                    time_sleep(1)
                    select_ages = dealform_extRooms.find_elements_by_class_name('js-select-child-age')
                    i = 0
                    for select_age in select_ages:
                        i += 1
                        if query[5 + i]:
                            select = Select(select_age)
                            select.select_by_value(query[5 + i])
                        else:
                            print("wrong query: " + "eta dei bambini{} is empty : ".format(str(i)) + query[5 + i])
                            return False
                btn_confirm = dealform_extRooms.find_element_by_class_name('confirm')
                btn_confirm.click()

            else:
                print("wrong query: " + "adulti is not correct : " + query[4])
                return False

        else:
            print("wrong query: " + "camera is not correct : " + query[3])
            return False
        time_sleep(1)
        # cur_url = str(driver.current_url)
        # cur_toPrice = ''
        # new_toPrice = ''
        if query[10]:
            move = ActionChains(driver)
            slider = driver.find_element_by_class_name('fl-slider__handle')
            cur_width = driver.find_element_by_class_name('fl-slider__range').size['width']
            # while True:
            #     width1 = driver.find_element_by_class_name('fl-slider__range').size['width']
            #     width = driver.find_element_by_class_name('fl-slider').size['width']
            #     print(width)
            #     print(width1)

            dis_width = lst_price[query[10].strip()]
            n_offset = dis_width - cur_width

            move.click_and_hold(slider).move_by_offset(n_offset, 0).release().perform()
        # for str_split in cur_url.split('&'):
        #     if 'aPriceRange%5Bto%5D=' in str_split:
        #         cur_toPrice = str_split
        #         if query['pricing']:
        #             new_toPrice = 'aPriceRange%5Bto%5D=' + str(query['pricing']) + '00'
        #         else:
        #             new_toPrice = 'aPriceRange%5Bto%5D=' + '0'
        #         cur_url = cur_url.replace(cur_toPrice, new_toPrice)
        #         driver.get(cur_url)
        toolbar_stars = driver.find_element_by_class_name('js-toolbar-stars').find_element_by_tag_name('button')
        toolbar_stars.click()
        popover__body_stars = driver.find_elements_by_class_name('popover__body--stars')
        n_df = len(popover__body_stars)
        while (n_df == 0):
            toolbar_stars.click()
            popover__body_stars = driver.find_elements_by_class_name('popover__body--stars')
            n_df = len(popover__body_stars)

        reset_button = popover__body_stars[0].find_element_by_id('filter-popover-reset-button')
        reset_button.click()

        if 'tutti I tipi' in query[11].lower():
            btn_0 = popover__body_stars[0].find_element_by_id('acc-type-filter-0')
            btn_0.click()
        elif 'solo casa vacanza' in query[11].lower():
            btn_2 = popover__body_stars[0].find_element_by_id('acc-type-filter-2')
            btn_2.click()
        elif 'solo hotel' in query[11].lower():
            startmp = query[11].replace('solo hotel', '').replace('stelle','')
            stars = startmp.replace('Solo hotel', '').replace('Stelle', '').strip().split(',')
            btn_stars = popover__body_stars[0].find_element_by_class_name('refinement-row__content').find_elements_by_tag_name('button')
            for star in stars:
                star = int(star.strip())
                btn_stars[(star - 1)].click()
                time_sleep(1)

        btn_done = popover__body_stars[0].find_element_by_id('filter-popover-done-button')
        btn_done.click()
        time.sleep(5)

        print(query[12])
        if query[12]:
            ordervalue = query[12]
            xpath = ("//select[@name='mf-select-sortby']/option[text()='{}']").format(ordervalue)
            driver.find_element_by_xpath(xpath).click()
            time.sleep(5)
    except:
        print("Restart driver")
        driver.quit()
        time_sleep(5)
        driver = get_seleniumdriver('https://www.trivago.it/')
        input_datein = datetime.datetime.strptime(query[1], "%d/%m/%Y").date()
        max_date = datetime.date(input_datein.year + 1, input_datein.month,
                                 calendar.monthrange(input_datein.year + 1, input_datein.month)[1])
        if input_datein < datetime.datetime.now().date():
            print("wrong query: " + "starting_period is low current date : " + query[1])
            return False
        elif input_datein > max_date:
            print("wrong query: " + "starting_period is low max date : " + query[1])
            return False

        input_dateout = datetime.datetime.strptime(query[2], "%d/%m/%Y").date()
        nyear = input_dateout.year
        nmonth = input_dateout.month + 2
        if input_dateout.month + 2 > 12:
            nyear += 1
            nmonth = nmonth - 12
        max_date = datetime.date(nyear, nmonth, calendar.monthrange(nyear, nmonth)[1])
        if input_dateout < input_datein:
            print("wrong query: " + "ending_period is low starting_period + 3month : " + query[2])
            return False
        elif input_dateout > max_date:
            print("wrong query: " + "ending_period is low max date : " + query[2])
            return False

        '''run query'''
        querytext = driver.find_element_by_id('querytext')
        driver.implicitly_wait(30)
        querytext.clear()
        querytext.send_keys(query[0])
        time_sleep(1)
        querytext.send_keys(Keys.ENTER)
        # select date-in

        btn_date_in = driver.find_element_by_class_name('calendar-button-wrapper--checkin')
        btn_date_in.click()
        btn_date_in.click()
        time_sleep(1)
        df_container_calendars = driver.find_elements_by_class_name('df_container_calendar')
        n_df = len(df_container_calendars)
        while (n_df == 0):
            btn_date_in.click()
            # btn_date_in.click()
            time_sleep(1)
            df_container_calendars = driver.find_elements_by_class_name('df_container_calendar')
            n_df = len(df_container_calendars)

        df_container_calendar = df_container_calendars[0]
        td_days = df_container_calendar.find_elements_by_class_name('cal-day-wrap')
        td_time = td_days[10].find_element_by_tag_name('time').get_attribute('datetime')
        td_time = datetime.datetime.strptime(td_time, "%Y-%m-%d")
        n_step = 0
        if td_time.month != input_datein.month or td_time.year != input_datein.year:
            if input_datein.year > td_time.year:
                n_step = input_datein.month + (12 - td_time.month)

            elif input_datein.year < td_time.year:
                n_step = 0 - td_time.month - (12 - input_datein.month)
            else:
                n_step = input_datein.month - td_time.month
        if n_step > 0:
            btn_next = df_container_calendar.find_element_by_class_name('cal-btn-next')
            for i in range(n_step):
                btn_next.click()
                time_sleep(1)
        elif n_step < 0:
            btn_prev = df_container_calendar.find_element_by_class_name('cal-btn-prev')
            n_step = abs(n_step)
            for i in range(n_step):
                btn_prev.click()
                time_sleep(1)

        td_days = df_container_calendar.find_elements_by_class_name('cal-day-wrap')
        for td_day in td_days:
            td_time = td_day.find_element_by_tag_name('time').get_attribute('datetime')
            td_time = datetime.datetime.strptime(td_time, "%Y-%m-%d").date()
            if td_time == input_datein:
                td_day.click()
                break
        time_sleep(1)

        btn_date_in = driver.find_element_by_class_name('calendar-button-wrapper--checkout')
        btn_date_in.click()
        time_sleep(1)
        btn_date_in.click()
        time_sleep(1)
        df_container_calendars = driver.find_elements_by_class_name('df_container_calendar')
        n_df = len(df_container_calendars)
        while (n_df == 0):
            btn_date_in.click()
            # btn_date_in.click()
            time_sleep(1)
            df_container_calendars = driver.find_elements_by_class_name('df_container_calendar')
            n_df = len(df_container_calendars)

        df_container_calendar = df_container_calendars[0]
        td_days = df_container_calendar.find_elements_by_class_name('cal-day-wrap')
        td_time = td_days[10].find_element_by_tag_name('time').get_attribute('datetime')
        td_time = datetime.datetime.strptime(td_time, "%Y-%m-%d")
        n_step = 0
        if td_time.month != input_dateout.month or td_time.year != input_dateout.year:
            if input_dateout.year > td_time.year:
                n_step = input_dateout.month + (12 - td_time.month)

            elif input_dateout.year < td_time.year:
                n_step = 0 - td_time.month - (12 - input_dateout.month)
            else:
                n_step = input_dateout.month - td_time.month
        if n_step > 0:
            btn_next = df_container_calendar.find_element_by_class_name('cal-btn-next')
            for i in range(n_step):
                btn_next.click()
                time_sleep(1)
        elif n_step < 0:
            btn_prev = df_container_calendar.find_element_by_class_name('cal-btn-prev')
            n_step = abs(n_step)
            for i in range(n_step):
                btn_prev.click()
                time_sleep(1)

        td_days = df_container_calendar.find_elements_by_class_name('cal-day-wrap')
        for td_day in td_days:
            td_time = td_day.find_element_by_tag_name('time').get_attribute('datetime')
            td_time = datetime.datetime.strptime(td_time, "%Y-%m-%d").date()
            if td_time == input_dateout:
                td_day.click()
                break
        time_sleep(1)

        """selecting camera"""
        btn_camera = driver.find_element_by_class_name('dealform-button--guests')
        btn_camera.click()
        btn_camera.click()
        time_sleep(1)
        df_overlays = driver.find_elements_by_class_name('df_overlay')

        n_df = len(df_overlays)
        while (n_df == 0):
            btn_camera.click()
            time_sleep(1)
            df_overlays = driver.find_elements_by_class_name('df_overlay')

            n_df = len(df_overlays)

        btn_roomtypes = df_overlays[0].find_elements_by_class_name('roomtype-btn')
        if 'camera singola'.lower() in query[3].lower():
            btn_roomtypes[0].click()
            time_sleep(1)
            btn_search = driver.find_element_by_class_name('search-button')
            btn_search.click()
        elif 'camera doppia'.lower() in query[3].lower():
            btn_roomtypes[1].click()
            time_sleep(1)
            btn_search = driver.find_element_by_class_name('search-button')
            btn_search.click()
        elif 'camere familiari'.lower() in query[3].lower():
            btn_roomtypes[2].click()
            time_sleep(1)
            if query[4]:
                dealform_extRooms = driver.find_element_by_id('dealform_extRooms')
                select = Select(dealform_extRooms.find_element_by_id('select-num-adults-2'))
                select.select_by_value(query[4])
                if query[5]:
                    select = Select(dealform_extRooms.find_element_by_id('select-num-children-2'))
                    select.select_by_value(query[5])
                    time_sleep(1)
                    select_ages = dealform_extRooms.find_elements_by_class_name('js-select-child-age')
                    i = 0
                    for select_age in select_ages:
                        i += 1
                        if query[5 + i]:
                            select = Select(select_age)
                            select.select_by_value(query[5 + i])
                        else:
                            print("wrong query: " + "eta dei bambini{} is empty : ".format(str(i)) + query[
                                5 + i])
                            return False
                btn_confirm = dealform_extRooms.find_element_by_class_name('confirm')
                btn_confirm.click()

            else:
                print("wrong query: " + "adulti is not correct : " + query[4])
                return False

        elif 'camera multiple'.lower() in query[3].lower():
            btn_roomtypes[3].click()
            time_sleep(1)
            if query[4]:
                dealform_extRooms = driver.find_element_by_id('dealform_extRooms')
                select = Select(dealform_extRooms.find_element_by_id('select-num-adults-2'))
                select.select_by_value(query[4])
                if query[5]:
                    select = Select(dealform_extRooms.find_element_by_id('select-num-children-2'))
                    select.select_by_value(query[5])
                    time_sleep(1)
                    select_ages = dealform_extRooms.find_elements_by_class_name('js-select-child-age')
                    i = 0
                    for select_age in select_ages:
                        i += 1
                        if query[5 + i]:
                            select = Select(select_age)
                            select.select_by_value(query[5 + i])
                        else:
                            print("wrong query: " + "eta dei bambini{} is empty : ".format(str(i)) + query[
                                5 + i])
                            return False
                btn_confirm = dealform_extRooms.find_element_by_class_name('confirm')
                btn_confirm.click()

            else:
                print("wrong query: " + "adulti is not correct : " + query[4])
                return False

        else:
            print("wrong query: " + "camera is not correct : " + query[3])
            return False
        time_sleep(1)
        # cur_url = str(driver.current_url)
        # cur_toPrice = ''
        # new_toPrice = ''
        if query[10]:
            move = ActionChains(driver)
            slider = driver.find_element_by_class_name('fl-slider__handle')
            cur_width = driver.find_element_by_class_name('fl-slider__range').size['width']
            # while True:
            #     width1 = driver.find_element_by_class_name('fl-slider__range').size['width']
            #     width = driver.find_element_by_class_name('fl-slider').size['width']
            #     print(width)
            #     print(width1)

            dis_width = lst_price[query[10].strip()]
            n_offset = dis_width - cur_width

            move.click_and_hold(slider).move_by_offset(n_offset, 0).release().perform()
            time.sleep(5)

        # for str_split in cur_url.split('&'):
        #     if 'aPriceRange%5Bto%5D=' in str_split:
        #         cur_toPrice = str_split
        #         if query['pricing']:
        #             new_toPrice = 'aPriceRange%5Bto%5D=' + str(query['pricing']) + '00'
        #         else:
        #             new_toPrice = 'aPriceRange%5Bto%5D=' + '0'
        #         cur_url = cur_url.replace(cur_toPrice, new_toPrice)
        #         driver.get(cur_url)
        toolbar_stars = driver.find_element_by_class_name('js-toolbar-stars').find_element_by_tag_name('button')
        toolbar_stars.click()
        popover__body_stars = driver.find_elements_by_class_name('popover__body--stars')
        n_df = len(popover__body_stars)
        while (n_df == 0):
            toolbar_stars.click()
            popover__body_stars = driver.find_elements_by_class_name('popover__body--stars')
            n_df = len(popover__body_stars)

        reset_button = popover__body_stars[0].find_element_by_id('filter-popover-reset-button')
        reset_button.click()

        print("-{}".format(query[11]));
        if 'tutti I tipi' in query[11].lower():
            btn_0 = popover__body_stars[0].find_element_by_id('acc-type-filter-0')
            btn_0.click()
        elif 'solo casa vacanza' in query[11].lower():
            btn_2 = popover__body_stars[0].find_element_by_id('acc-type-filter-2')
            btn_2.click()
        elif 'solo hotel' in query[11].lower():
            startmp = query[11].replace('solo hotel', '').replace('stelle', '')
            stars = startmp.replace('Solo hotel', '').replace('Stelle', '').strip().split(',')
            btn_stars = popover__body_stars[0].find_element_by_class_name(
                'refinement-row__content').find_elements_by_tag_name('button')
            for star in stars:
                star = int(star.strip())
                if (star - 1) >= 0:
                    btn_stars[(star - 1)].click()
                    time_sleep(1)

        btn_done = popover__body_stars[0].find_element_by_id('filter-popover-done-button')
        btn_done.click()
        time.sleep(5)

        print("--{}".format(query[12]))
        if query[12]:
            ordervalue = query[12]
            xpath = ("//select[@name='mf-select-sortby']/option[text()='{}']").format(ordervalue)
            driver.find_element_by_xpath(xpath).click()
            time.sleep(5)

    """ get data """
    b_true = True
    lst_result = []
    while b_true:
        print("---start")        # js_itemlist = driver.find_element_by_id('js_itemlist')
        # li_itemlist = js_itemlist.find_elements_by_tag_name('li')

        #itemlist = driver.find_elements_by_class_name('hotel-item')
        #btn_prices = driver.find_elements_by_xpath('//button[@data-qa="cheapest-deal"]')
        
            #WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.CLASS_NAME, "hotel-item")))
            #WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.XPATH, '//button[@data-qa="cheapest-deal"]')))


        itemlist = driver.find_elements_by_class_name('hotel-item')
        btn_prices = driver.find_elements_by_xpath('//button[@data-qa="cheapest-deal"]')
        driver.implicitly_wait(30)
        

        print('----hotel-item count:{}'.format(len(itemlist)))
        lst_result = []
        # n_item = 0
        n_result = 0
        for n_item in range(len(itemlist)):
            print("----")
            print('----hotelindex:{}'.format(n_result + 1))
            print("-----find itemlist1 ")
            itemlist1 = driver.find_elements_by_class_name('hotel-item')
            item = itemlist1[n_item]
            result = {}
            for key in output_header:
                result[key] = ''
            result['merchant'] = 'trivago'
            result['scraping_date'] = str_date
            result['city_name'] = query[0]
            result['Starting_period'] = query[1]
            result['Ending_period'] = query[2]
            result['Camera'] = query[3]
            result['currency'] = "eur"
            print("-----find hotel_name")
            result['hotel_name'] = item.find_element_by_class_name('name__copytext').text.strip()
            # get stars
            print("-----find star")
            # soup = BeautifulSoup(item.get_attribute('innerHTML'), 'html.parser')
            if "stars-wrp" in item.get_attribute('innerHTML'):
                lst_star = item.find_elements_by_class_name('star')
                # lst_star = WebDriverWait(item, 2).until(ec.visibility_of_all_elements_located((By.CLASS_NAME, "star")))
                result['star'] = str(len(lst_star))

            # get price
            # prices = None
            # btns = item.find_elements_by_tag_name('button')
            # for btn_price in btns:
            #     if 'cheapest-deal' in btn_price.get_attribute('data-qa'):
            #         btn_price.click()
            #         time_sleep(1)
            #         sl_boxs = item.find_elements_by_class_name('sl-box')
            #         if len(sl_boxs) == 0:
            #             btn_price.click()
            #             time_sleep(1)
            #             sl_boxs = item.find_elements_by_class_name('sl-box')
            #
            #         sl_box = sl_boxs[0]
            #         ol = sl_box.find_element_by_tag_name('ol')
            #         prices = ol.find_elements_by_xpath('//span[@data-qa="slideout-deal-price"]')
            #         break

            # btn_price = item.find_element_by_xpath('//button[@data-qa="cheapest-deal"]')
            # print("find btn_price ")
            # btn_prices = driver.find_elements_by_xpath('//button[@data-qa="cheapest-deal"]')

            btn_prices = item.find_element_by_class_name('item__flex-column').find_element_by_tag_name('section').find_elements_by_tag_name('article')
            btn_price = None
            for btn_a in btn_prices:
                if "accommodation-list__cheapest--" in btn_a.get_attribute("class"):
                    if btn_a.find_element_by_tag_name("button").get_attribute("data-qa") == "cheapest-deal":
                        btn_price = btn_a
                    break

            # if btn_prices[(len(btn_prices)-1)].find_element_by_tag_name('button').get_attribute("data-qa") != "cheapest-deal":
            
            if btn_price == None:
                lst_result.append(result)

                writer.writerow(result)
                n_result += 1
                print("-----{}".format(result))
                continue
            else:
            # btn_price = btn_prices[(len(btn_prices)-1)]
                try:
                    btn_price.click()
                except:
                    continue

            # btn_price = btn_prices[n_item]
            # try:
            #     btn_price.click()
            # except:
            #     print("try: find btn_prices ")
            #     btn_prices = driver.find_elements_by_xpath('//button[@data-qa="cheapest-deal"]')
            #     btn_price = btn_prices[n_item]
            #     btn_price.click()

            # btn_price = WebDriverWait(item, 10).until(ec.element_to_be_clickable((By.XPATH, '//button[@data-qa="cheapest-deal"]')))
            time_sleep(5)
            print("-----find sl_boxs ")
            try:
                sl_box = item.find_element_by_class_name('sl-box')
            # if len(sl_boxs) <= 0:
            except:
                # print("try: find sl_boxs ")
                # btn_price.click()
                # btn_price = item.find_element_by_class_name('item__flex-column').find_element_by_tag_name(
                #     'section').find_element_by_tag_name('article')
                # btn_price.click()
                # time_sleep(5)
                # sl_box = item.find_element_by_class_name('sl-box')
                continue
            # sl_box = sl_boxs[0]
            print("-----find sections ")
            try:
                sections = sl_box.find_elements_by_tag_name('section')
            except:
                # time_sleep(5)
                print("------try: find sl_boxs sections")
                sl_box = item.find_element_by_class_name('sl-box')
                sections = sl_box.find_elements_by_tag_name('section')

            section = None
            ltr = None
            try:
                for section in sections:
                    if 'slideouts__section--' in section.get_attribute('class'):
                        break
                if section:
                    print("-------find ltr ")
                    try:
                        ltr = WebDriverWait(section, 30).until(
                            ec.visibility_of_element_located((By.XPATH, "//div[@dir='ltr']")))
                    except TimeoutException:
                        print("-------no existing ltr")
                        continue
            except:
                try:
                    sl_box = item.find_element_by_class_name('sl-box')
                    sections = sl_box.find_elements_by_tag_name('section')
                except:
                    time_sleep(5)
                    print("------try: find sl_boxs sections")
                    sections = sl_box.find_elements_by_tag_name('section')
                for section in sections:
                    if 'slideouts__section--' in section.get_attribute('class'):
                        break
                if section:
                    print("------retry to find ltr ")
                    try:
                        ltr = WebDriverWait(section, 30).until(
                            ec.visibility_of_element_located((By.XPATH, "//div[@dir='ltr']")))
                    except TimeoutException:
                        print("------no existing ltr")
            # ol = sl_box.find_element_by_tag_name('ol')
            print("-----find prices ")
            try:
                prices = ltr.find_elements_by_xpath('//span[@data-qa="slideout-deal-price"]')

                if prices:
                    n_price = 0
                    for price in prices:

                        n_price += 1
                        if n_price > 5:
                            continue
                        spans = price.find_elements_by_tag_name('span')
                        for span in spans:                                
                            if 'slideouts__price' in span.get_attribute('class'):
                                result[('Price ' + str(n_price))] = span.text.strip().replace("€", "")
                                print('------Price ' + str(n_price) + ":" + span.text.strip().replace("€", ""))
            except:
                print('------try again: search price tags.')
                prices = ltr.find_elements_by_xpath('//span[@data-qa="slideout-deal-price"]')

                if prices:
                    n_price = 0
                    for price in prices:
                        
                        n_price += 1
                        if n_price > 5:
                            continue
                        spans = price.find_elements_by_tag_name('span')
                        for span in spans:
                            if 'slideouts__price' in span.get_attribute('class'):
                                result[('Price ' + str(n_price))] = span.text.strip().replace("€", "")
                                print('------Price ' + str(n_price) + ":" + span.text.strip().replace("€", ""))

            btn_price.click()
            time_sleep(2)

            lst_result.append(result)

            writer.writerow(result)
            n_result += 1
            print("-----result:{}".format(result))


        try:
            btn_page_next = driver.find_element_by_class_name('btn--next')
            btn_page_next.click()
            time.sleep(5)
        except:
            break


    return lst_result


if __name__ == '__main__':
    config_option = load_config()

    lst_query = get_query(config_option['input_path'])

    out_file = config_option['out_path']
    csvfile = open(out_file, 'w')
    writer = csv.DictWriter(csvfile, delimiter=";", fieldnames=output_header)
    writer.writeheader()

    driver = get_seleniumdriver('https://www.trivago.it/')

    results = []
    #for one_query in lst_query:
    #    one_result = get_data(driver, one_query, writer)
    #    results.extend(one_result)

    itemindex = 1
    for one_query in lst_query:
        #driver.close()
        print("---------{}----------".format(itemindex))
        if itemindex % 10 == 0 and itemindex != 1:
            driver.quit()
            time.sleep(20)
            driver = get_seleniumdriver('https://www.trivago.it/')

        one_result = get_data(driver, one_query, writer)
        results.extend(one_result)
        itemindex = itemindex + 1


    driver.close()
    csvfile.close()



    print("\n~ ~ ~ F i n i s h e d ~ ~ ~ ")
