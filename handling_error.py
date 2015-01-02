# -*- coding: utf-8 -*-
import config
import time
import helper
import observer

class Handling_Error:

  def __init__(self):
    self.config = config.Config(self.__class__.__name__)
    self.count_error = 0

  def set_timeout(self, list_pub, list_voit, clicker):
    observer.instance.set_status("3")
    start = time.time()
    i = 0
    while time.time() - start < int(self.config.get("timeout"))*60:
      print("Full Error! Wait! " + str(int(self.config.get("timeout"))*60-(time.time()-start))+ " сек.")
      if i%15 == 0:
        try:
          for obj in list_voit:
            obj.refresh()
          for obj in self.list_pub:
            obj.refresh()
          clicker.refresh()
        except:
          pass
      i += 1
      helper.move_mouse()
      time.sleep(5)

  def is_full(self, list_pub, list_voit, clicker):
    if self.count_error == int(self.config.get("count_error")):
      self.set_timeout(list_pub, list_voit, clicker)
      self.count_error = 0
      return True
    return False

  def get_count_error(self):
    return self.count_error

  def add_count_error(self):
    self.count_error = self.count_error + 1

  def remove_count_error(self, mode="all"):
    if self.count_error == 0:
      return
    if mode == "one":
      self.count_error = self.count_error - 1
    elif mode == "all":
      self.count_error = 0