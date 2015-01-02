# -*- coding: utf-8 -*-
import ConfigParser
import sys

class Config:
  def __init__(self, class_name):
    self.class_name = class_name
    self.file = "settings/config.ini"

  def get(self, param):
    config = ConfigParser.RawConfigParser()
    config.read(self.file)
    return config.get(self.class_name, param)

  def set(self, param, value):
    config = ConfigParser.RawConfigParser()
    config.read(self.file)
    config.set(self.class_name, param, value)
    with open(self.file, 'wb') as configfile:
      config.write(configfile)

if __name__ == '__main__':
  instance = Config("Worker")
  print type(instance.get("walk_min"))
