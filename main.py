import requests
import urllib.request
import os
from bs4 import BeautifulSoup

if __name__=="__main__":
    fileList = open("FILELIST.txt").readlines()
    baseUrl = "https://www.nike.com/kr/ko_kr/search?q="
    urlList = []
    # URL 수집
    for code in fileList[:3]:

        Url = baseUrl + code.strip()
        html = requests.get(Url)
        bs4 = BeautifulSoup(html.text,'lxml')
        ###
        div = bs4.find('div',class_='filter-tit')
        num = div.find('span',class_='num').get_text().strip()
        if num == '(0)':
            pass
        else:
            item = bs4.find('ul',class_='uk-grid item-list-wrap')
            urlList.append('https://www.nike.com'+item.find('a')['href'])

    for url in urlList[:1]:
        print(url)
        html = requests.get(url)
        bs4 = BeautifulSoup(html.text, 'lxml')
        ###
        imgList = []
        title = bs4.find('h1',class_='title-wrap').get_text().strip()
        picLi = bs4.find('ul',id='product-gallery').find_all('li')
        for pic in picLi:
            imgList.append(pic.find('img')['src'])
        count = 1
        print("[INFO] 한글 상품명 : " + title)
        for pic_url in imgList:
            print("[INFO] " + str(count) + "번째 사진 다운로드 시작.")
            # dirname = "./pics/" + str(code)
            dirname = "./pics/"
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            fileurl = dirname + str(code.strip()) + "_" + str(count) + ".png"
            urllib.request.urlretrieve(pic_url, fileurl)
            #ws.write(j, 4 + count, os.getcwd() + fileurl[1:].replace('/', '\\'))
            count += 1



