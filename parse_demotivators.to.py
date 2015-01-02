# -*- coding: utf-8 -*-
from lxml.html import parse
import MySQLdb
import sys
import urllib2

DEFAULT_PAGE = 500
HOST = "http://demotivators.to"
db = MySQLdb.connect(host="localhost", user="root", passwd="1", db="pub_uhru_v2", charset="utf8")
cursor = db.cursor()

def get_page(db):
    cursor = db.cursor()
    sql = """SELECT page FROM current_page LIMIT 1"""
    cursor.execute(sql)
    data = cursor.fetchall()
    num_page = None
    for res in data:
        num_page = res[0]
    if num_page == None:
        num_page = DEFAULT_PAGE
        sql = """INSERT INTO current_page(page) VALUES(%(page)i)"""%{"page": num_page}
        cursor.execute(sql)
        db.commit()
    return num_page

def set_page(db, num_page):
    cursor = db.cursor()
    sql = """DELETE FROM current_page"""
    cursor.execute(sql)
    db.commit()
    sql = """INSERT INTO current_page(page) VALUES(%(page)i)"""%{"page": num_page}
    cursor.execute(sql)
    db.commit()



num_page = get_page(db)
if num_page == 0:
    sys.exit(-1)
if num_page != 1:
    page = parse(HOST+'?page=' + str(num_page)).getroot()
elif num_page == 1:
    page = parse(HOST).getroot()
#ищем ссылки на полные изображения
elem_div = []
elem_div = page.cssselect("table div.poster")

if len(elem_div):
    hrefs = []
    for div in elem_div:
        hrefs.append(div.get("data-sharer-url"))
        print("")

    if len(hrefs):
        #вставляем ссылки в таблицу demotivators
        sql = """INSERT IGNORE INTO demotivators(url) VALUES"""
        for href in hrefs:
            if href == hrefs[-1]:
                sql += "('%(href)s')"%{"href": href}
            else:
                sql += "('%(href)s'), "%{"href": href}
       # print(sql)
        #sys.exit()
        cursor.execute(sql)
        db.commit()
        #/
else:
    sys.exit(-1)
#переходим по каждой ссылке
for href in hrefs:
    page = parse(href).getroot()
    imgs = []
    imgs = page.cssselect("span.poster-img > a > img")
    if len(imgs) == 0:
        sys.exit(-1)
    else:
        for img in imgs:
            file_name = img.get("src").split("/")[-1]
            f = open("demotivators.to/dowloaded_image/" + file_name, "wb")
          #  print(HOST+img.get("src"))
          #  sys.exit()
            headers = {'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)'}
            req = urllib2.Request(HOST + img.get("src"), None, headers)
            f.write(urllib2.urlopen(req).read())
            sql = """DELETE FROM demotivators WHERE url='%(href)s'"""%({"href": href})
            cursor.execute(sql)
            db.commit()

            sql = """INSERT IGNORE INTO demotivators(name, path, url) VALUES('%(name)s', '%(path)s', '%(href)s')"""%({"name": db.escape_string(img.get("alt").encode("utf-8")), "path": db.escape_string(("demotivators.to/dowloaded_image/" + file_name).encode("utf-8")), "href": db.escape_string(href.encode('utf-8'))})
            cursor.execute(sql)
            db.commit()
page = num_page - 1
sql = """UPDATE current_page SET page=%(page)i WHERE page=%(num_page)i"""%({"page": page, "num_page": num_page})
cursor.execute(sql)
db.commit()
db.close()
