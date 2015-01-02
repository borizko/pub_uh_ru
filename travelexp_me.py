# -*- coding: utf-8 -*-
from module_text import Module_Text
from db_connector import DbConnect
from lxml.html import parse
from lxml.html import fromstring, tostring
import lxml
import sys
import re

class Travelexp_me(Module_Text):
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
    list_link_articles = page.cssselect("div.excerpt h2.excerpt-title a")
    if len(list_link_articles):
      #собираем список из названий и url статей
      list_articles = []
      for link_articles in list_link_articles:
        list_articles.append({"name": link_articles.text.strip(), "url": self.create_absolute_url(link_articles.get("href"))})
      #заходим в каждую статью и парсим текст
      for article in list_articles:
        page = self.get_html(article['url'])
        for content in page.cssselect('div.main-content'):
          #Удаляем не нужные элементы
          for h2 in content.cssselect("h2"):
            h2.getparent().remove(h2)
          for ins in content.cssselect("p ins"):
            p = ins.getparent()
            p.getparent().remove(p)
          for div in content.cssselect("div"):
            div.getparent().remove(div)
          #парсим изображения
          img = []
          for i, image in enumerate(content.cssselect("img")):
            if i == 4:
              break;
            img.append(self.create_absolute_url(image.get("src")))
          pattern = re.compile('<img.*?>')
          list_text = pattern.split(tostring(content))
          text = fromstring("??img".join(list_text)).text_content()
          text = text.strip()
          #Удаляем комментарии
          text = re.sub(r"<[\w\W]+?>", "", text).strip()
          articles_id = self.insert_article_in_db({"module":self.name_module, "section":self.section, "name": self.db.escape_string(article['name'].encode("utf-8")), "text": self.db.escape_string(text.encode("utf-8")), "url": article['url']})
          for i, image in enumerate(img):
            self.insert_image({"articles_id": articles_id, "url": image})
      sql = """UPDATE current_page_module SET page = page-1 WHERE module='%(module)s' AND section='%(section)s'"""%{"module": self.name_module, "section": self.section}
      self.db.query(sql, "change")
    else:
      return None


list_section =[
 {'name': "/", 'start_page': 39, 'id_theme': "4"},
]

__name_module = "travelexp_me"

__host = "travelexp.me"

instance = Travelexp_me(DbConnect(), list_section, __name_module, __host, 'latin-1' )  

if __name__ == '__main__':
  print(instance.parse('/'))