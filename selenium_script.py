import pandas
from selenium import webdriver
from selenium.common.exceptions import ElementNotVisibleException, StaleElementReferenceException, \
    NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
import time
import json
import os
from os import path
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class SeleniumAutomation:
    def config_json(self):
        # from qt widget, function will get user name and password to dump into json config file.
        # this will run when login button is clicked on gui, but if user doesn't want automation, don't press login.
        if path.exists('config.json'):
            print('Logged In!')  # Print 'Logged in' next to button with Qlabel or something.
        else:
            # open login widget window
            # pyqt_user and pyqt_password are entered by the user
            # create config file to be used in get_feedback_template()
            pyqt_user = 'carlosvsmith7@gmail.com'    # input from gui
            pyqt_password = 'brazil4444'            # input from gui
            login_dict = dict(user_name=pyqt_user, password=pyqt_password)
            with open('config.json', 'w') as outfile:
                json.dump(login_dict, outfile)
            print('Logged In!!')
        # include a reset user_name and password button that deletes the config file and let's user reenter login info.
        # def reset_button():
        # try:
        #     os.remove('config.json')
        # except OSError as e:
        #     print('File deleted')

    global browser
    browser = webdriver.Chrome()
    browser.minimize_window()
    browser.get('https://www.vipkid.com/login?prevUrl=https%3A%2F%2Fwww.vipkid.com%2Ftc%2Fmissing')

    def login(self):
        with open('config.json', 'r') as openfile:
            config_file = json.load(openfile)
        user_name = config_file['user_name']
        password = config_file['password']
        # Sign in
        login_email = browser.find_element_by_xpath('//*[@id="__layout"]/div/div[2]/div/div[2]/div/form/div[1]/div[1]/div/div[1]/input')
        login_email.send_keys(user_name)
        login_password = browser.find_element_by_xpath('//*[@id="__layout"]/div/div[2]/div/div[2]/div/form/div[1]/div[2]/div/div/input')
        login_password.send_keys(password)
        sign_in = browser.find_element_by_xpath('//*[@id="__layout"]/div/div[2]/div/div[2]/div/form/div[2]/button')
        sign_in.click()
        time.sleep(1)
        try:
            WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.XPATH, "//*[@id='__layout']/div/div[2]/div/div[2]/div/form/div[1]/div[3]/div/div/input")))
        except TimeoutException:
            print('No Verification needed!')  # don't print anything, just remove this else portion.
        else:
            print('Please Type in Verification Code & Press Enter.')  # popup widget or message in gui.
            browser.maximize_window()  # window will be minimized unless verification is required.

    def get_feedback_template(self):
        materials_button = WebDriverWait(browser, 120).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__layout"]/div/div[2]/div/div[1]/div/div[2]/div/div[3]/div[3]/table/tbody/tr[1]/td[7]/div/div/div[2]')))
        materials_button.click()
        browser.switch_to.window(browser.window_handles[-1])
        browser.minimize_window()
        time.sleep(1)
        template_button = browser.find_element_by_xpath("//*[@id='tab-5']")
        browser.execute_script("arguments[0].click();", template_button)
        time.sleep(1)

    def select_template_text(self):
        # click show more button until all templates are shown.
        show_more_button = browser.find_element_by_xpath("//*[@id='__layout']/div/div/div[3]/div/div[1]/div[1]/div[2]/section/div[2]/div[4]/div/button")
        try:
            while show_more_button.is_displayed():
                browser.execute_script("arguments[0].click()", show_more_button)
        except StaleElementReferenceException as e:
            print('All templates showing!')
        time.sleep(1)
        # Now we can just iterate through every <li> tag until we find a teacher name in csv file.
        # Find length of li tags to iterate through.
        ul_list = browser.find_element_by_class_name('shared-notes-list-container')
        li_tags = ul_list.find_elements_by_tag_name('li')
        valid_teachers = ['Katie EAV', 'Tammy PHT', 'Amber MZC', 'Andrew BAR', 'Katie EAV', 'Kimberly BDP',
                          'Richard ZZ', 'Tomas B', 'Stefanie BD', 'Kristina EB', 'Jessica XH review', 'Thomas CH']
        for li_tag in li_tags:
            teacher_name = li_tag.find_element_by_xpath(".//div[2]/div[1]").get_attribute('innerHTML').splitlines()[0]
            if teacher_name in valid_teachers:
                template = li_tag.find_element_by_xpath(".//div[2]/div[2]").text
                print(template)
                break


test = SeleniumAutomation()
test.config_json()
test.login()
test.get_feedback_template()
test.select_template_text()
input('Press ENTER to end program')



# def auto_feedback():
#     student_name = input('Student name: ')
#     new_student = input('New Student?: ')
#     template = str(input('Feedback template: '))
#     feedback = template.replace('we', f'{student_name} and I', 1)
#     if new_student in ['no', 'No', 'n']:
#         print(f'{feedback} Fantastic job today {student_name}! Keep practicing your English and working hard, you are improving every class! See you next time {student_name}.' +
#             ' 亲爱的父母，如果您喜欢今天的课程，请考虑给我一个5分的苹果评估。 这项评估对我的工作非常重要。 非常感谢!' +
#             ' From, Teacher Carlos ZDG.')
#     else:
#         print(f'{feedback} Fantastic job today {student_name}! It was great meeting you. Keep up the great work, and I hope to see you in my class again soon.' +
#             ' 亲爱的父母，如果您喜欢今天的课程，请考虑给我一个5分的苹果评估。 这项评估对我的工作非常重要。 非常感谢!' +
#             ' From, Teacher Carlos ZDG.')
#
#
# auto_feedback()
