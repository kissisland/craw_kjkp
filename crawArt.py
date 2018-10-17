import requests, csv, time
from multiprocessing.dummy import Pool
from lxml import html


start_url = 'https://www.kjkp.com/articles?page={}'
all_links = []



def save(title, content):
    with open("{}.txt".format(title), 'w', encoding='utf-8', newline="") as f:
        f.write(content)


def get_list(url):
    try:
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            selector = html.fromstring(res.content)
            links = selector.xpath("//h2[@class='title']/a/@href")
            print(links)
            all_links.extend(links)
        else:
            time.sleep(5)
            get_list(url)
    except Exception as e:
        time.sleep(5)
        print("getlist异常:{}".format(e))
        get_list(url)


def get_detail(url):
    try:
        res = requests.get(url)
        if res.status_code == 200:
            selector = html.fromstring(res.content)
            title = selector.xpath("//h3[@class='title']/text()")
            if title:
                title = title[0]
                title = title.replace("?",'').replace("！",'').replace('"','').strip()
            content = selector.xpath("//div[@class='content mt-10']")
            if content:
                content = content[0].xpath("string(.)")

            print(title)
            save(title, content)
    except Exception as e:
        time.sleep(5)
        print("get_detail异常:{}".format(e))
        get_detail(url)

if __name__ == '__main__':
    pool = Pool(50)

    pool.map(get_list,[start_url.format(i) for i in range(1, 44)])

    pool.map(get_detail, all_links)

