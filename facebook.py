# -*- coding: utf-8 -*-
from browser import Browser
import time
from config import Config
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys

class Facebook(Browser):
  def __init__(self):
    self.start_url = "http://www.facebook.com/"
    self.config = Config(self.__class__.__name__)

  def start(self, browser="chrome"):
    Browser.start(self, browser)
    self.driver.set_window_position(350, 0)
    self.driver.set_window_size(307, 700)
    self.driver.set_page_load_timeout(60)

  def start_work(self):
    self.start()
    self.driver.get(self.start_url)
    if self.config.get("login") and self.config.get("password"):
      self.login(self.config.get("login"), self.config.get("password"))
      self.is_start = True
    else:
      self.is_start = False

  def login(self, login, password):
    self.driver.find_element_by_name("email").send_keys(login)
    self.driver.find_element_by_name("pass").send_keys(password)
    self.driver.find_element_by_id("loginbutton").find_element_by_tag_name("input").click()
    time.sleep(2)


  def publish(self, obj_publ):
    if self.is_start:
      try:
        textarea = self.driver.find_element_by_name("xhpc_message")
        textarea.click()
        time.sleep(5)
        textarea = self.driver.find_element_by_name("xhpc_message_text")
        textarea.send_keys("http://uh.ru/a/"+obj_publ.id_article+"/201273")
        textarea.send_keys(Keys.RETURN)
        time.sleep(5)
        textarea.send_keys(Keys.CONTROL, Keys.RETURN)
      except:
        print("Не получилось запостить в facebook")

  def refresh(self):
    self.driver.refresh()