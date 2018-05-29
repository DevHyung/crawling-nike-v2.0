import requests
import urllib.request
import os
import xlsxwriter
from bs4 import BeautifulSoup
import time
now = time.localtime()
s = "%04d%02d%02d_%02d%02d추출" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min)
wb = xlsxwriter.Workbook('./'+s+'.xlsx')
ws = wb.add_worksheet('sheet1')
ws.write(0, 0, "파일명이름")
ws.write(0, 1, "이름")
ws.write(0, 2, "모델명")
ws.write(0, 3, "색상")
ws.write(0, 4, "재질")
ws.write(0, 5, "사진들")
j = 1

if __name__=="__main__":
    fileList = open("FILELIST.txt").readlines()
    baseUrl = "https://www.nike.com/kr/ko_kr/search?q="
    urlList = []
    codeList = []
    # URL 수집
    for code in fileList:
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
    print("[INFO] 총",len(urlList),"개 URL 수집완료")
    for url in urlList:
        print(url)
        html = requests.get(url)
        bs4 = BeautifulSoup(html.text, 'lxml')
        ###
        imgList = []
        title = bs4.find('h1',class_='title-wrap').get_text().strip()
        picLi = bs4.find('ul',id='product-gallery').find_all('li')
        style = bs4.find('span',class_='style-color').get_text().split(':')[1].strip()
        prodCode = bs4.find('span',class_='style-code').get_text().split(':')[1].strip()
        noti = bs4.find('div',class_='product-noti-content').find('dd').get_text().strip()
        for pic in picLi:
            imgList.append(pic.find('img')['src'])

        print("[INFO] 코드 : " + prodCode)
        print("[INFO] 한글 상품명 : " + title)
        print("[INFO] 컬러 : " + style)
        print("[INFO] 소재 : " + noti)
        ws.write(j, 0, prodCode)
        ws.write(j, 1, title)
        ws.write(j, 2, prodCode)
        ws.write(j, 3, style)
        ws.write(j, 4, noti)
        count = 1
        for pic_url in imgList:
            print("[INFO] " + str(count) + "번째 사진 다운로드 시작.")
            # dirname = "./pics/" + str(code)
            dirname = "./pics/"
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            fileurl = dirname + str(prodCode.strip()) + "_" + str(count) + ".png"
            urllib.request.urlretrieve(pic_url, fileurl)
            ws.write(j, 4 + count, os.getcwd() + fileurl[1:].replace('/', '\\'))
            count += 1
        j+=1
wb.close()


