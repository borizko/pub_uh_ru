# -*- coding: utf-8 -*-
import urllib2
import config

class Observer:
  def __init__(self):
    self.url = "http://pub-uhru.esy.es"
    self.dict_status = {
    1: "Error out", 
    2: "Publish", 
    3: "Full Error",
    4: "Timeout",
    5: "Stop"
    }
    
  def set_status(self, status_code):
    computer_name = config.Config("App").get("computer_name")
    param = {
    "computer_name": str(computer_name),
    "status_code": str(status_code)
    }
    path = "/set_status.php"
    self.request(path, param, "change")

  def request(self, path, param={}, type_request="change"):
    try:
      url = self.url+path+"?"
      for i, k in enumerate(param):
        if i == 0:
          url += k+"="+str(param[k])
        else:
          url += '&'+k+"="+str(param[k])
      if type_request == "change":
        print url
        urllib2.urlopen(url).read()
    except:
      pass

instance = Observer()

if __name__ == '__main__':
  instance.set_status("1")
