import urllib.request
from bs4 import BeautifulSoup
import ssl
import re
import time
import xlwt
import sqlite3
import os
from Anjukedistrictspider import *

ssl._create_default_https_context = ssl._create_unverified_context

datalist = []
filename = '安居客未央大学城租房信息表.xls'
requesturl = urlsearchBylocation()
def geturlhtml(requesturl,datalist):
    head = {
        "method":"GET","accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9","accept-language":"zh-CN,zh;q=0.9","user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
    }
    for i in range(30):
        print("第%d页信息获取中..."%(i+1))
        url = requesturl+"/p"+str(i+1)+"/"
        request = urllib.request.Request(url,headers=head)
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        datalistresult = getHouseinfo(html,datalist)
        print("第%s页内容获取完毕"%(i+1))

        time.sleep(0.5)
    print("共获取到%d条租房信息"%(len(datalistresult)))
def getHouseinfo(html,datalist):
    bs = BeautifulSoup(html,"html.parser")
    #每一间房源的全部信息的div标签<div class="zu-itemmod"
    #每一间房标题的标签<div class="zu-info" style="width: auto">
    #每一间房详情<p class="details-item tag">
    #每一间房的地址<address class="details-item">
    #每一间房的价格<div class="zu-side">
    #更多细节<p class="details-item bot-tag" style="width: auto">

    houseinfos = bs.find_all('div',class_="zu-itemmod")
    if houseinfos != []:
        lenhouseinfos = len(houseinfos)
        print("该页共有%d条房屋信息"%lenhouseinfos)
        time.sleep(0.5)
        for i in range(len(houseinfos)):
            houseinfo = str(houseinfos[i])
            data = []
            pattern1 = re.compile(r'<b class="strongbox">(.*)</b>',re.M)
            pattern2 = re.compile(r'<b class="strongbox" style="font-weight: normal;">(.*?)</b>',re.M)
            pattern3 = re.compile(r'<a href=".*" target="_blank">(.*?)</a>.*</address>',re.S)
            pattern4 = re.compile(r'<span class="cls-1">(.*)</span>')
            pattern5 = re.compile(r'<span class="cls-2">(.*)</span>')
            pattern6 = re.compile(r'<span class="cls-3">(.*)</span>')
            pattern7 = re.compile(r'<div _soj="Filter_\d*&amp;hfilter=filterlist" class="zu-itemmod" link="(.*?)">',re.S)
            pattern8 = re.compile(r'<a _soj="Filter_\d*" href="(.*?)" target="_blank">',re.S)


            result1 = re.findall(pattern1,houseinfo)
            data.append(result1[0])
            data.append(result1[1])
            result2 = re.findall(pattern2,houseinfo)
            result2final = result2[0]+"室"+result2[1]+"厅"+result2[2]+"平方米"
            data.append(result2final)
            result3 = re.findall(pattern3,houseinfo)
            data.append(result3[0])
            result4 = re.findall(pattern4,houseinfo)
            data.append(result4[0])
            result5 = re.findall(pattern5,houseinfo)
            data.append(result5[0])
            result6 = re.findall(pattern6,houseinfo)
            if result6 == []:
                data.append("未说明")
            else:
                data.append(result6[0])
            # 每个房屋信息的详情页链接
            housedetailsite = re.findall(pattern7,houseinfo)
            if housedetailsite == []:
                housedetailsite2 = re.findall(pattern8,houseinfo)
                if housedetailsite2 == []:
                    data.append("none")
                else:
                    data.append(housedetailsite2[0])
            else:
                data.append(housedetailsite[0])
            datalist.append(data)
            print(data)
    else:
        print("该网页待验证或无数据...")
    return datalist

def saveData(datalist,filename):
    workbook = xlwt.Workbook(encoding="utf-8")
    worksheet = workbook.add_sheet("sheet_anjuke",cell_overwrite_ok=True)
    col = ('标题','价格','户型面积','地址','租房类型','朝向','有无电梯','详情页')
    for i in range(len(col)):
        worksheet.write(0,i,col[i])
    for j in range(len(datalist)):
        data = datalist[j]
        for k in range(len(data)):
            worksheet.write(j+1,k,data[k])
    workbook.save(filename)
    print("保存数据成功")

def initDb(requesturl):
    #初始化数据库结构
    sql = '''
    create table '%s'(
    id integer primary key autoincrement,
    title varchar,
    price numeric,
    structure text,
    address text,
    renttype varchar,
    direction varchar ,
    elevator varchar ,
    detailsite text
    )
    '''%requesturl
    # databaseName = "Anjuke-"+ locationIndex
    conn = sqlite3.connect("Anjuke_Data.db")
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    conn.close()

def insert2Db(datalist,requesturl):
    #判断database文件是否存在
    filedir = './Anjuke_Data.db'
    initDb(requesturl)
    conn = sqlite3.connect("Anjuke_Data.db")
    cur = conn.cursor()
    for data in datalist:
        for index in range(len(data)):
            if index == 1:
                continue
            data[index] = "'"+data[index]+"'"
        sql = '''
        insert into '%s' (title,price,structure,address,renttype,direction,elevator,detailsite)values(%s)''' %(requesturl, ",".join(data))

        cur.execute(sql)

    conn.commit()
    conn.close()


#判断房子是合租还是整租
def is_room_shared():
    datalist = []
    sharedrooms = []
    entirerooms = []
    conn = sqlite3.connect("Anjuke_Daxuecheng.db")
    cur = conn.cursor()
    sql = "select * from Anjukehouseinfo"
    data = cur.execute(sql)
    for houseitem in data:
        datalist.append(houseitem)
    cur.close()
    conn.close()
    for room in datalist:
        if room[5] == "合租":
            sharedrooms.append(room)
        else:
            entirerooms.append(room)
    for sharedroom in sharedrooms:
        print(sharedroom)
    for entireroom in entirerooms:
        print(entireroom)
    time.sleep(2)
    p1 = average_Price(sharedrooms)
    p2 = average_Price(entirerooms)

    print("合租平均价格为：%d"%p1)
    print("整租平均价格为：%d"%p2)
#判断房子平均价格
def average_Price(rooms):
    sumprice = 0
    for room in rooms:
        sumprice += room[2]
    averageprice = sumprice/len(rooms)
    return averageprice

if __name__ == '__main__':
    geturlhtml(requesturl,datalist)
    # saveData(datalist,filename)
    insert2Db(datalist,requesturl)
