# -*- coding: utf-8 -*-
import time
from uh_ru import Uh_ru

class Clicker(Uh_ru):
  def __init__(self, timer):
    Uh_ru.__init__(self)
    self.timer = timer
    self.start_timer = 0


  def get_page_article(self, id_article):
    try:
      self.driver.get("http://uh.ru/a/"+id_article)
    except:
      return False
    return True

  def clicking(self, id_article):
    if (time.time() - self.start_timer)/60 >= self.timer:
      print("Clicking ...")
      self.get_page_article(id_article)
      i=0

      while len(self.driver.find_elements_by_css_selector(".points_link a")) > 0:
        i += 1
        list_a = self.driver.find_elements_by_css_selector(".points_link a")
        time.sleep(5)
        try:
          list_a[0].click()
        except:
          pass
        current_window = self.driver.current_window_handle
        list_windows = self.driver.window_handles
        for handle in list_windows:
          if handle != current_window:
            time.sleep(4)
            self.driver.close()
            self.driver.switch_to_window(handle)
            break
        print(len(self.driver.find_elements_by_css_selector(".points_link a")))
        print(i)
      self.start_timer = time.time()
    return True

    def find_links(self):
      return self.driver.find_elements_by_css_selector(".points_link a")