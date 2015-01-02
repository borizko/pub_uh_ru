# -*- coding: utf-8 -*-
from module_text import Module_Text
from db_connector import DbConnect
import re

class Zoopicture_ru(Module_Text):
  pass

list_section =[
 {'name': "/category/dog", 'start_page': 31, 'id_theme': "2"},
 {'name': "/category/cat", 'start_page': 33, 'id_theme': "2"},
 {'name': "/category/big-cat", 'start_page': 29, 'id_theme': "2"},
 {'name': "/category/birds", 'start_page': 36, 'id_theme': "2"},
 {'name': "/category/bear", 'start_page': 10, 'id_theme': "2"},
 {'name': "/category/primates", 'start_page': 22, 'id_theme': "2"},
 {'name': "/category/rodentia", 'start_page': 15, 'id_theme': "2"},
 {'name': "/category/reptilia", 'start_page': 18, 'id_theme': "2"},
 {'name': "/category/amphibia", 'start_page': 9, 'id_theme': "2"},
 {'name': "/category/insects", 'start_page': 22, 'id_theme': "2"},
 {'name': "/category/water", 'start_page': 38, 'id_theme': "2"},
 {'name': "/category/animal", 'start_page': 78, 'id_theme': "2"},
]

__name_module = "zoopicture_ru"

__host = "zoopicture.ru"

instance = Zoopicture_ru(DbConnect(), list_section, __name_module, __host, 'latin-1' )  
instance.min_image = 2
if __name__ == '__main__':
  print(instance.get_data(1))



