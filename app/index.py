import json
from selenium import webdriver


def read_config():
    with open("config.json") as jsonFile:
        config = json.load(jsonFile)
    return config


def test_url(url_object):
    print("Testing URL %s Started" % url_object['url'])
    driver = webdriver.Chrome()
    driver.get(url_object['url'])

    response_start = driver.execute_script("return window.performance.timing.responseStart")
    dom_complete = driver.execute_script("return window.performance.timing.domComplete")

    page_load_time = dom_complete - response_start
    print("%s" % page_load_time)
    print("Testing URL %s Completed" % url_object['url'])
    driver.close()


def run_all_test():
    config = read_config()
    for url_object in config['urls']:
        test_url(url_object)


run_all_test()
