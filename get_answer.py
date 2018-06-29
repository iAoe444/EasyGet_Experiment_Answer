#该程序用于最终结合“download_tiku”中的得到的题库和该程序的爬答题界面的题目功能，搜答案功能
#综合得到最终答案
import requests
import re

def search(question):
    '''该程序用于查找题库和他对应的答案'''
    #打开题库文件操作
    file = open('题库.txt','r',encoding = 'utf-8')#这里要注意要打开的编码为'utf=8编码'
    try:
        file_context = file.read()
    finally:
        file.close()
    #正则表达式查找
    pattern = re.compile(question + r'.*?"answer": "(.*?)"}')#预编译正则表达式
    answer = re.search(pattern,file_context)
    if answer:
        print(answer.group(1))
    else:
        print('题库里该题目的答案')

def get_dati_onepage(page):
    '''该程序用于解析答题界面的题目***需要用到cookie和post方法***'''

    #由于需要用到cookies的方式维持登陆，所以需要用到cookies，这里的cookies使用的是找request里的cookies
    f = open(r'cookies.txt','r')#从文件里找到cookies
    cookies = {}#初始化cookies的字典格式
    for line in f.read().split(';'):#转换cookies的格式为字典格式
        name,value = line.strip().split('=',1)
        cookies[name] = value

    # 由于于网页用的是Ajax加载方式，所以需要用post方法发送headers的page信息，这里是建立page信息，以字典存储
    p = {'page':page}

    #使用post形式请求网页
    response = requests.post("http://10.0.10.145/redir.php?catalog_id=6&cmd=dati",cookies = cookies,data=p)
    html = response.text.encode('iso-8859-1').decode('gbk')#网页是gbk格式，所以需要先改为gbk格式

    #正则表达式提取有用信息，使用list存储
    pattern = re.compile(r'<h3>(\d+?)、(.*?)</h3>')
    items = re.findall(pattern,html)
    return items

def main():
    '''双循环分别解析10页和10页里的10个题目'''
    for i in range(10):
        items = get_dati_onepage(i-1)
        l = len(items)
        for j in range(l):
            print(items[j][0] + '、' + items[j][1])#这里的items[j][0]为题目编号，items[j][1]为具体题目
            search(items[j][1])
        print('\n')

if __name__ == '__main__' :
    main()