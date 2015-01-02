# -*- coding: utf-8 -*-
from PIL import Image
from pymouse import PyMouse
import pyatspi
import time
import datetime
import random
import sys

reg = pyatspi.Registry.generateKeyboardEvent

dict_keys = {
  'a' : 38,
  'b' : 56,
  'c' : 54,
  'd' : 40,
  'e' : 26,
  'f' : 41,
  'g' : 42, 
  'h' : 43,
  'i' : 31,
  'j' : 44,
  'k' : 45,
  'l' : 46,
  'm' : 58,
  'n' : 57,
  'o' : 32,
  'p' : 33,
  'q' : 71,
  'r' : 27,
  's' : 39,
  't' : 28,
  'u' : 30,
  'v' : 55,
  'w' : 25,
  'x' : 53,
  'y' : 29,
  'z' : 52,
  '-' : 20,
  '.' : 60,
  '/' : 61,
  1 : 10,
  2 : 11,
  3 : 12,
  4 : 13,
  5 : 14,
  6 : 15,
  7 : 16,
  8 : 17,
  9 : 18,
  0 : 19,  
}

def input_text(text):
  reg = pyatspi.Registry.generateKeyboardEvent
  for ch in text:
    if ch.isalpha():
      if ch.isupper():
        reg(62, None, pyatspi.KEY_PRESS)
        reg(dict_keys[ch.lower()], None, pyatspi.KEY_PRESSRELEASE)
        reg(62, None, pyatspi.KEY_RELEASE)
        continue
      if ch.islower():
        reg(dict_keys[ch], None, pyatspi.KEY_PRESSRELEASE)
        continue
    if ch in ['_', '-', '.', '/']:
      if ch == '_':
        reg(62, None, pyatspi.KEY_PRESS)
        reg(20, None, pyatspi.KEY_PRESSRELEASE)
        reg(62, None, pyatspi.KEY_RELEASE)
      else:
        reg(dict_keys[ch], None, pyatspi.KEY_PRESSRELEASE) 
      continue
    if unicode(ch).isnumeric():
      reg(dict_keys[int(ch)], None, pyatspi.KEY_PRESSRELEASE) 
      continue  


def resize_image(img, size=(410, 410)):
  print("Resize")
  image = Image.open(img)
  print("Old size: "+str(image.size[0])+"x"+str(image.size[1]))
  width = image.size[0]
  height = image.size[1]
  if image.size[0] < size[0]:
    width = size[0] 
    image = image.resize((width, image.size[1]*(width/image.size[0])))
  if image.size[1] < size[1]:
    height = size[1]
    image = image.resize((width, height))
  image.save(img)
  print("New size: "+str(image.size[0])+"x"+str(image.size[1]))
  
def press_enter():
  reg(36, None, pyatspi.KEY_PRESSRELEASE)

def press_down():
  reg(116, None, pyatspi.KEY_PRESSRELEASE)

def move_screen(target="right"):
  reg(37, None, pyatspi.KEY_PRESS)
  reg(64, None, pyatspi.KEY_PRESS)
  if target == "right":
    reg(114, None, pyatspi.KEY_PRESSRELEASE)
  elif target == "left":
    reg(113, None, pyatspi.KEY_PRESSRELEASE)
  reg(37, None, pyatspi.KEY_RELEASE)
  reg(64, None, pyatspi.KEY_RELEASE)

def change_screenshot(img):
  image = Image.open(img)
  out_image = image.crop((12, 135, 95, 186))
  out_image.save(img)

def pay_idx(a, b):
  now = datetime.datetime.now()
  if now.hour > 8 and now.hour < 23:
    return random.randint(a[0], a[1])
  else:
    return random.randint(b[0], b[1])

def move_mouse():
  M = PyMouse()
  x0, y0 = M.position()[0], M.position()[1]
  time.sleep(10)
  x1, y1 = M.position()[0], M.position()[1]
  if x1 != x0 or y1 != y0:
    return
  x1 = x0 + 100
  y1 = y0 + 100
  M.move(x1, y1)
  time.sleep(2)
  M.move(x0, y0)


def debug(data=[]):
  for item in data:
    if type(item) == type({}):
      print("!")
      for k in item:
        print(k)
        print("->")
        print(item[k])
        print("\n")
    else:
      print(item)
      print("------------")
  sys.exit()

