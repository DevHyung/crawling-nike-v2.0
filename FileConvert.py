import os
from PIL import Image
if __name__ == "__main__":
    print(">>> PNG To JPG 프로그램")
    print(">>> 사용법 : 사진폴더에 넣고 실행파일 클릭하면 됩니다.")
    files = os.listdir('./')
    print(">>> 변환중...")
    for file in files:
        im = Image.open('./'+file)
        if not im.mode == 'RGB':
            im = im.convert('RGB')
            im.save('./'+file)
    print(">>> 변환완료")
    input("종료하시려면 아무키나 눌러주세요")
