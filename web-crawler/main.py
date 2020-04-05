import requests
from bs4 import BeautifulSoup
import time
import os
import re
import logging
import shutil


streamHandler = logging.StreamHandler()
logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)
logger.addHandler(streamHandler)

url = 'https://alicek106.com'
url_prefix = 'https://alicek106.com'

sites = {
}
deleted_sites = {
}

agent_header = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
image_header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'Host': 'img.alicek106.com',
            'User-Agent': agent_header,
            'Referer': 'https://alicek106.com/'
        }


def download_image(url, uuid):
    with requests.Session() as session:
        try:
            if os.path.exists('data/' + uuid):
                return False
            else:
                os.mkdir('data/' + uuid)

            session.headers = {"User-Agent": agent_header}
            max_retries = 0
            while max_retries < 5:
                try:
                    response = session.get(url)
                except Exception as e:
                    logger.error('something wrong in download image')
                soup = BeautifulSoup(response.content, 'html.parser')
                if response.status_code == 200 and soup != '':
                    break
                else:
                    logger.error(f'response code is not 200 : {response.status_code}')
                    max_retries += 1

            with open(f'data/{uuid}/text.txt', 'w', encoding='utf8') as handler:
                handler.write(soup.find("title").text)
                handler.write('\n')
                handler.write(soup.find("div", {"class": "writing_view_box"}).text.strip())

            if soup.find("ul", {"class": "appending_file"}) is None:
                # This is just text.
                return True

            files = soup.find('ul', {'class': 'appending_file'}).find_all('a')
            # TODO // len(file_uid)/10 result in unexpected action.
            for idx, file in enumerate(files):
                image_url = file.get('href')
                file_uid = re.compile(r'no=\w*').search(image_url).group().split('=')[1] + '.jpg'
                try:
                    response = requests.get(image_url.replace('download.php', 'viewimage.php'), headers=image_header)
                except Exception as e:
                    logger.error('something wrong in download image 2')
                # with open(f'data/{uuid}/{file_uid[:int(len(file_uid)/10)]}.jpg', 'wb') as handler:
                with open(f'data/{uuid}/{idx}-{file_uid[:int(len(file_uid) / 10)]}.jpg', 'wb') as handler:
                    handler.write(response.content)
        except Exception as e:
            print(e)
            print(url)
            return False

        return True

# 삭제된 게시물의 파일은 따로 보관
def store_deleted_files():
    global sites
    copy_of_sites = dict(sites)

    url = 'alicek106.com'
    with requests.Session() as session:
        session.headers = {"User-Agent": agent_header}
        try:
            response = session.get(url, headers={"Accept": "application/text"})
        except Exception as e:
            logger.error('something wrong')
            return
        if '이용에 불편을 드려 죄송합니다' in response.text:
            logger.error('site error in store_deleted_files')
            return

        if response.text == '':
            logger.error('empty string.')
            return

        for key, val in sites.items():
            if key not in response.text:
                try:
                    shutil.move('data/' + key, 'removed')
                    logger.info(f'post moved : {key}')
                except Exception as e:
                    logger.error(f'already exist, but tried to move : {key}')
                del copy_of_sites[key]
                deleted_sites[key] = key

    sites = dict(copy_of_sites)

# 등록 후 1분 이상 된 게시글은 dict에서 삭제 (메모리 관리)
def delete_stale_dict():
    global sites
    current = time.time()
    copy_of_sites = dict(sites)
    for key, val in sites.items():
        # 60초 안에 페이지네이션이 발생할 경우 false positive가 발생함.
        # 60초 안에 삭제된 게시글만 catch 가능
        if current - val > 120:
            del copy_of_sites[key]
            deleted_sites[key] = key
            print(f'deleted from dict : {key}')
    sites = dict(copy_of_sites)

while True:
    with requests.Session() as session:
        time.sleep(5) # 1초 주기로 가져옴
        session.headers = {"User-Agent": agent_header}
        try:
            response = session.get(url, headers={"Accept": "application/text"})
        except Exception as e:
            logger.error('something wrong. continue.')
        data = BeautifulSoup(response.text, 'html.parser').find_all(class_="gall_tit ub-word")

        for i in data[3:]:
            result = i.find('a')
            uuid = re.compile(r'no=\d*').search(result['href']).group().split('=')[1]

            if int(uuid) > UNIQUE_NUMBER and uuid not in sites and uuid not in deleted_sites:
                sites[uuid] = time.time()
                if download_image(url_prefix + result['href'], uuid):
                    logger.info(f'saved {result["href"]}')
            else: # 이미 다운로드가 되어 있음
                pass

        # 등록 후 10분 이상 된 게시글은 dict에서 삭제
        delete_stale_dict()

        # 삭제된 게시물일 경우 별도로 보관
        store_deleted_files()
