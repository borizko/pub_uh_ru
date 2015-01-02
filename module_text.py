# -*- coding: utf-8 -*-
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
import helper
from config import Config

class Module_Text:
  def __init__(self, db, list_section, name_module, host,charset="", mode_new=False, subdomen="", protocol="http://"):
    self.db = db
    self.list_section = list_section
    self.name_module = name_module
    self.host = host
    self.protocol = protocol
    self.mode_new = mode_new
    self.charset = charset
    self.min_image = 2
    self.section = None
    self.id_theme = None
    self.count_saved_articles = 0
    if subdomen:
      self.subdomen = subdomen+"."
    else:
      self.subdomen = subdomen
    print(subdomen)

  def get_name_app(self):
    return int(Config("App").get("computer_name"))

  def set_section(self):
    return self.list_section[random.randint(0, len(self.list_section)-1)]['name']

  def get_data(self, id_theme):
    print("Get Data")
    print("1")
    self.id_theme = id_theme
    self.section = self.set_section()
    print(self.section)
    sql = """SELECT id, name, text, url FROM articles WHERE module='%(module)s' AND used='0' AND section='%(section)s' AND computer_name=%(computer_name)i LIMIT 1"""% {'module': self.name_module, 'section': self.section, 'computer_name': self.get_name_app()}
    data = self.db.query(sql, "select")
    print('2')
    if not len(data):
      print("3")
      if not self.mode_new: 
        print("mode new false") 
        self.parse()

      else:
        self.get_parse_data()
      data = self.db.query(sql, "select")
      if not len(data):
        print("Len data =0")
        #self.set_page_less()
        return None
    print("4")
    text = self.split_text(data[0][2])[0:10]
    name = data[0][1]
    self.remember_article(data[0][0])
    img = self.parse_and_save_image(data[0][0])
    if len(img) < self.min_image:
      print(data[0][3])
      print(len(img))
      self.check_data({'id': data[0][0]})
      print("Check data")
      return None
    print("6")
    return {"id": data[0][0], "section": self.section, "name": name, "img": img, "text": text, "id_theme": id_theme}
    
  def parse_and_save_image(self, id_article):
    img = []
    sql = """SELECT url FROM images_article WHERE articles_id=%(id_article)i"""%{"id_article":id_article}
    for item in self.db.query(sql, 'select'):
      try:
        image_file = self.get_content(item[0], 'img')
        image_path = "images/" + item[0].split("/")[-1]
        f = open(image_path, "wb")
        f.write(image_file)
        f.close()
        img.append(image_path)
      except:
        continue
    return img

  def split_text(self, txt):
    text = []
    for item in txt.split("??img"):
      if item == "" or item == "\t" or item == "\n":
        continue
      text.append(item) 
    return text

  def check_data(self, check_dict={}):
    self.set_article_used(check_dict)
    sql = """DELETE FROM temp_table"""
    self.db.query(sql, "change")
    print("2389")
    

  def set_article_used(self, check_dict):
    print("234")
    sql = """SELECT path FROM images_article WHERE articles_id=%(id_article)i"""%{'id_article':check_dict["id"]}
    data = self.db.query(sql, 'select')
    sql = """DELETE FROM images_article WHERE articles_id=%(id_article)i"""%{'id_article':check_dict["id"]}
    self.db.query(sql, 'change')
    print("236")
    try:
      for item in check_dict["img"]:
        os.remove(item)
    except:
      print("234")
      pass
    sql = """UPDATE articles SET used='1' WHERE id=%(id_article)i"""%{'id_article':check_dict["id"]}
    self.db.query(sql, "change")

  def remember_article(self, id_article):
    sql = """INSERT IGNORE INTO temp_table(module, section, articles_id) VALUES('%(module)s', '%(section)s', %(id)i)"""%{'module': self.name_module,'section':self.section, 'id': id_article}
    self.db.query(sql, "change")

  def parse(self):
    print("Парсим")
    print("-----------------")
    self.count_saved_articles = 0
    num_page = int(self.get_page())
    if num_page > 1:
      url = self.protocol+self.subdomen+self.host+self.section+"/page/"+str(num_page)+'/'
    if num_page == 0:
      self.set_page_more()
      url = self.protocol+self.subdomen+self.host+self.section
    if num_page == 1:
      url = self.protocol+self.subdomen+self.host+self.section
    page = self.get_html(url)
    print("ПАйдж"+str(page))
    #ищем ссылки на все статьи
    list_link_articles = []
    if page:
      list_link_articles = page.cssselect("div.post h2.entry-title a")
    if len(list_link_articles):
      #собираем список из названий и url статей
      list_articles = []
      for link_articles in list_link_articles:
        list_articles.append({"name": link_articles.text.strip(), "url": self.create_absolute_url(link_articles.get("href"))})
      #заходим в каждую статью и парсим текст
      for article in list_articles:
        print("--------------")
        page = self.get_html(article['url'])
        for content in page.cssselect('div.entry-content'):
          img = []
          for i, image in enumerate(content.cssselect("img")):
            if i == 4:
              break;
            img.append(self.create_absolute_url(image.get("src")))
          for caption in content.cssselect("div.caption"):
            caption.getparent().remove(caption)
          pattern = re.compile('<img.*?>')
          list_text = pattern.split(tostring(content))
          text = fromstring("??img".join(list_text)).text_content()
          text = text.strip()
          articles_id = self.insert_article_in_db({"module":self.name_module, "section":self.section, "name": self.db.escape_string(article['name'].encode("utf-8")), "text": self.db.escape_string(text.encode("utf-8")), "url": article['url']})
          img_saved = []
          for i, image in enumerate(img):
            self.insert_image({"articles_id": articles_id, "url": image})
          self.count_saved_articles +=1
      self.set_page_less()
      print("Количество вставленных статей "+ str(self.count_saved_articles)) 
    else:
      self.set_page_less()
      print("Нет статей")
      return None

  def set_page_less(self):
    print("Set page less")
    sql = """UPDATE current_page_module SET page = page-1 WHERE module='%(module)s' AND section='%(section)s'"""%{"module": self.name_module, "section": self.section}
    self.db.query(sql, "change")

  def set_page_more(self):
    print("SET page more")
    sql = """UPDATE current_page_module SET page = page+1 WHERE module='%(module)s' AND section='%(section)s'"""%{"module": self.name_module, "section": self.section}
    self.db.query(sql, "change")

  def get_html(self, url):
    result = self.get_content(url)
    if result:
      return fromstring(result)
    else:
      return result

  def get_content(self, url, t_p='txt'):
    print(url)
    if not url.find(self.host) == -1:
      print(url.find(self.host))
      print(self.host)
      print(url)
      try:
        headers = {'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)'}
        req = urllib2.Request(url, None, headers)
        if t_p != 'txt':
          return urllib2.urlopen(req, timeout=10).read()
        if self.charset:
          return urllib2.urlopen(req, timeout=10).read().decode('utf-8', self.charset)
        else:
          return urllib2.urlopen(req, timeout=10).read()
      except:
        print("Ошибка при парсинге")
        return None
    else:
      print("Не тот хост")
      return None

  def get_page_from_list_section(self):
    for item in self.list_section:
      if item['name'] == self.section:
        return item['start_page']

  def get_page(self):
    sql = """SELECT page FROM current_page_module WHERE module='%(module)s' AND section='%(section)s' LIMIT 1"""%{'module': self.name_module, 'section':self.section}
    data = self.db.query(sql, 'select')
    page = None
    for item in data:
      page = item[0]
    if page == None:
      page = self.get_page_from_list_section()
      sql = """INSERT IGNORE INTO current_page_module(module, section, page) VALUES('%(module)s', '%(section)s', %(page)i)"""%{'module': self.name_module, 'section':self.section, 'page': page}
      self.db.query(sql, 'change')
    return page

  def create_absolute_url(self, url):
    if url.find("http://") > -1:
      return url
    if url.find("/") == 0:
      return self.protocol+self.subdomen+self.host+url
    else:
      return self.protocol+self.subdomen+self.host + self.section + "/" + url

  def insert_article_in_db(self, article={}):
    article.update({"computer_name": self.get_name_app()})
    sql = """INSERT IGNORE INTO articles(module, section, name, text, url, computer_name) VALUES('%(module)s', '%(section)s', '%(name)s', '%(text)s', '%(url)s', %(computer_name)i)""" % article
    #print(sql)
    self.db.query(sql, "change")
    sql = """SELECT id FROM articles WHERE url = '%(url)s'"""%{"url": article['url']}
    data = self.db.query(sql, "select")
    return data[0][0]

  def insert_image(self, image={}):
    sql = """INSERT IGNORE INTO images_article(articles_id, url) VALUES(%(articles_id)i, '%(url)s')""" % image
    #print(sql)
    self.db.query(sql, 'change')

  def db_open(self):
    self.db.open()

  def db_close(self):
    self.db.close()


