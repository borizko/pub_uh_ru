# -*- coding: utf-8 -*-
import time
import urllib2
import observer
import config

class Remote_Manager:
  def __init__(self):
    self.config = config.Config("App")
    self.url = "http://pub-uhru.esy.es/is_stop.php?computer_name="+self.config.get("computer_name")

  def is_stop(self):
    try:
      return not not int(urllib2.urlopen(self.url).read().rstrip())
    except:
      return True


  def check_stop(self):
    print "Проверка остановки"
    if self.is_stop():
      while self.is_stop():
        print "Стоп"
        time.sleep(15)

instance = Remote_Manager()
if __name__ == '__main__':
  print instance.is_stop()

