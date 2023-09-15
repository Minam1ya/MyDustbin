#all

import os
import requests
import re
from bs4 import BeautifulSoup
import time
import urllib.request

#使用到的参数
P=[]
urlp = "https://www.luogu.com.cn/problem/" 
urll = "https://www.luogu.com.cn/problem/list?difficulty=0&page=1"
urls = "https://www.luogu.com.cn/problem/solution/"
savedate = "./"
fn =""

#获取符合需求的题目题号
def getlist(url):
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    }
    response = requests.get(url=url, headers=headers,verify=False)
    #print(response.text)
    html = response.text
    pattern = re.compile(r'(<a\shref=".*?">)*?')
    problemlist = re.findall(pattern,response.text)
    for x in problemlist:
        if(x!=""):
            P.append(x[9:14])

#获得题目
def getproblem(url):
    #发送请求部分
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    }
    response = requests.get(url=url, headers=headers,verify=False)
    #print(response.text)
    html = response.text
    #整理数据
    bs = BeautifulSoup(html,"html.parser")
    core = bs.select("article")[0]
    md = str(core)
    md = re.sub("<h1>","# ",md)
    md = re.sub("<h2>","## ",md)
    md = re.sub("<h3>","#### ",md)
    md = re.sub("</?[a-zA-Z]+[^<>]*>","",md)    
    #保存数据
    global fn
    fn =bs.title.string
    fn = fn[:-5]
    savedate = "./"
    savedate = savedate + "save" + "/" + fn
    if not os.path.exists(savedate):
            os.mkdir(savedate)
    filename = savedate + '/' + fn + ".md"
    with open(filename,"w", encoding="utf-8") as fp:    
        fp.write(md)

#获得题解
def getsolution(url):
    #发送请求
    headers = {
    "Cookie": "__client_id=7298f81227f1bc2d6e646cba05a73571d5f5ac0c; _uid=1091435",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"

        }
    response = requests.get(url=url, headers=headers,verify=False)
    #整理数据
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    md = soup.find('script')
    md1 = md.text
    start =  md1.find('"')
    end =  md1.find('"', start + 1)
    md1 =  md1[start + 1:end]
    md2 = urllib.parse.unquote( md1)
    md2  =  md2 .encode('utf-8').decode('unicode_escape')
    start =  md2 .find('"content":"')
    end =  md2 .find('","type":"题解"')
    solution =  md2 [start + 11:end]
    #保存数据
    savedate = "./"
    savedate = savedate + "save" + "/" + fn
    if not os.path.exists(savedate):
            os.mkdir(savedate)
    filename = savedate  + "/" + fn + "-题解" ".md"
    with open(filename,"w", encoding="utf-8") as fp:    
        fp.write(solution)

def main():
    #获取需要的题号
    getlist(urll)
    #开始爬
    count = 0
    for i in range(len(P)):
        count+=1
        print("正在爬{}题的题目".format(P[i]))
        getproblem(urlp+P[i])
        time.sleep(5)
        print("正在爬{}题的题解".format(P[i]))
        getsolution(urls+P[i])
        time.sleep(5)
        if(count>=3):
            break
 
if __name__ == "__main__":
    main()