#methods for new parser
  def get_parse_data(self):
    print("Парсим")
    print("-----------------")
    self.count_saved_articles = 0
    self.init_parse()
    url = self.get_url_parse()
    if not url:
      print(1)
      return None
    list_link_articles = []
    #ищем ссылки на все статьи
    list_link_articles = self.get_list_link_articles(url) 
    if len(list_link_articles):
      list_articles = self.get_list_articles(list_link_articles)
      for article in list_articles:
        print("----------")
        for content in self.get_article_content(article['url']):
          content = self.remove_elements(content)
          img = self.get_list_image(content)
          if len(img) <= 1:
            continue
          content = self.strip_tags(content)
          text = self.get_text(content) 
          self.save_image(
            img, 
            self.insert_article_in_db({"module":self.name_module, "section":self.section, "name": self.db.escape_string(article['name'].encode("utf-8")), "text": self.db.escape_string(text.encode("utf-8")), "url": article['url']})
          )
        self.count_saved_articles +=1
      self.set_page_less() 
      print("Количество вставленных статей "+ str(self.count_saved_articles)) 
      return True
    else:
      self.set_page_less()
      print(3)
      return None


  def get_elements_from_url(self, url, selector_links):
    page = self.get_html(url)
    print("ПАйдж"+str(page))
    #ищем ссылки на все статьи
    if page:
      return page.cssselect(selector_links)
    else:
      return []

  def get_list_articles(self, list_link):
    list_articles = []
    for link_articles in list_link:
      title = self.handle_title_article(link_articles.text)
      list_articles.append({"name": title.strip(), "url": self.create_absolute_url(link_articles.get("href"))})
    return list_articles

  def get_list_img_from_content(self, content, selector="img", count_image=6):
    img = []
    if type(selector) == type([]):
      i = 0
      for sel in selector: 
        for image in content.cssselect(sel):
          if i == count_image:
            break;
          img.append(self.create_absolute_url(image.get("src")))
          i += 1
    else:
      for i, image in enumerate(content.cssselect(selector)):
        if i == count_image:
          break;
        img.append(self.create_absolute_url(image.get("src")))
    return img

  def get_text_from_content(self, content):
    pattern = re.compile('<img.*?>')
    list_text = pattern.split(tostring(content))
    text = fromstring("??img".join(list_text)).text_content()
    text = text.strip()
    #Удаляем комментарии
    text = re.sub(r"<[\w\W]+?>", "", text).strip()
    return text

  def save_image(self, img, articles_id):
    print("Количесво изо"+ str(len(img)))
    for i, image in enumerate(img):
      self.insert_image({"articles_id": articles_id, "url": image})


  def get_url_parse_from_pattern(self, pattern):
    num_page = self.get_page()
    if num_page > 1:
      pattern = pattern.split("??num_page")
      string = "" 
      for i, item in enumerate(pattern):
        if i == len(pattern)-1:
          string += item
          break
        string += item + str(num_page)
      return self.protocol+self.subdomen+self.host+self.section+string
    if num_page == 0:
      self.set_page_more()
      return self.protocol+self.subdomen+self.host+self.section
    if num_page == 1:
      return self.protocol+self.subdomen+self.host+self.section


