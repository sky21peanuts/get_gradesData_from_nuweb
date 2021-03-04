# -*- coding: utf-8 -*-

import os
import re
import time
import sys
import codecs
import shutil
import getpass
import warnings
from datetime import datetime as dt
from selenium import webdriver
from selenium.webdriver.common.keys import Keys as keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException


DRIVER_PATH = '../driver/chromedriver'
DefaultFileName = 'kakuteiSeisekiCsv.csv'
NUWEB = 'https://nuweb.nagasaki-u.ac.jp/'
VCONN = 'https://v-conn.nagasaki-u.ac.jp'
DL_DIR = '/Users/' + os.getlogin() + '/Downloads/'
WAIT_TIME = 5


# Log color setting
class pycolor:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    PURPLE = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    END = '\033[0m'
    BOLD = '\038[1m'
    UNDERLINE = '\033[4m'
    INVISIBLE = '\033[08m'
    REVERCE = '\033[07m'


# Detecting OS
def checkOS():
    if os.name == 'posix':
        return 0
    elif os.name == 'nt':
        return 1
    else:
        return 99


# Changing driver name by checkOS()
def detectDriver():
    if checkOS() == 1:
        DRIVER_PATH.replace('chromedriver', 'chromedriver.exe')
    else:
        pass


# Changing download directory by checkOS()
def dlOptions(opt):
    global DL_DIR
    if checkOS() == 1:
        DL_DIR = 'C:' + DL_DIR
        WIN = DL_DIR.replace('/', '\\')
        opt.add_experimental_option('prefs', {
            'download.default_directory': WIN
        })
    else:
        opt.add_experimental_option('prefs', {
            'download.default_directory': DL_DIR
        })


# Authenicationg before access and download
def authenication():
    # Hide warning : DeprecationWarning by option
    try:
        warnings.simplefilter('ignore', DeprecationWarning)
        opt = Options()
        opt.add_argument('--headless')
        detectDriver()
        driver = webdriver.Chrome(executable_path = DRIVER_PATH, chrome_options = opt)
        driver.get(NUWEB)
        driver.set_window_size(1200, 980)
        time.sleep(WAIT_TIME)
    except FileNotFoundError:
        driverError()
        sys.exit()
    except WebDriverException:
        driverError()
        sys.exit()

    # login trials : 3 times
    for count in range(3):
        # 2 times over : error message is printed
        if count == 0:
            print(pycolor.CYAN + '\n----------Start Authenication to CAS----------\n' + pycolor.END)
        else:
            print(pycolor.RED + '\nID or password is invalid.\n' + pycolor.END)
        id = input('　　長大ID : ')
        pw = getpass.getpass('パスワード : ')

        id_field = driver.find_element_by_xpath('//*[@id="LoginFormSimple"]/tbody/tr[1]/td[2]/input')
        id_field.send_keys(id)
        pw_field = driver.find_element_by_xpath('//*[@id="LoginFormSimple"]/tbody/tr[2]/td[2]/input')
        pw_field.send_keys(pw)
        driver.find_element_by_xpath('//*[@id="LoginFormSimple"]/tbody/tr[3]/td/button[1]/span').click()
        time.sleep(WAIT_TIME)
        try:
            once = driver.find_element_by_xpath('/html/body/div[10]/div[2]/div[2]/div/center/input')
        except NoSuchElementException:
            driver.find_element_by_xpath('/html/body/div[6]/div/div[1]/div[2]/div/div/div[3]/div[2]/div/div[2]/ul[6]/li[1]').click()
            time.sleep(WAIT_TIME)
            driver.service.stop()
            print(pycolor.CYAN + '\n----------Authenication successfully----------\n' + pycolor.END)
            return id, pw
        else:
            once.click()
            if count == 2:
                print(pycolor.RED + '\n-----------------Login Failed-----------------\n' + pycolor.END)
                print(pycolor.CYAN + '\n-------The session has been terminated.-------\n' + pycolor.END)
                return 0
            continue


