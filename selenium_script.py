from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.chrome.options import Options
import time
import pickle
import sys


class SeleniumAutomation:
    # def config_json(self):
    #     # from qt widget, function will get user name and password to dump into json config file.
    #     # this will run when login button is clicked on gui, but if user doesn't want automation, don't press login.
    #     if path.exists('config.json'):
    #         print('Logged In!')  # Print 'Logged in' next to button with Qlabel or something.
    #     else:
    #         # open login widget window
    #         # pyqt_user and pyqt_password are entered by the user
    #         # create config file to be used in get_feedback_template()
    #         pyqt_user = 'carlosvsmith7@gmail.com'    # input from gui
    #         pyqt_password = 'brazil4444'            # input from gui
    #         login_dict = dict(user_name=pyqt_user, password=pyqt_password)
    #         with open('config.json', 'w') as outfile:
    #             json.dump(login_dict, outfile)
    #         print('Logged In!!')
    # include a reset user_name and password button that deletes the config file and let's user reenter login info.
    # def reset_button():
    # try:
    #     os.remove('config.json')
    # except OSError as e:
    #     print('File deleted')

    # def verification_login(self):
    # with open('config.json', 'r') as openfile:
    #     config_file = json.load(openfile)
    # user_name = config_file['user_name']
    # password = config_file['password']
    # Sign in
    # login_email = browser.find_element_by_xpath('//*[@id="__layout"]/div/div[2]/div/div[2]/div/form/div[1]/div[1]/div/div[1]/input')
    # login_email.send_keys(user_name)
    # login_password = browser.find_element_by_xpath('//*[@id="__layout"]/div/div[2]/div/div[2]/div/form/div[1]/div[2]/div/div/input')
    # login_password.send_keys(password)
    # sign_in = browser.find_element_by_xpath('//*[@id="__layout"]/div/div[2]/div/div[2]/div/form/div[2]/button')
    # sign_in.click()
    # time.sleep(1)
    # try:
    #     WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.XPATH, "//*[@id='__layout']/div/div[2]/div/div[2]/div/form/div[1]/div[3]/div/div/input")))
    # except TimeoutException:
    #     print('No Verification needed!')  # don't print anything, just remove this else portion.
    # else:
    #     print('Please Type in Verification Code & Press Enter.')  # popup widget or message in gui.
    options = Options()
    options.add_argument('--disable-extensions')
    browser = webdriver.Chrome(options=options)
    browser.get('https://www.vipkid.com/login?prevUrl=https%3A%2F%2Fwww.vipkid.com%2Ftc%2Fmissing')

    def save_cookie(self):
        with open('cookie', 'wb') as file:
            pickle.dump(self.browser.get_cookies(), file)

    def load_cookie(self):
        try:
            with open('cookie', 'rb') as cookiesfile:
                cookies = pickle.load(cookiesfile)
                for cookie in cookies:
                    self.browser.add_cookie(cookie)
                self.browser.refresh()
                missing_cf_button = WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, 'to-do-type')))
                missing_cf_button.click()
        except Exception:
            print("Login to save cookies.")

    def get_student_name(self):
        # Wait to find the "missing cf/ua" tab"
        WebDriverWait(self.browser, 120).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[2]/div/div/ul/li[2]/a')))
        self.save_cookie()
        try:
            student_name = WebDriverWait(self.browser, 2).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[2]/div/div/div/div[2]/div/div[3]/div[3]/table/tbody/tr[1]/td[4]/div/div/div/span'))).get_attribute('innerHTML').splitlines()[0]
            print(student_name)  # populate this name in 'student name' box in GUI.
        except TimeoutException:
            print('All student feedbacks completed!')
            sys.exit(1)

    def nav_to_template(self):
        materials_button = WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__layout"]/div/div[2]/div/div[1]/div/div[2]/div/div[3]/div[3]/table/tbody/tr[1]/td[7]/div/div/div[2]')))
        materials_button.click()
        self.browser.switch_to.window(self.browser.window_handles[-1])
        self.browser.minimize_window()
        time.sleep(1)
        template_button = self.browser.find_element_by_xpath("//*[@id='tab-5']")
        self.browser.execute_script("arguments[0].click();", template_button)
        time.sleep(1)

    def select_template_text(self):
        # click show more button until all templates are shown.
        show_more_button = self.browser.find_element_by_xpath("//*[@id='__layout']/div/div/div[3]/div/div[1]/div[1]/div[2]/section/div[2]/div[4]/div/button")
        try:
            while show_more_button.is_displayed():
                self.browser.execute_script("arguments[0].click()", show_more_button)
        except StaleElementReferenceException:
            time.sleep(1)
        # Now we can just iterate through every <li> tag until we find a teacher name in csv file.
        # Find length of li tags to iterate through.
        ul_list = self.browser.find_element_by_class_name('shared-notes-list-container')
        li_tags = ul_list.find_elements_by_tag_name('li')
        valid_teachers = ['Katie EAV', 'Tammy PHT', 'Amber MZC', 'Andrew BAR', 'Kimberly BDP', 'Miranda CR',
                          'Richard ZZ', 'Tomas B', 'Stefanie BD', 'Kristina EB', 'Jessica XH', 'Thomas CH']
        non_valid_teacher_count = int(len(li_tags))
        for li_tag in li_tags:
            teacher_name = li_tag.find_element_by_xpath(".//div[2]/div[1]").get_attribute('innerHTML').splitlines()[0]
            if teacher_name in valid_teachers:
                template = li_tag.find_element_by_xpath(".//div[2]/div[2]").text
                print(template)
                break
            elif teacher_name not in valid_teachers:
                non_valid_teacher_count -= 1
                continue
        if non_valid_teacher_count == 0:
            print('No valid teacher templates :(')


test = SeleniumAutomation()
# test.config_json()
# test.verification_login()
test.load_cookie()
test.get_student_name()
test.nav_to_template()
test.select_template_text()
input('Press ENTER to end program')

