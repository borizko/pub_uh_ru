# -*- coding: utf-8 -*-
from module_text import Module_Text
from db_connector import DbConnect
from lxml.html import parse
from lxml.html import fromstring, tostring
import lxml
import sys
import re
import random

class Billionnews_ru(Module_Text):
  def set_section(self):
    random.shuffle(self.list_section)
    for i in self.list_section:
      if i['id_theme'] == self.id_theme:
        return i["name"]


  def parse(self):
    num_page = self.get_page()
    if num_page > 1:
      url = self.protocol+self.host+self.section+"/page/"+str(num_page)
    if num_page == 0:
      self.set_page_more()
      url = self.protocol+self.subdomen+self.host+self.section
    if num_page == 1:
      url = self.protocol+self.host+self.section
    page = self.get_html(url)
    #ищем ссылки на все статьи
    list_link_articles = []
    list_link_articles = page.cssselect("div.news div.news_h h2 a")
    if len(list_link_articles):
      #собираем список из названий и url статей
      list_articles = []
      for link_articles in list_link_articles:
        title = re.sub("\([\w\W\d]*?\)", "", link_articles.text.strip())
        list_articles.append({"name": title, "url": self.create_absolute_url(link_articles.get("href"))})
      #заходим в каждую статью и парсим текст
      for article in list_articles:
        print("Парсим статью")
        page = self.get_html(article['url'])
        for content in page.cssselect('div.news_t'):
          #парсим изображения
          img = []
          for i, image in enumerate(content.cssselect("img[src$='.jpg']")):
            if i == 6:
              break;
            img.append(self.create_absolute_url(image.get("src")))
          content_text = re.sub('</{0,1}p>', "\n", tostring(content))
          content_text = re.sub('</{0,1}br>', "\n", content_text)
          #open("text.txt", "w").write(content_text.encode("utf-8", "windows-1251"))
          #sys.exit()
          content_text = re.sub('</{0,1}h\d{0, 1}>', "\n", content_text)
          content = fromstring(content_text)
          pattern = re.compile('<img.*?>')
          list_text = pattern.split(tostring(content))
          text = fromstring("??img".join(list_text)).text_content()
          text = text.strip()
          #Удаляем комментарии
          text = re.sub(r"<[\w\W]+?>", "", text).strip()
          articles_id = self.insert_article_in_db({"module":self.name_module, "section":self.section, "name": self.db.escape_string(article['name'].encode("utf-8")), "text": self.db.escape_string(text.encode("utf-8")), "url": article['url']})
          for i, image in enumerate(img):
            self.insert_image({"articles_id": articles_id, "url": image})
        self.count_saved_articles +=1
      self.set_page_less() 
      print("Количество вставленных статей "+ str(self.count_saved_articles)) 
    else:
      print("Нет статей")
      return None


list_section =[
 {'name': "/travel", 'start_page': 10, 'id_theme': "4"},
 {'name': "/animal", 'start_page': 9, 'id_theme': "2"},
 {'name': "/transport", 'start_page': 9, 'id_theme': "6"},
 {'name': "/tehnika", 'start_page': 9, 'id_theme': "6"},
 {'name': "/lud", 'start_page': 6, 'id_theme': "3"},
 #{'name': "/znam", 'start_page': 3, 'id_theme': "3"},
 #{'name': "/nepoznat", 'start_page': 5, 'id_theme': "8"},
 {'name': "/naci", 'start_page': 7, 'id_theme': "3"},
 #{'name': "/dorogo", 'start_page': 4, 'id_theme': "1"},
]

__name_module = "billionnews_ru"

__host = "billionnews.ru"

instance = Billionnews_ru(DbConnect(), list_section, __name_module, __host, '' )  

if __name__ == '__main__':
  instance.section = '/naci'

  print(instance.get_data("2"))