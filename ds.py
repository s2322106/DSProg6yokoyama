import requests # urlを読み込むためrequestsをインポート
import time
from bs4 import BeautifulSoup # htmlを読み込むためBeautifulSoupをインポート

URL = 'https://www.univcoop.or.jp/press/life/report.html' # URL入力
images = [] # 画像リストの配列

soup = BeautifulSoup(requests.get(URL).content,'lxml') # bsでURL内を解析
time.sleep(0.01)

for link in soup.find_all("img"): # imgタグを取得しlinkに格納
    if link.get("src").endswith(".jpg"): # imgタグ内の.jpgであるsrcタグを取得
        images.append(link.get("src")) # imagesリストに格納


