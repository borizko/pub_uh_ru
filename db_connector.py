# -*- coding: utf-8 -*-
import MySQLdb

from MySQLdb import _mysql as mysql

from config import Config

class DbConnect:

  def __init__(self):
    self.config = Config(self.__class__.__name__)
    self.open()
    sql = """SET NAMES utf8"""
    self.query(sql, "change")

  def query(self, sql, type_query="change"):
    cursor = self.db.cursor()
    cursor.execute(sql)
    if type_query == "change":
      self.db.commit()
      return True
    elif type_query == "select":
      return cursor.fetchall()

  def escape_string(self, txt):
    return mysql.escape_string(txt)

  def close(self):
    self.db.close()

  def open(self):
    self.db = MySQLdb.connect(host=self.config.get("host"), user=self.config.get("username"), passwd=self.config.get("password"), db=self.config.get("db_name"), charset=self.config.get("charset"))