# -*- coding: utf-8 -*-
from browser import Browser
from pymouse import PyMouse
import helper
import subprocess
import os
import time
CAPTCHA_DIR = "captcha/"

class Uh_ru(Browser):

  def __init__(self):
    self.login_url = "http://uh.ru/login/"
    self.start_url = "http://uh.ru"
    self.mouse = PyMouse()

  def start(self, browser="chrome"):
    Browser.start(self, browser)
    self.driver.set_window_position(350, 0)
    self.driver.set_window_size(307, 700)
    self.driver.set_page_load_timeout(60)

  def login(self, login, password):
    try:
      self.open_url("http://uh.ru/login/")
    except:
      pass
    self.driver.find_element_by_css_selector("form.user_auth").find_element_by_name("login").send_keys(login)
    self.driver.find_element_by_css_selector("form.user_auth").find_element_by_name("password").send_keys(password)
    try:
      self.driver.find_element_by_css_selector("form.user_auth").find_element_by_name("enter").click()
    except:
      pass

  def input_captcha(self, login_url):
    while True:
      if self.get_url() == login_url:
        url_captcha = self.driver.find_element_by_name("signup").find_element_by_css_selector("img").get_attribute("src")
        captcha = url_captcha.split('/')[-1]
        self.driver.get_screenshot_as_file(CAPTCHA_DIR+captcha+".png")
        helper.change_screenshot(CAPTCHA_DIR+captcha+".png")
        batcmd='python input_captcha.py ' + CAPTCHA_DIR + captcha
        text = subprocess.check_output(batcmd, shell=True)
        os.remove(CAPTCHA_DIR+captcha+".png")
        if str(text) != "None":
          self.driver.find_element_by_name("keystring").send_keys(str(text))
          try:
            self.driver.find_element_by_name("signup").find_element_by_name("enter").click()
          except:
            pass
          time.sleep(1)
          if self.get_url() == login_url:
            continue
          else:
            break
        else:
          break

  def start_work(self, login, password):
    self.start()
    self.login(login, password)
    self.input_captcha("http://uh.ru/login/")

  def refresh(self):
    try:
      self.driver.refresh()
    except:
      pass