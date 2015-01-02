# -*- coding: utf-8 -*-
import random
import helper

class Manager_Module:

  def __init__(self):
    self.list_module = {
      "1": {"id":1, "modules": [], "used": 0}, # Вещи
      "2": {"id":2, "modules": [], "used": 0}, # Животные, Природа
      "3": {"id":3, "modules": [], "used": 0}, # Люди, Общество
      "4": {"id":4, "modules": [], "used": 0}, # Места, Глобальное
      "5": {"id":5, "modules": [], "used": 0}, # События, Происшествия
      "6": {"id":6, "modules": [], "used": 0}, # Техника, Технологии
      "7": {"id":7, "modules": [], "used": 0}, # Бизнес
      "8": {"id":8, "modules": [], "used": 0}, # Непознанное
      "9": {"id":9, "modules": [], "used": 0}, # Юмор
    }
    self.module = None
    self.module_name = None

  def load_list_modules(self):
    for item in self.list_module:
      self.list_module[item]["modules"] = []
    with  open("settings/modules/list_modules.csv") as f:
      for line in f:
        if line[0] == "#":
          continue
        module_name = line.rstrip()
        if module_name == "":
          continue
        module = __import__(module_name)
        list_theme = []
        for item in module.list_section:
          if not item["id_theme"] in list_theme:
            list_theme.append(item["id_theme"])
        for item in list_theme:
          self.list_module[item]["modules"].append(module_name)
   # helper.debug([self.list_module])


  def get_data(self, id_theme):
    self.load_list_modules()
    try:
      if len(self.list_module[id_theme]["modules"]):
        self.module_name = self.get_module(str(id_theme))
        print("Имя модуля "+self.module_name)
        self.module = __import__(self.module_name)
        if self.module_name == "demotivators_to":
          self.module.db.open()
          return self.module.get_data(id_theme)
        else:
          self.module.instance.db_open()
          return self.module.instance.get_data(id_theme)
      else:
        return None
    except:
      print("Error load module")
      return None

  def get_module(self, id_theme):
    return self.list_module[id_theme]['modules'][random.randint(0, len(self.list_module[id_theme]['modules'])-1)]

  def check_data(self, check_dict={}):
    if self.module_name == "demotivators_to":
      self.module.check_data(check_dict)
      self.module.db.close()
    else:
      self.module.instance.check_data(check_dict)
      self.module.instance.db_close()

if __name__ == '__main__':
  
  Manager_Module().load_list_modules()
