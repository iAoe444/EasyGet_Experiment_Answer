#该程序用于爬取题库，将它保存在"题库.txt"文件里
import requests
import re
import json
from requests.exceptions import RequestException

def get_one_page(url):
    '''用于获取网页的HTML格式文本'''
    try:
        response=requests.get(url)#避免出现错误，使用requests.exceptions模块来调试错误
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def parse_one_page(html):
    '''用于匹配文本而将其写入字典中后放在容器里'''
    pattern = re.compile(r'<h3>\d{0,5}、(.*?)</h3>.*?<span style="color:#666666">（标准答案：\s+(.*?)\s+）</span>')
    items = re.findall(pattern,html)
    for item in items:
        yield {
            'question': item[0],
            'answer': item[1]
        }

def write_to_file(question_bank):
    '''这个函数用于将得到的字典格式的文件以文本方式写入题库里'''
    with open('题库.txt','a' ,encoding='utf-8') as f: #这里的a代表向后追加
        f.write(json.dumps(question_bank,ensure_ascii=False) + '\n')
        f.close()

def main(url,page):
    '''通过循环来获取一个题目主题的所有题目和答案内容'''
    for i in range(page):
        newurl = url + str(i)
        html = get_one_page(newurl).encode('iso-8859-1').decode('gbk')
        for item in parse_one_page(html):
            print(item)
            write_to_file(item)

if __name__ == '__main__':
    #url和urlpage用于存储题库的链接和页数，这里可以写个自动判断题目的程序
    url = ['http://10.0.10.145/redir.php?catalog_id=6&cmd=learning&tikubh=1436&page=',\
           'http://10.0.10.145/redir.php?catalog_id=6&cmd=learning&tikubh=1467&page=',\
           'http://10.0.10.145/redir.php?catalog_id=6&cmd=learning&tikubh=1471&page=',\
           'http://10.0.10.145/redir.php?catalog_id=6&cmd=learning&tikubh=1484&page=',\
           'http://10.0.10.145/redir.php?catalog_id=6&cmd=learning&tikubh=1485&page=',\
           'http://10.0.10.145/redir.php?catalog_id=6&cmd=learning&tikubh=1486&page=',\
           'http://10.0.10.145/redir.php?catalog_id=6&cmd=learning&tikubh=4199&page=',\
           'http://10.0.10.145/redir.php?catalog_id=6&cmd=learning&tikubh=4200&page=']
    urlpage = [77,37,80,27,19,12,10,16]
    for i in range(len(urlpage)):
        main(url[i],urlpage[i])