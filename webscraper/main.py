from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import logging
import json
import time

#universal vars

# debug level
frm = "%(asctime)-15s %(message)s"

lvl = logging.WARNING




#logging.basicConfig(level=logging.DEBUG)
#logging.basicConfig(level=lvl,format=frm,file="log")


def getReq(url):
    try:
        with closing(get(url, stream=True)) as resp:
            if checkResponse(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        logging.warning('error during requests to {} : {}'.format(url, str(e)))
        return None


def checkResponse(resp):
    return (resp.status_code == 200
            and resp.headers['Content-Type'].lower() is not None
            and resp.headers['Content-Type'].lower().find('html') > -1)

raw_html = getReq("https://answers.yahoo.com/dir/index")
html = BeautifulSoup(raw_html, "html.parser")


items = []


for li in html.find_all('li', class_="ya-discover-tile ya-discover-tile-qn Bfc P-14 Bdbx-1g Bgc-w"):
    arr = {}
    arr['title'] = ' '.join(li.find('a', class_="title").text.split())
    arr['category'] = ' '.join(li.find("div", class_="Clr-888 Fz-12 Lh-18").find('a', class_="Clr-b").text.split())
    arr['description'] = ' '.join(li.find('div', class_="fullDesc Mah-130 Ovy-s Fz-13 Lh-18 Ol-n D-n").text.replace('\n', '').split())
    if arr['description'].find('Best answer:') > -1:
        arr['description'] = None

    items.append(arr)


with open('data/'+time.asctime().replace(":","-").replace(" ", "_"), "w") as f:
    f.write(json.dumps(items))
