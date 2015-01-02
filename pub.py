# -*- coding: utf-8 -*-
from worker import Worker
import helper
import random
from config import Config
import handling_error
import observer
import traceback

all_list_theme = [
      "1", # Вещи
      "2", # Животные, Природа
      "3", # Люди, Общество
      "4", # Места, Глобальное
      "5", # События, Происшествия
      "6", # Техника, Технологии
      "7", # Бизнес
      "8", # Непознанное
      "9", # Юмор
]
def get_list_theme():
  list_theme = []
  for line in open("settings/themes/list_theme.csv"):
    list_theme = line.split(";")
  return list_theme

def get_pub_users():
  list_pub = []
  for line in open("settings/publish/pub_users.csv"):
    if line[0] == "#":
      continue
    list_pub.append({"login": line.split(";")[0], "pass": line.split(";")[1].rstrip()})
  return list_pub

def get_clicker():
  for line in open("settings/publish/pub_users.csv"):
    if line[0] == "#":
      continue
    if line.split(";")[2].strip() == "clicker":
      print(1)
      return {"login":line.split(";")[0], "pass": line.split(";")[1]}



worker = Worker()

list_voit = [
  {"login": "alexko-z", "pass": "123456ty"},
  #{"login": "stepan86", "pass": "stepanok123ewrtQW"},
  {"login": "sanya1994", "pass": "sanek346rTYPost"},
  #{"login": "vasyk-siniy", "pass": "fahrteERu309"},
  #{"login": "demon-petrov", "pass": "SRWQskoey$^821367"}
]
handle_err = handling_error.Handling_Error()
config = Config("Pub")
publish = config.get("with_publish")
print(publish)
list_pub = get_pub_users()
print(list_pub)
clicker = get_clicker()
helper.move_screen()
worker.start_work(list_pub, list_voit, clicker)
helper.move_screen('left')
try:
  while True:
    from worker import Worker
    list_theme = get_list_theme()
    is_full = False
    random.shuffle(list_theme)
    random.shuffle(list_theme)
    print(list_theme[0])
    worker.set_empty_count_article()
    if publish == "on":
      while worker.list_obj_pub[0].count_article != int(config.get("count_publish")):
        print("Count error: "+ str(handle_err.get_count_error()))
        worker.all_refresh()
        if worker.work(list_theme):
          handle_err.remove_count_error("one")
          worker.add_count_article()
        else:
          handle_err.add_count_error()
          is_full = handle_err.is_full(list_pub, list_voit, clicker)
          if is_full:
            break
      if is_full:
        continue
    else:
      publish = "on"
      
    #worker.obj_clicker.clicking('1719283')
    worker.timeout()
except Exception as err:
  print(err)
  traceback.print_exc()
  worker.stop()
  observer.instance.set_status("1")
  

