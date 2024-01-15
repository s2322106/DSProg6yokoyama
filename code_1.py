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
    text = re.sub(r"[円,]", "", text.get_text())
    money_data.append(text)
  return money_data

expense = []
for txt, money in zip(txt_(url),txt_money(url)):
  outcome = txt, money
  expense.append(outcome)

##スクレイピングデータを保存
import sqlite3
path = '/Users/hiro/assignment/DSpfinal/DSProg6yokoyama/'
db_name = 'tests.db'
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

##ローカルデータを保存
path = '/Users/hiro/assignment/DSpfinal/DSProg6yokoyama/'
db_name = 'mydata.db'

con = sqlite3.connect(path + db_name)

cur = con.cursor()
sql_create_table_mydata = 'CREATE TABLE my_money(name text, money int);'
cur.execute(sql_create_table_mydata)
con.close()

con = sqlite3.connect(path + db_name)

cur = con.cursor()

sql_insert_mydata = 'INSERT INTO my_money VALUES (?,?)'

mydata_list  = [
    ('居住費', 0),
    ('食費', 14959),
    ('交通費', 3653),
    ('教養娯楽費', 7877),
    ('書籍費', 1020),
    ('勉学費', 0),
    ('日常費', 137),
    ('電話代', 0),
    ('その他', 0),
    ('貯金・繰越金', 0),
    ('支出合計', 27646)
]

cur.executemany(sql_insert_mydata, mydata_list)

con.commit()

con.close()



