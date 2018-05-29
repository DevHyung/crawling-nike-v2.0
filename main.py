import requests
import urllib.request
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
        print(title)
        print(imgList)

