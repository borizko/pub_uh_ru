# -*- coding: utf-8 -*-
from publisher import Publisher
from facebook import Facebook
from manager_module import Manager_Module
from voiter import Voiter
from clicker import Clicker
import time
import random
import helper
import config
import sys
import observer

class Worker:

  def __init__(self):
    self.list_obj_pub = []
    self.list_obj_voit = []
    self.obj_clicker = None
    self.config = config.Config(self.__class__.__name__)
    self.obj_facebook = None

  def error_reaction(self, obj_pub):
    print("Ошибка")
    print("-------------------------") 
    obj_pub.set_empty("var")
    return False

  def work(self, list_theme):
    print("Создаем статью")
    self.all_refresh()
    #self.obj_facebook.refresh()
    for obj_pub in self.list_obj_pub:
      observer.instance.set_status("2")
      id_theme = list_theme[random.randint(0, len(list_theme)-1)]
      if obj_pub.get_body_article(id_theme):
        self.all_refresh()
        print("Модуль "+obj_pub.manager_module.module_name+" секция "+obj_pub.manager_module.module.instance.section)
        obj_pub.get_page_create_article()
        helper.move_screen()
        obj_pub.move_window()
        if obj_pub.create_body_article():
          helper.move_screen('left')
          obj_pub.move_window('right')
          self.all_refresh()
          if obj_pub.set_parameters_article():
            if obj_pub.set_preview():
              for obj in self.list_obj_voit:
                #obj.get_page_article(obj_pub)
                obj.voiting(obj_pub)
                #obj.voiting_down()
              #self.obj_facebook.publish(obj_pub)
              obj_pub.set_empty()
              print('Успешно опубликовано!!!')
              print('-------------------------')
            else:
              print("Ошибка установки превью статьи")
              return self.error_reaction(obj_pub)
          else:
            print("Ошибка установки параметров")
            return self.error_reaction(obj_pub)
        else:
          print("Ошибка создания тела статьи !!")
          helper.move_screen('left')
          obj_pub.move_window('right')
          return self.error_reaction(obj_pub)
      else:
        #print("Модуль "+obj_pub.manager_module.module_name+" секция "+obj_pub.manager_module.module.instance.section+" не вернул данные")
        #self.log(u"Модуль "+ obj_pub.manager_module.module_name+u" секция "+obj_pub.manager_module.module.instance.section+u" не вернул данные")
        return self.error_reaction(obj_pub)
    return True
    
  def log(self, txt):
    with open("log/log.txt") as f:
      string = f.read()
    with open("log/log.txt", "w") as f:
      f.write(string+txt.encode("utf-8")+"\n")

  def start_work(self, list_pub=[], list_voit=[], clicker=None, facebook=None):
    for obj_voit in list_voit:
      obj = Voiter()
      self.list_obj_voit.append(obj)
      obj.start_work(obj_voit["login"], obj_voit["pass"])
    for obj_pub in list_pub:
      obj = Publisher(Manager_Module())
      self.list_obj_pub.append(obj)
      obj.start_work(obj_pub["login"], obj_pub["pass"])
    self.obj_clicker = Clicker(60)
    self.obj_clicker.start_work(clicker["login"], clicker["pass"])
    #self.obj_facebook = Facebook()
    #self.obj_facebook.start_work()



  def timeout(self):
    start = time.time()
    observer.instance.set_status("4")
    i = 0
    time_walk = random.randint(int(self.config.get('walk_min')), int(self.config.get('walk_max')))
    self.config.set('walk', str(time_walk))
    while time.time() - start < int(self.config.get('walk'))*60:
      print("Осталось: " + str(int(self.config.get('walk'))*60 - (time.time() - start)) + " сек.")
      print("-")
      if i%15 == 0:
        try:
          self.all_refresh()
        except:
          pass
      helper.move_mouse()
      time.sleep(5)
      i += 1

  def add_count_article(self):
    for obj in self.list_obj_pub:
      obj.count_article += 1

  def set_empty_count_article(self):
    for obj in self.list_obj_pub:
      obj.count_article = 0


  def all_refresh(self):
    for obj in self.list_obj_voit:
      try:
        obj.refresh()
      except:
        pass
    for obj in self.list_obj_pub:
      try:
        obj.refresh()
      except:
        pass
    try:
      self.obj_clicker.refresh()
    except:
      pass
    #self.obj_facebook.refresh()

  def stop(self):
    for obj in self.list_obj_voit:
      try:
        obj.driver.close()
      except:
        pass
    for obj in self.list_obj_pub:
      try:
        obj.driver.close()
      except:
        pass
    try:
      self.obj_clicker.driver.close()
    except:
      pass