#Публичные методы для переопеределения
  def get_url_parse(self):
    pattern = self.pattern_page
    return self.get_url_parse_from_pattern(pattern)

  def get_text(self, content):
    text = self.get_text_from_content(content)
    text = re.sub(ur"Увеличить картинку", "", text)
    return text


  def strip_tags(self, content):
    content_text = re.sub('</{0,1}p>', "\n", tostring(content))
    content_text = re.sub('</{0,1}br>', "\n", content_text)
    content_text = re.sub('</{0,1}h\d{0, 1}>', "\n", content_text)
    return fromstring(content_text)

  def get_list_image(self, content):
    selector=self.selector_img
    count_image=self.count_img
    return self.get_list_img_from_content(content, selector, count_image)

  def get_article_content(self, url):
    selector = self.selector_content
    return  self.get_elements_from_url(url, selector)

  def get_list_link_articles(self, url):
    selector= self.selector_title
    print("Селектор title"+selector)
    return self.get_elements_from_url(url, selector)


  def handle_title_article(self, txt):
    title = re.sub("\([\w\W\d]*?\)", "", txt)
    return title

  def init_parse(self):
    self.pattern_page="/page/??num_page" 
    self.selector_title=""
    self.selector_content=""
    self.selector_img=""
    self.count_img=6
    self.remove_selectors = [] #[{'selector':, 'type':self|parent}]

  def remove_elements(self, content):
    for sel in self.remove_selectors:
      if not sel.get("type", None) or sel.get("type", None) == 'self':
        for el in content.cssselect(sel['selector']):
          el.getparent().remove(el)
      else:
        for el in content.cssselect(sel['selector']):
          el.getparent().getparent().remove(el.getparent())
    return content


