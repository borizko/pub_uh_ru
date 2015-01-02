# -*- coding: utf-8 -*-
from db_connector import DbConnect
import random
import subprocess
import sys
import os

COUNT_UPLOAD = 3
db = DbConnect()
class obj:
  def __init__(self):
    self.section = "/"

instance = obj()

list_section =[
 {'name': "/", 'start_page': 10, 'id_theme': "9"},
]

def get_data(id_theme):
  sql = """SELECT id, name, path FROM demotivators WHERE used='%(used)s' and name is not NULL and path is not null LIMIT %(count)i"""%({"used":'0', "count": COUNT_UPLOAD})
  print(sql)
  data = db.query(sql, "select")
  print(len(data))
  if not len(data) == COUNT_UPLOAD:
    parse()
    data = db.query(sql, "select")
    if not len(data) == COUNT_UPLOAD:
      return None
  text = []
  img = []
  name = ""
  for dem in data:
    img.append(dem[2])
  name = data[random.randint(0, len(data)-1)][1]
  remember_demotivators(data)
  #print {"name": name, "img": img, "text": [], "id_theme": id_theme}
  #sys.exit()
  return {"name": name, "img": img, "text": [], "id_theme": id_theme}


def check_data(check_dict={}):
  sql = """SELECT id_dem FROM temp_demotivators_to"""
  data = db.query(sql, "select")
  for dem in data:
    set_demotivators_used(dem[0])
  sql = """DELETE FROM temp_demotivators_to"""
  db.query(sql, "change")

def parse():
  db.close()
  batcmd='python parse_demotivators.to.py'
  subprocess.check_output(batcmd, shell=True)
  db.open()

def remember_demotivators(data):
  sql = """INSERT IGNORE INTO temp_demotivators_to(id_dem) VALUES"""
  for i, dem in enumerate(data):
    if i == len(data)-1:
      sql += "("+str(dem[0])+")"
    else:
      sql += "("+str(dem[0])+"), "
  db.query(sql, "change")  

def set_demotivators_used(id_dem):
  sql = """SELECT path FROM demotivators WHERE id=%(id_dem)i LIMIT 1"""%{'id_dem': id_dem}
  data = db.query(sql, 'select')
  for item in data:
    os.remove(item[0]);
  sql = """UPDATE demotivators SET used=%(used)i WHERE id=%(id)i"""%({"used": 1, "id": id_dem})
  db.query(sql, "change")

if __name__ == '__main__':
  print("12434")
  print(get_data("9"))