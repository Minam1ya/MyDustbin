#demo
from tkinter import *
import tkinter as tk
from tkinter import  messagebox
import os
import requests
import re
from bs4 import BeautifulSoup
import time
import urllib.request

#声明各种变量
P=[]
urlp = "https://www.luogu.com.cn/problem/" 
urls = "https://www.luogu.com.cn/problem/solution/"
savedate = "./"
fn =""
var1 = ""
var2 = ""
var3 = ""
difficulty = ""
type = ""
keyword = ""


#一个对题目来源进行转换的程序
def select1(var):
    global type
    if var == "洛谷":
        type = "B%7CP"
    elif var == "主题库":
        type = "P"
    elif var == "入门与面试":
        type = "B"
    elif var == "CodeForces":
        type = "CF"
    elif var == "SPOJ":
        type = "SP"
    elif var == "AtCoder":
        type = "AT"
    elif var == "UVA":
        type = "UVA"
    return select1

#一个对题目难度进行转换的程序
def select2(var):
    global difficulty
    if var == "暂无评定":
        difficulty = "0"
    elif var == "入门":
        difficulty = "1"
    elif var == "普及-":
        difficulty = "2"
    elif var == "普及/提高-":
        difficulty = "3"
    elif var == "普及+/提高":
        difficulty = "4"
    elif var == "普及+/省选-":
        difficulty = "5"
    elif var == "省选/NOI-":
        difficulty = "6"
    elif var == "NOI/NOI+/CTSC":
        difficulty = "7"
    return select2

#获取符合需求的题目列表
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

#主程序
def start():
    #获取需要的题号
    global var1 
    global var2 
    global var3
    global keyword
    global difficulty
    global type
    #题目来源函数
    select1(var1)
    #题目难度函数
    select2(var2)
    #关键字(不知道为什么只能是一个字，两个字就会报错
    keyword = var3
    urll = "https://www.luogu.com.cn/problem/list?difficulty=" + difficulty + "&page=1" + "&type=" + type + "&keyword=" + keyword
    print(urll)
    var1 = ""
    var2 = ""
    var3 = ""
    #获取题目列表
    P.clear()
    getlist(urll)
    difficulty = ""
    type = ""
    keyword = ""
    #开始爬
    count = 0
    for i in range(len(P)):
        count+=1
        print("正在爬{}题的题目".format(P[i]))
        getproblem(urlp+P[i])
        time.sleep(3)
        print("正在爬{}题的题解".format(P[i]))
        getsolution(urls+P[i])
        time.sleep(3)
        if(count>=50):
            P.clear()
            break


root = tk.Tk()
root.geometry('640x320+500+300')
root.title('爬虫模拟器V0.002学习版')



#第一个条件
p10 = Label(root,text="所属题库:")
p10.grid(column=1,row=0,ipadx=20,ipady=3)

#题目所属列表
list1 = tk.StringVar()
p11 = tk.Listbox(root,listvariable=list1)
p11.insert(1,"洛谷")    
p11.insert(2,"主题库")
p11.insert(3,"入门与面试")
p11.insert(4,"CodeForces")
p11.insert(5,"SPOJ")
p11.insert(6,"AtCoder")
p11.insert(7,"UVA")
p11.grid(column=2,row=0,ipadx=20,ipady=3)

#获取所属题库
def get1():
    global var1
    var1 = p11.get(p11.curselection())
    print(var1)

p12 =tk.Button(root,text="确定题库",command= get1)
p12.grid(column=2,row=1,ipadx=20,ipady=10)

#第二个条件
p20 = Label(root,text="题目难度:")
p20.grid(column=3,row=0,ipadx=20,ipady=3)

#题目难度列表
p21 = tk.Listbox(root)
p21.grid(column=4,row=0,ipadx=20,ipady=3)

list2 = tk.StringVar()
p21 = tk.Listbox(root,listvariable=list2)
p21.insert(1,"暂无评定")    
p21.insert(2,"入门")
p21.insert(3,"普及-")
p21.insert(4,"普及/提高-")
p21.insert(5,"普及+/提高")
p21.insert(6,"普及+/省选-")
p21.insert(7,"省选/NOI-")
p21.insert(8,"NOI/NOI+/CTSC")
p21.grid(column=4,row=0,ipadx=20,ipady=3)

#获取所属题目难度
def get2():
    global var2
    var2 = p21.get(p21.curselection())
    print(var2)

#确认题目难度按钮
p22 =tk.Button(root,text="确定题目难度",command= get2)
p22.grid(column=4,row=1,ipadx=20,ipady=10)

#第三个条件
p30 = Label(root,text="输入关键字:")
p30.grid(column=1,row=3,ipadx=20,ipady=10)

#输入关键字
def get3():
    global var3
    data= p31.get()
    var3 = str(data)

#关键字输入框
p31 = tk.Entry(root,show=None)
p31.grid(column=2,row=3,ipadx=20,ipady=10)

#确认关键字按钮
p32 =tk.Button(root,text="确定关键字",command=get3 )
p32.grid(column=3,row=3,ipadx=20,ipady=10)

#开始爬取按钮
p40 =tk.Button(root,text="给我爬!",command= start )
p40.grid(column=4,row=3,ipadx=20,ipady=10)

root.mainloop()