import requests
import time
import re
from bs4 import BeautifulSoup

url = "https://ieagent.jp/blog/money/daigakusei-seikatsuhi-112814"

response = requests.get(url)
html_content = response.text
# BeautifulSoupを使用してHTMLを解析
html_soup = BeautifulSoup(html_content, "html.parser")
time.sleep(1)

def txt_(url) :
  txt_data = []
  texts = html_soup.find_all("th", limit=11)
  for text in texts :
    text = text.get_text()
    txt_data.append(text)
  return txt_data

def txt_money(url) :
  money_data = []
  texts = html_soup.find_all("td", limit=11)
  for text in texts :
    text = text.get_text()
    money_data.append(text)
  return money_data

expense = []
for txt, money in zip(txt_(url),txt_money(url)):
  outcome = txt, money
  expense.append(outcome)

print(expense)

import sqlite3
path = '/content/'
db_name = 'tests.sqlite'
#DBに接続
con = sqlite3.connect(path + db_name)

#SQLを取得するためのオブジェクト取得
cur = con.cursor()

sql_create_table_money = 'CREATE TABLE average_moneys(name int, money int);'

cur.execute(sql_create_table_money)
#DBの接続を閉じる
con.close()
con = sqlite3.connect(path + db_name)

cur = con.cursor()

sql_insert_many = "INSERT INTO average_moneys VALUES (?, ?)"

cur.executemany(sql_insert_many, expense)

con.commit()

con.close()

con = sqlite3.connect(path + db_name)

cur = con.cursor()

sql_select = 'SELECT * FROM average_moneys'

cur.execute(sql_select)

for i in cur:
  print(i)

con.close()