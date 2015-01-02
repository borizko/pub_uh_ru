# -*- coding: utf-8 -*-

from uh_ru import Uh_ru

class Voiter(Uh_ru):

  def get_page_article(self, obj_pub):
    try:
      self.driver.get("http://uh.ru/a/"+obj_pub.id_article)
    except:
      return False
    return True

  def voiting(self, obj_pub):
    try:
      self.driver.execute_script("$.get('http://uh.ru/ajax.php?file=article_voting&voice=5&article="+obj_pub.id_article+"')")
    except:
      return False
    return True

  def voiting_down(self):
    self.open_url(self.start_url)
    try:
      list_a = self.driver.find_elements_by_css_selector("a.name")
      for a in list_a:
        id_article = a.get_attribute("href").split("/")[2]
        self.driver.execute_script("$.get('http://uh.ru/ajax.php?file=article_voting&voice=1&article="+id_article+"')")
        print("Voiting down")
    except:
      pass



