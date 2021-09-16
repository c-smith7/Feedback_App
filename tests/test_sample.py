import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


@pytest.fixture()
def test_setup():
    global driver
    driver = webdriver.Chrome(executable_path="C:\\Users\\mcmco\\Desktop\\Python_scripts\\Feedback_GUI\\chromedriver.exe")
    yield
    driver.close()
    driver.quit()
    print("sample test complete")


def test_search(test_setup):
    driver.get("https://www.google.com/")
    driver.find_element_by_name("q").send_keys("manchester city" + Keys.ENTER)
    time.sleep(2)
