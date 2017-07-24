#!/usr/bin/python
import re
import os
import sys
import time
import requests
import urllib2
import json
import arrow
from time import gmtime, strftime
from mechanize import Browser
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from flask import Flask, render_template, redirect, url_for,request
from flask import make_response
app = Flask(__name__)
br = Browser()
cwd = os.getcwd()

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_experimental_option('prefs', {
    'credentials_enable_service': False,
    'profile': {
        'password_manager_enabled': False
    }
})
chrome_options.add_argument("--incognito")

show_id = ""
episode_name = ""

def maybankLogin(password, driver):
    driver.switch_to.frame(0)
    driver.find_element_by_xpath("//form[@name='loginForm']/table[@id='loginTable']/tbody/tr/td/input[@class='userpass']").send_keys("darrylma")
    driver.find_element_by_xpath("//form[@name='loginForm']/table[@id='loginTable']/tbody/tr/td/input[@name='action']").click()
    time.sleep(1)
    driver.find_element_by_xpath("//form[@name='loginForm']/div[@class='paddingdiv']/table/tbody/tr/td/input[@value='Yes']").click()
    time.sleep(1)
    driver.find_element_by_xpath("//input[@name='password1']").send_keys(password)
    driver.find_element_by_xpath("//input[@value='Login']").click()

def publicBankLogin(password, driver):
    driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
    driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
    driver.find_element_by_xpath("//input[@name='tempusername']").send_keys("darrylma")
    driver.find_element_by_xpath("//button[@name='Next']").click()
    time.sleep(1)
    driver.find_element_by_xpath("//span[contains(text(),'Yes')]").click()
    driver.find_element_by_xpath("//input[@id='password']").send_keys(password)
    driver.find_element_by_xpath("//button[@id='SubmitBtn']").click()

def citibankLogin(password, driver):
    driver.find_element_by_xpath("//input[@id='username']").send_keys("darrylma85")
    driver.find_element_by_xpath("//input[@id='password']").send_keys(password)
    driver.find_element_by_xpath("//a[@id='link_lkSignOn']").click()

def uobLogin(password, driver):
    uob_password = password.replace("!","")
    driver.find_element_by_xpath("//input[@id='userName']").send_keys("darrylma")
    driver.find_element_by_xpath("//input[@id='PASSWORD1']").send_keys(uob_password)
    driver.find_element_by_xpath("//button[@id='btnSubmit']").click()

def publicMutualLogin(password, driver):
    driver.find_element_by_xpath("//input[@name='txtUserName']").send_keys("DARRYLMA85")
    driver.find_element_by_xpath("//input[@name='txtPassword']").send_keys(password)
    driver.find_element_by_xpath("//a[@id='LoginButton']").click()

def epfLogin(password, driver):
    driver.find_element_by_xpath("//input[@id='id1']").send_keys("darrylma")
    driver.find_element_by_xpath("//a[contains(text(),'Next')]").click()
    driver.find_element_by_xpath("//input[@id='id4']").send_keys(password)
    driver.find_element_by_xpath("//a[@id='id5']").click()

def sspniLogin(password, driver):
    driver.find_element_by_name("j_username").send_keys("850519145937")
    driver.find_element_by_name("j_password").send_keys(password)
    driver.find_element_by_xpath("//input[@name='Hantar']").click()

def tnbLogin(password, driver):
    driver.find_element_by_xpath("//input[@id='txtusername']").send_keys("darrylma85@gmail.com")
    driver.find_element_by_xpath("//input[@id='txtpassword']").send_keys(password[0:8])
    driver.find_element_by_xpath("//input[@id='btnSubmit']").click()

def indahWaterLogin(password, driver):
    driver.find_element_by_xpath("//input[@id='username']").send_keys("darrylma")
    driver.find_element_by_xpath("//input[@id='password']").send_keys(password[0:8])
    driver.find_element_by_xpath("//input[@value='Login']").click()

def timeLogin(password, driver):
    driver.find_element_by_xpath("//input[@id='username']").send_keys("850519145937")
    driver.find_element_by_xpath("//input[@id='password']").send_keys(password[0:8])
    driver.find_element_by_xpath("//button[@id='btn_login']").click()

def openChrome(url, destination, password):
    # Ignore robots.txt
    br.set_handle_robots( False )
    # Google demands a user-agent that isn't a robot
    br.addheaders = [('User-agent', 'Firefox')]
    driver = webdriver.Chrome("chromedriver.exe", chrome_options=chrome_options)
    driver.get(url)
    if (destination == "Maybank"):
        maybankLogin(password, driver)
    elif (destination == "Public Bank"):
        publicBankLogin(password, driver)
    elif (destination == "Citibank"):
        citibankLogin(password, driver)
    elif (destination == "UOB"):
        uobLogin(password, driver)
    elif (destination == "Public Mutual"):
        publicMutualLogin(password, driver)
    elif (destination == "EPF"):
        epfLogin(password, driver)
    elif (destination == "SSPN-i"):
        sspniLogin(password, driver)
    elif (destination == "TNB"):
        tnbLogin(password, driver)
    elif (destination == "Indah Water"):
        indahWaterLogin(password, driver)
    elif (destination == "Time"):
        timeLogin(password, driver)

#### ROUTING FUNCTIONS ####
@app.route('/')
def showMainPage():
    '''
    tv_show_names = ["12 Monkeys","Billions","Black Mirror","Fear the Walking Dead","Game of Thrones","Homeland","Suits","Stranger Things","The Walking Dead","Zoo"]
    tv_shows = []
    for position, tv_show_name in enumerate(tv_show_names):
        tv_show = []
        connection = urllib2.urlopen("http://api.tvmaze.com/search/shows?q=" + tv_show_name)
        output = connection.read()
        connection.close()
        data = json.loads(output)
        #print data
        show_id = data[0]['show']['id']
        tv_show.append(tv_show_name)
        tv_show.append("http://www.imdb.com/title/" + data[0]['show']['externals']['imdb'])
        tv_show.append(data[0]['show']['rating']['average'])

        try:
            next_episode_url = data[0]['show']['_links']['nextepisode']['href']
            found = True
            connection = urllib2.urlopen(str(next_episode_url))
            output = connection.read()
            connection.close()
            data = json.loads(output)
            tv_show.append(found)
            tv_show.append(data['season'])
            tv_show.append(data['number'])
            tv_show.append(data['airdate'])
        except:
            found = False
        print tv_show

        tv_shows.append(tv_show)
    return render_template('index.html', tv_shows = tv_shows)
    '''
    return render_template('index.html')
@app.route('/openBrowser', methods=['GET', 'POST'])
def openBrowser():
    if request.method == 'POST':
        #sys.stderr.write("Test")
        url = request.form['url']
        destination = request.form['destination']
        password = request.form['password']
        openChrome(url, destination, password)
        resp = "OK"
        return resp

if __name__ == "__main__":
    app.run(debug = True)
    app.run(host='0.0.0.0', port=5000)
