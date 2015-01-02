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
    self.selector_title=".post_head h2 a"
    self.selector_content="article .post_info div[id^='news-']"
    self.selector_img="img[src$='.jpg']"
    self.count_img=10
    self.remove_selectors = [{"selector": "span.counter", "type":"self"}]

list_section = [
 {'name': "/girls", 'start_page': 25, 'id_theme': "9"},
 {'name': "/photo-prikol", 'start_page': 84, 'id_theme': "9"},
 {'name': "/prikoli", 'start_page': 110, 'id_theme': "9"},
 {'name': "/pictures_photo", 'start_page': 159, 'id_theme': "9"},
 {'name': "/it-is-interesting", 'start_page': 40, 'id_theme': "9"},
 {'name': "/animals", 'start_page': 39, 'id_theme': "2"},
 {'name': "/karikatury-komiksy", 'start_page': 12, 'id_theme': "9"},
]

__name_module = "porjati_ru"

__host = "porjati.ru"

instance = Module_Class(DbConnect(), list_section, __name_module, __host,'' ,True, "www")  

if __name__ == '__main__':
  instance.section = '/jokes'

  print(instance.get_data("9"))