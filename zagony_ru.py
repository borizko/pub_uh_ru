# -*- coding: utf-8 -*-
from module_text import Module_Text
from db_connector import DbConnect
import random
import helper

class Module_Class(Module_Text):

  def set_section(self):
    random.shuffle(self.list_section)
    random.shuffle(self.list_section)
    for i in self.list_section:
      if i['id_theme'] == self.id_theme:
        return i["name"]

  def init_parse(self):
    Module_Text.init_parse(self)
    self.pattern_page="/page/??num_page/" 
    self.selector_title="#dle-content .short h2 a"
    self.selector_content="#dle-content .short .short1 .short2 .short3 .short18"
    self.selector_img=["img[src$='.jpg']", "img[src$='.jpeg']", "img[src$='.png']"]
    self.count_img=10



list_section = [
 {'name': "/girls", 'start_page': 132, 'id_theme': "3"},
 {'name': "/girls", 'start_page': 132, 'id_theme': "9"},
]

__name_module = "zagony_ru"

__host = "zagony.ru"

instance = Module_Class(DbConnect(), list_section, __name_module, __host, '',True)  

if __name__ == '__main__':
  instance.section = '/girls'

  print(instance.get_data("3"))