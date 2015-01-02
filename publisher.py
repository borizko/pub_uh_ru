# -*- coding: utf-8 -*-
import os
from uh_ru import Uh_ru
import re
import sys
import time
import helper
from selenium.webdriver.support.select import Select
import random
import config
import remote_manager

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

Xm = 71 #56
Ym = 299 #280

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))+"/"

class Publisher(Uh_ru):

  def __init__(self, manager_module):
    Uh_ru.__init__(self)
    self.id_article = None
    self.manager_module = manager_module
    self.body_article = None # {'name': , 'text': [...], 'img':[...], 'id_theme':}
    self.config = config.Config(self.__class__.__name__)
    self.count_article = 0
    self.remote_manager = remote_manager.instance

  def get_body_article(self, id_theme):
    self.remote_manager.check_stop()
    self.body_article = self.manager_module.get_data(id_theme)
    if self.body_article:
      return True
    return False

  def get_page_create_article(self):
    try:
      self.remote_manager.check_stop()
      self.open_url("http://uh.ru/profile/article_user/")
      self.open_url("http://uh.ru/profile/article_user/new")
    except:
      pass

  def create_body_article(self):

    self.remote_manager.check_stop()
    if not self.body_article == None:
      if not len(self.body_article['img']):
        self.set_empty()
        return False
      if len(self.body_article['img']) > 10:
          self.body_article['img'] = self.body_article['img'][0:10]
      helper.resize_image(self.body_article['img'][0])
      time.sleep(5)
      if len(self.body_article['text']):
        print("Длина списка текста "+ str(len(self.body_article['text'])))
        pattern = re.compile(ur"[^(а-яА-Яa-zA-Z)]+", re.UNICODE)
        for i, txt in enumerate(self.body_article['text']):
           if re.sub(pattern, "", txt.strip()) == "":
              print("Пустые элементы текста "+str(i))
              del self.body_article["text"][i]
        print("Длина списка текста "+ str(len(self.body_article['text'])))
        #i = 0 ###########
        for txt in self.body_article['text']:
          self.remote_manager.check_stop()
          
          #i += 1 ###########
          #if i == 2:
          #  break
          time.sleep(1)
          txt = re.sub("\t+", "", "\n"+txt.strip()+"\n")
          txt = re.sub(ur"Увеличить картинку", "", txt)
          print(txt)
          script = "$('#main_col table').eq(0).append('<textarea id=my></textarea>');"
          script +=" var els = $('*');"
          script +=" els.keydown(function(evt){evt = evt || window.event; if (evt.keyCode == 13) {return false}});"
          self.driver.execute_script(script)
          self.driver.find_element_by_css_selector("#my").send_keys(txt)
          time.sleep(1)
          script = "$('.tinymce').val($('.tinymce').val()+$('#my').val());$('#my').remove()"
          self.driver.execute_script(script)
          time.sleep(1)
          try:
            self.remote_manager.check_stop()
            print(len(self.body_article['img']))
            self.body_article['img'][0]
            self.upload_image(self.body_article['img'][0])
            del self.body_article['img'][0]
          except:
            continue
      if len(self.body_article['img']):
        for img in self.body_article['img']:
          self.remote_manager.check_stop()
          self.upload_image(img)
      try:
        self.remote_manager.check_stop()
        self.driver.find_element_by_id("form_edit_article").find_element_by_css_selector("input[type=submit]").click()
        try:
          time.sleep(2)
          alert = self.driver.switch_to_alert()
          alert.accept()
          return False
        except:
          pass
      except:
        return False
      self.id_article = self.get_url().split('/')[-1].split('?')[0]
      print(self.id_article)
      return True
    else:
      return False

  def upload_image(self, img):
    self.mouse.move(Xm, Ym)
    time.sleep(2)
    self.mouse.click(Xm, Ym, 1)
    time.sleep(1)
    helper.press_down()
    time.sleep(2)
    helper.input_text(CURRENT_DIR+img)
    helper.press_enter()
    time.sleep(20)

  def set_parameters_article(self):
    self.remote_manager.check_stop()
    try:
      self.driver.get(self.get_url())
    except:
      return False
    name = self.body_article['name']
    self.driver.find_element_by_name("name").send_keys(name)
    self.driver.execute_script("String.prototype.capitalize = function() { return this.charAt(0).toUpperCase() + this.slice(1); }; var value = $('input[name=name]').val(); $('input[name=name]').val(value.toLowerCase().capitalize());")
    dropdown = Select(self.driver.find_element_by_name("article_category"))
    dropdown.select_by_index(int(self.body_article['id_theme'])-1)
    dropdown = Select(self.driver.find_element_by_name("link_rating"))
    dropdown.select_by_index(helper.pay_idx([int(self.config.get("cost_day_min")), int(self.config.get("cost_day_max"))], [int(self.config.get("cost_evening_min")), int(self.config.get("cost_evening_max"))]))
    self.remote_manager.check_stop()
    try:
      self.driver.find_element_by_css_selector(".edit_param").find_element_by_css_selector("input[type=submit]").click()
    except:
      return False
    return True

  def set_preview(self):
    self.remote_manager.check_stop()
    try:
      self.driver.get(self.get_url())
    except:
      return False
    if self.get_url() == "http://uh.ru/profile/article_user/"+self.id_article+"?edit=excision":
      list_elem = self.driver.find_elements_by_css_selector("a.image_insert")
      print("кол-во элементов image_insert " + str(len(list_elem)))
      if len(list_elem) == 0:
        return False
      elem = list_elem[random.randint(0, len(list_elem)-1)]
      elem.click()
      time.sleep(5)
      #self.driver.find_element_by_id("box").click()
      #self.driver.find_element_by_id("window").find_element_by_css_selector("input[type=submit]").click()
      self.remote_manager.check_stop()
      try:
        self.driver.execute_script("$('#window input[type=submit]').click()")
      except:
        return False
      return True
    else:
      return False

  def move_window(self, side="left"):
    if side == "left":
      self.driver.set_window_position(0, 0)
    else:
      self.driver.set_window_position(350, 0)

  def set_empty(self, type_oper="all"):
    if type_oper == "all":
      self.manager_module.check_data(self.body_article)
    self.id_article = None
    self.body_article = None
    
