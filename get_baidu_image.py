import requests
import re
import os
import urllib.parse
from lxml import etree
import time


def get_html(url):
    """获取网页并返回文本"""

    headers = {
        'Referer': 'https://image.baidu.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
    }
    try:
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            r.encoding = r.apparent_encoding
            return r.text
        else:
            print("请求页面失败！")
    except Exception as e:
        print(e)


def get_image_url(text):
    """从web文本中提取图片真实的url"""
    image_url = re.findall('"thumbURL":"(.*?)",', text)  # 正则表达式
    return image_url


def get_image_content(image_url):
    """通过图片url获取图片内容"""
    headers = {
        'Referer': image_url,
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
    }
    try:
        r = requests.get(image_url, headers=headers)
        if r.status_code == 200:
            r.encoding = r.apparent_encoding
            return r.content
        else:
            print('请求失败！')
    except Exception as e:
        print(e)


def save_image(image_url, image_content):
    """将图片保存到本地"""
    root_dir = 'D:\\baiduimage\\'
    path = root_dir + image_url.split('/')[-1]
    if not os.path.exists(root_dir):
        os.makedirs(root_dir)
    if not os.path.exists(path):
        try:
            with open(path, 'wb') as f:
                f.write(image_content)
                print('图片{}保存成功，地址在{}'.format(image_url, path))
        except:
            print('保存路径有错：',path)
    else:
        print("图片已存在！")



def main():
    keyword = input('请输入你要查询的关键字：')
    keyword_quote = urllib.parse.quote(keyword)  # URL使用中文字符需要urllib.parse.quote进行编码
    num_page = int(input("请输入要爬取的页数(每页30张图): "))  # 百度每次最多请求30张图片
    count = 0
    for i in range(num_page):
        url = 'https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord+=&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&word={}&z=&ic=0&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&step_word={}&pn={}&rn=30&gsm=1e&1541136876386='.format(
            keyword_quote, keyword_quote, i * 30)
        count += 1
        print(count)
        html = get_html(url)
        image_urls = get_image_url(html)
        for image_url in image_urls:
            content = get_image_content(image_url)
            save_image(image_url, content)

        time.sleep(5)
if __name__ == '__main__':
    main()
