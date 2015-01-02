# -*- coding: utf-8 -*-
from module_text import Module_Text
from db_connector import DbConnect
import random

class Module_Class(Module_Text):

  def set_section(self):
    print("set_section")
    random.shuffle(self.list_section)
    random.shuffle(self.list_section)
    for i in self.list_section:
      if i['id_theme'] == self.id_theme:
        return i["name"]

  def init_parse(self):
    Module_Text.init_parse(self)
    print("init_parse")
    self.pattern_page="/page/??num_page/" 
    self.selector_title=".w_news .w_hdr .w_tit h2 a"
    self.selector_content=".w_cnt .w_cntn"
    self.selector_img="img"
    self.count_img=10

list_section = [
 #{'name': "/girls", 'start_page': 105, 'id_theme': "3"},
 {'name': "/pictures", 'start_page': 405, 'id_theme': "3"},
 {'name': "/pictures/geo", 'start_page': 30, 'id_theme': "4"},
 {'name': "/jokes", 'start_page': 700, 'id_theme': "9"},
]

__name_module = "bugaga_ru"

__host = "bugaga.ru"

instance = Module_Class(DbConnect(), list_section, __name_module, __host,'' ,True, "www")  

if __name__ == '__main__':
  instance.section = '/jokes'

  print(instance.get_data("9"))