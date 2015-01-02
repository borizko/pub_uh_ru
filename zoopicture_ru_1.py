# -*- coding: utf-8 -*-
from db_connector import DbConnect
import random
import subprocess
import sys
import helper
from lxml.html import parse
from lxml.html import fromstring, tostring
import lxml
import urllib2
import re
import os

db = DbConnect()

NAME_MODULE = "zoopicture_ru"
HOST = "http://www.zoopicture.ru"
list_section =[
 {'name': "/category/dog", 'start_page': 31},
 {'name': "/category/cat", 'start_page': 33},
 {'name': "/category/big-cat", 'start_page': 29},
 {'name': "/category/birds", 'start_page': 36},
 {'name': "/category/bear", 'start_page': 10},
 {'name': "/category/primates", 'start_page': 22},
 {'name': "/category/rodentia", 'start_page': 15},
 {'name': "/category/reptilia", 'start_page': 18},
 {'name': "/category/amphibia", 'start_page': 9},
 {'name': "/category/insects", 'start_page': 22},
 {'name': "/category/water", 'start_page': 38},
 {'name': "/category/animal", 'start_page': 78},
]
def get_data(id_theme):
  section = list_section[random.randint(0, len(list_section)-1)]['name']
  print(section)
  sql = """SELECT id, name, text FROM articles WHERE module='%(module)s' AND used='0' AND section='%(section)s' LIMIT 1"""% {'module': NAME_MODULE, 'section': section}
  data = db.query(sql, "select")
  if not len(data):
    parse(section)
    data = db.query(sql, "select")
    if not len(data):
      return None
  text = split_text(data[0][2])
  name = data[0][1]
  remember_article(data[0][0], section)
  img = []
  sql = """SELECT path FROM images_article WHERE articles_id=%(articles_id)i"""%{"articles_id": data[0][0]}
  for item in db.query(sql, 'select'):
    img.append(item[0])
  return {"id": data[0][0], "section": section, "name": name, "img": img, "text": text, "id_theme": id_theme}


def split_text(txt):
  return txt.split("??img")

def check_data(check_dict={}):
  set_article_used(check_dict['id'])
  sql = """DELETE FROM temp_table"""
  db.query(sql, "change")
  sql = """UPDATE current_page_module SET page = page-1 WHERE module='%(module)s' AND section='%(section)s'"""%{"module": NAME_MODULE, "section": check_dict['section']}
  db.query(sql, "change")

def set_article_used(id_article):
  sql = """SELECT path FROM images_article WHERE articles_id=%(id_article)i"""%{'id_article':id_article}
  data = db.query(sql, 'select')
  sql = """DELETE FROM images_article WHERE articles_id=%(id_article)i"""%{'id_article':id_article}
  db.query(sql, 'change')
  for item in data:
    os.remove(item[0])
  sql = """UPDATE articles SET used='1' WHERE id=%(id_article)i"""%{'id_article':id_article}
  db.query(sql, "change")

def remember_article(id_article, section):
  sql = """INSERT IGNORE INTO temp_table(module, section, articles_id) VALUES('%(module)s', '%(section)s', %(id)i)"""%{'module':NAME_MODULE,'section':section, 'id': id_article}
  db.query(sql, "change")

def parse(section):
  num_page = get_page(section)
  if num_page > 1:
    url = HOST+section+"/page/"+str(num_page)+'/'
  if num_page == 0:
    return
  if num_page == 1:
    url = HOST+section
  page = get_html(url)
  #ищем ссылки на все статьи
  list_link_articles = []
  list_link_articles = page.cssselect("div.post h2.entry-title a")
  if len(list_link_articles):
    #собираем список из названий и url статей
    list_articles = []
    for link_articles in list_link_articles:
      list_articles.append({"name": link_articles.text.strip(), "url": create_absolute_url(link_articles.get("href"))})
    #заходим в каждую статью и парсим текст
    for article in list_articles:
      page = get_html(article['url'])
      for content in page.cssselect('div.entry-content'):
        img = []
        for i, image in enumerate(content.cssselect("img")):
          if i == 4:
            break;
          img.append(create_absolute_url(image.get("src")))
        for caption in content.cssselect("div.caption"):
          caption.getparent().remove(caption)
        pattern = re.compile('<img.*?>')
        list_text = pattern.split(tostring(content))
        text = fromstring("??img".join(list_text)).text_content()
        text = text.strip()
        articles_id = insert_article_in_db({"module":NAME_MODULE, "section":section, "name": article['name'], "text": text, "url": article['url']})
        for i, image in enumerate(img):
          #print(image)
          image_file = get_content(image)
          image_path = "images/" + image.split("/")[-1]
          f = open(image_path, "wb")
          f.write(image_file)
          f.close()
          if not i:
            helper.resize_image(image_path)
          insert_image({"articles_id": articles_id, "path": image_path})
  else:
    return None

def get_html(url):
  return fromstring(get_content(url))

def get_content(url):
  headers = {'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)'}
  req = urllib2.Request(url, None, headers)
  return urllib2.urlopen(req).read()

def get_page_from_list_section(section):
  for item in list_section:
    if item['name'] == section:
      return item['start_page']

def get_page(section):
  sql = """SELECT page FROM current_page_module WHERE module='%(module)s' AND section='%(section)s' LIMIT 1"""%{'module': NAME_MODULE, 'section':section}
  data = db.query(sql, 'select')
  page = None
  for item in data:
    page = item[0]
  if page == None:
    page = get_page_from_list_section(section)
    sql = """INSERT IGNORE INTO current_page_module(module, section, page) VALUES('%(module)s', '%(section)s', %(page)i)"""%{'module': NAME_MODULE, 'section':section, 'page': page}
    db.query(sql, 'change')
  return page

def create_absolute_url(url):
  if url.find(HOST) > -1:
    return url
  if url.find("/") == 0:
    return HOST+url
  else:
    return HOST + section + "/" + url

def insert_article_in_db(article={}):
  sql = """INSERT IGNORE INTO articles(module, section, name, text, url) VALUES('%(module)s', '%(section)s', '%(name)s', '%(text)s', '%(url)s')""" % article
  db.query(sql, "change")
  sql = """SELECT id FROM articles WHERE name = '%(name)s'"""%{"name": article['name']}
  data = db.query(sql, "select")
  return data[0][0]

def insert_image(image={}):
  sql = """INSERT IGNORE INTO images_article(articles_id, path) VALUES(%(articles_id)i, '%(path)s')""" % image
  #print(sql)
  db.query(sql, 'change')

if __name__ == "__main__":
  #print(get_data("1"))
  parse("/category/dog")