# Main block for this app
def getGradeCSV(id, pw):
    # process to go to page
    try:
        print(pycolor.CYAN + '----------Continue to getting grades----------\n' + pycolor.END)
        warnings.simplefilter('ignore', DeprecationWarning)
        opt = Options()
        opt.add_argument('--headless')
        dlOptions(opt)
        detectDriver()
        driver = webdriver.Chrome(executable_path = DRIVER_PATH, options = opt)
        print(pycolor.CYAN + '!--- Loading v-conn' + pycolor.END)
        driver.get(VCONN)
        print(pycolor.CYAN + '!--- Loaded v-conn successfully' + pycolor.END)
        driver.set_window_size(1200, 980)
        time.sleep(WAIT_TIME)
    except FileNotFoundError:
        driverError()
        sys.exit()
    except WebDriverException:
        driverError()
        sys.exit()

    # process to login
    print(pycolor.CYAN + '!--- Trying to login' + pycolor.END)
    id_field = driver.find_element_by_xpath('//*[@id="username"]')
    id_field.send_keys(id)
    pw_field = driver.find_element_by_xpath('//*[@id="password_input"]')
    pw_field.send_keys(pw)
    driver.find_element_by_xpath('//*[@id="form_table"]/tbody/tr[3]/td/div/table/tbody/tr[4]/td/input').click()
    print(pycolor.CYAN + '!--- Logged in successfully' + pycolor.END)
    time.sleep(3)

    # After into SSL VPN Service
    print(pycolor.CYAN + '!--- Trying to open NUWeb' + pycolor.END)
    dropdown = driver.find_element_by_xpath('//*[@id="protocol_selector"]')
    Select(dropdown).select_by_index(1)
    addr = driver.find_element_by_xpath('//*[@id="unicorn_form_url"]')
    addr.send_keys(NUWEB[8:])
    driver.find_element_by_xpath('//*[@id="browse_text"]').click()
    time.sleep(WAIT_TIME)
    print(pycolor.CYAN + '!--- Loaded NUWeb successfully' + pycolor.END)

    # After CAS
    print(pycolor.CYAN + '!--- Trying to login' + pycolor.END)
    id_field = driver.find_element_by_name('username')
    id_field.send_keys(id)
    pw_field = driver.find_element_by_name('password')
    pw_field.send_keys(pw)
    driver.find_element_by_xpath('/html/body/div[2]/form/div[2]/div[1]/div[2]/a').click()
    print(pycolor.CYAN + '!--- Logged in successfully' + pycolor.END)
    time.sleep(WAIT_TIME)
    print(pycolor.CYAN + '!--- Loading grades data' + pycolor.END)
    driver.find_element_by_id('tab-si').click()
    time.sleep(WAIT_TIME)
    driver.find_element_by_xpath('/html/body/div[6]/div/div[2]/div[2]/div/div/ul/li[2]/span').click()
    time.sleep(WAIT_TIME)
    driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="main-frame-if"]'))
    driver.find_element_by_xpath('//*[@id="taniReferListForm"]/table/tfoot/tr/td/input[2]').click()
    time.sleep(WAIT_TIME)
    driver.find_element_by_xpath('//*[@id="taniReferListForm"]/p[3]/input[1]').click()
    time.sleep(WAIT_TIME)
    driver.switch_to.default_content()
    print(pycolor.CYAN + '!--- Downloaded \'kakuteiSeisekiCsv.csv\'' + pycolor.END)
    driver.find_element_by_xpath('/html/body/div[6]/div/div[1]/div[2]/div/div/div[3]/div[2]/div/div[2]/ul[6]/li[1]').click()
    time.sleep(WAIT_TIME)
    print(pycolor.CYAN + '!--- Logged out NUWeb successfully' + pycolor.END)
    driver.get(VCONN)
    time.sleep(WAIT_TIME)
    driver.find_element_by_xpath('//*[@id="logout_text"]').click()
    time.sleep(WAIT_TIME)
    print(pycolor.CYAN + '!--- Logged out v-conn successfully' + pycolor.END)
    driver.service.stop()


# Echo driveer error if chromedriver is in appropriate directory
def driverError():
    print(pycolor.YELLOW + '\nPlease put a chromedriver as following' + pycolor.END)
    print('--\n |\n |--driver\n |   |-chromedriver\n |\n |--app\n     |-app.py\n')


# csv is downloaded default download directory, so making working directory and move to there
def moveWorkdir(id):
    dateNow = dt.now()
    Username = os.getlogin()
    src = DL_DIR + DefaultFileName

    dst = '/Users/' + Username + '/Desktop/' + dateNow.strftime('%Y%m%d') + '_' + id
    if checkOS() == 1:
        dst = 'C:' + dst
    else:
        pass

    # Make output dir
    try:
        os.makedirs(dst)
    except FileExistsError:
        dst += '_tmp'
        os.makedirs(dst)
    print(pycolor.CYAN + '!!-- Made a directory to Desktop' + pycolor.END)
    # Move to dst
    shutil.move(src, dst)
    print(pycolor.CYAN + '!!-- Moved csv data to the directory on Desktop\n' + pycolor.END)

    # Return value is source file's name
    return (dst + '/')


# Here is an encoding option, to use utf-8 encoding for mac
def transcode(input, output):
    # Convert encoding from cp932 to utf-8
    with codecs.open(input, 'r', 'cp932') as fin:
        with codecs.open(output, 'w', 'utf-8') as fout:
            for row in fin:
                fout.write(row)
            fout.close()
        fin.close()


# Main block
def main():
    # Getting nu_id, nu_passwd
    try:
        NU_ID, NU_PASS = authenication()
    except TypeError:
        sys.exit()

    # Download csv
    getGradeCSV(NU_ID, NU_PASS)

    # Move to Desktop
    dir = moveWorkdir(NU_ID[2:])

    # Convert coding from cp932 to utf-8
    src = dir + 'kakuteiSeisekiCsv_utf-8.csv'
    transcode(dir + DefaultFileName, src)


if __name__ == '__main__':
    main()
