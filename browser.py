# -*- coding: utf-8 -*-
from selenium import webdriver
class Browser:

  def start(self, browser="chrome"):
    if browser == "chrome":
      chrome_options = webdriver.ChromeOptions()
      chrome_options.add_argument('--ipc-connection-timeout=%s' % "30")
      self.driver = webdriver.Chrome(chrome_options=chrome_options)
    elif browser == "firefox":
      self.driver = webdriver.Firefox()
    

  def close(self):
    self.driver.close()

  def open_url(self, url):
    try:
      self.driver.get(url)
    except:
      pass

  def get_url(self):
    return self.driver.current_url