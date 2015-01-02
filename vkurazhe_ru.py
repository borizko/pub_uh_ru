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
    self.remove_selectors = [
      {"selector": "h4", "type":"self"},
      {"selector": "h1", "type":"self"},
      {"selector": "h2", "type":"self"},
      {"selector": "h3", "type":"self"},
      {"selector": "script", "type":"self"},
      {"selector": "noscript", "type":"self"},
      {"selector": "#disqus_thread", "type":"self"},
      {"selector": ".news_info_morenews", "type":"self"},
      {"selector": "table", "type":"self"},
      {"selector": "ins", "type":"parent"},

    ]
    self.pattern_page="/?&p=??num_page" 
    self.selector_title="#content ul.cnt li h1 a"
    self.selector_content="#content"
    self.selector_img=["img[src$='.jpg']", "img[src$='.png']", "img[src$='.jpeg']"]
    self.count_img=10



list_section = [
 {'name': "/other", 'start_page': 42, 'id_theme': "9"},
 {'name': "/animals", 'start_page': 10, 'id_theme': "2"},
 #{'name': "/girls", 'start_page': 5, 'id_theme': "3"},
 #{'name': "/girls", 'start_page': 5, 'id_theme': "2"},
 {'name': "/positiff", 'start_page': 4, 'id_theme': "5"},
 {'name': "/creatiff", 'start_page': 6, 'id_theme': "9"},
 {'name': "/foto", 'start_page': 34, 'id_theme': "9"},
]

__name_module = "vkurazhe_ru"

__host = "vkurazhe.ru"

instance = Module_Class(DbConnect(), list_section, __name_module, __host,'' ,True)  

if __name__ == '__main__':
  instance.section = '/other'

  print(instance.get_data("9"))