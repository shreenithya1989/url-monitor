import json
import logging
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import WebDriverException, NoSuchElementException

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename="url-monitor.log",
    level=logging.INFO,
    datefmt='%d-%b-%y %H:%M:%S')


def read_config():
    with open('config.json') as data_file:
        data = json.load(data_file)
    return data


def read_urls(each_url):
    logging.debug("Testing Url %s started" % each_url['url'])
    driver = webdriver.Chrome()
    try:
        driver.get(each_url['url'])
        driver.maximize_window()
        response_start = driver.execute_script(
            "return window.performance.timing.responseStart")
        dom_complete = driver.execute_script(
            "return window.performance.timing.domComplete")

        if "containsText" in each_url:
            containing_text = each_url['containsText']
            expected_elements = driver.find_elements_by_xpath(
                "//*[contains(text(), '"+containing_text+"')]")
            if len(expected_elements) == 0:
                raise NoSuchElementException("No Match Found")

        page_load_time = dom_complete - response_start
        logging.info("url: %s, status: success, responseTime: %s",
                     each_url['url'], page_load_time)
    except NoSuchElementException as err:
        logging.error("url: %s, status: fail, message: %s",
                      each_url['url'], err.msg)
    except WebDriverException as err:
        logging.error("url: %s, status: fail, message: %s",
                      each_url['url'], err.msg)

    driver.close()
    logging.debug("Testing Url %s completed" % each_url['url'])


def run_all_test():
    config = read_config()
    while True:
        logging.info("URL monitoring started")
        for each_url in config['urls']:
            read_urls(each_url)
        logging.info("URL monitoring stopped")
        sleep(config["testInterval"] if "testInterval" in config else 5)


run_all_test()
