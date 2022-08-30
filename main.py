from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

birthday_boy = os.environ['BIRTHDAY_BOY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]

xingzuo = os.environ["XINGZUO"]

def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['low']),math.floor(weather['high']),weather['airQuality'],weather['wind'],weather['humidity']


def get_xingzuo():
  url = "https://api.tianapi.com/star/index?key=6859083171726381ffd34bc51ad5592b&astro=" + xingzuo
  res = requests.get(url).json()
  return res['newslist'][5][content] ,res['newslist'][6][content],res['newslist'][7][content],res['newslist'][8][content]

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_birthdayboy():
  next = datetime.strptime(str(date.today().year) + "-" + birthday_boy, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature_hight,temperature_low,airQuality,wind,humidity = get_weather()

luck_color ,luck_number ,guiren_xingzuo ,today_content = get_xingzuo()
  

data = {"weather":{"value":wea,"color":get_random_color()},
        "city":{"value":city},
        "temperature":{"value":temperature_hight,"color":get_random_color()},
        "temperature_low":{"value":temperature_low,"color":get_random_color()},
        "airQuality":{"value":airQuality,"color":get_random_color()},
        "wind":{"value":wind,"color":get_random_color()},
        "humidity":{"value":humidity,"color":get_random_color()},
        
        "luck_color":{"value":luck_color,"color":get_random_color()},   
        "luck_number":{"value":luck_number,"color":get_random_color()},        
        "guiren_xingzuo":{"value":guiren_xingzuo,"color":get_random_color()},     
        "today_content":{"value":today_content,"color":get_random_color()},
        
        "love_days":{"value":get_count(),"color":get_random_color()},
        "birthday_left":{"value":get_birthday(),"color":get_random_color()},
        "birthday_boy":{"value":get_birthdayboy(),"color":get_random_color()},
        "words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
