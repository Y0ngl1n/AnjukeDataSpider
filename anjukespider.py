import urllib.request
from bs4 import BeautifulSoup
import ssl
import re
import time
import xlwt
import sqlite3
import os

ssl._create_default_https_context = ssl._create_unverified_context
showdistrictname = []
showstreetname = []
districtDict = {"未央": "weiyangq", "雁塔": "yantaqu", "高新": "gaoxinxa", "经开区": "jingkaiqux", "莲湖": "lianhuqu",
                "碑林": "beilinqu", "长安": "changanb", "新城": "xinchengqu", "曲江新区": "qujiangxinqu", "灞桥": "baqiaoqu",
                "高陵": "gaoling", "浐灞": "chanba", "临潼": "lintongqu", "西咸新区": "xixianxinqu", "鄠邑": "huyiqu",
                "大兴新区": "daxingxinqu", "周至": "zhouzhixian", "蓝田": "lantianxian", "阎良": "yanliangqu",
                "西安周边": "xianzhoubianc", "国际港务区": "gjgwqxa", }
def showDistrictnames():
    for key in districtDict.keys():
        showdistrictname.append(key)
    print(showdistrictname)

def getpinOfstreet(districtname):

    url = "https://xa.zu.anjuke.com/fangyuan/"+districtname
    head = {
    "method": "GET",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-language": "zh-CN,zh;q=0.9",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
}
    request = urllib.request.Request(url, headers=head)
    response = urllib.request.urlopen(request)
    html = response.read().decode("utf-8")
    bs = BeautifulSoup(html, "html.parser")
    districtinfos = bs.find_all('div',class_="sub-items sub-level2")[0]
    districtinfo = str(districtinfos)

    pattern1 = re.compile(r'<a href="https://xa.zu.anjuke.com/fangyuan/.*-q-(.*)/" title=".*">.*</a>', re.M)
    pattern2 = re.compile(r'<a href="https://xa.zu.anjuke.com/fangyuan/.*" title=".*">(.*)</a>', re.M)
    result1 = re.findall(pattern1, districtinfo)
    result2 = re.findall(pattern2, districtinfo)
    streetDict = dict(zip(result2,result1))
    return streetDict

def getpinOfdistrict():

    url = "https://xa.zu.anjuke.com/fangyuan/"
    head = {
    "method": "GET",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-language": "zh-CN,zh;q=0.9",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
}
    request = urllib.request.Request(url, headers=head)
    response = urllib.request.urlopen(request)
    html = response.read().decode("utf-8")
    bs = BeautifulSoup(html, "html.parser")
    districtinfos = bs.find_all('div',class_="sub-items sub-level1")[0]
    districtinfo = str(districtinfos)

    pattern1 = re.compile(r'<a href="https://xa.zu.anjuke.com/fangyuan/.*" title=".*">(.*)</a>', re.M)
    pattern2 = re.compile(r'<a href="https://xa.zu.anjuke.com/fangyuan/(.*)/" title=".*">.*</a>', re.M)
    result1 = re.findall(pattern1, districtinfo)
    result2 = re.findall(pattern2, districtinfo)
    districtDict = dict(zip(result1,result2))
    return districtDict

districtDict = getpinOfdistrict()
#各区所含街道以及对应的url作为键值对的字典
weiyangqDict = getpinOfstreet(districtDict["未央"])
yantaquDict = getpinOfstreet(districtDict["雁塔"])
gaoxinxaDict = getpinOfstreet(districtDict["高新区"])
jingkaiquxDict = getpinOfstreet(districtDict["经开区"])
lianhuquDict = getpinOfstreet(districtDict["莲湖"])
beilinquDict = getpinOfstreet(districtDict["碑林"])
changanbDict = getpinOfstreet(districtDict["长安"])
xinchengquDict = getpinOfstreet(districtDict["新城"])
qujiangxinquDict = getpinOfstreet(districtDict["曲江新区"])
baqiaoquDict = getpinOfstreet(districtDict["灞桥"])
gaolingDict = getpinOfstreet(districtDict["高陵"])
chanbaDict = getpinOfstreet(districtDict["浐灞"])
lintongquDict = getpinOfstreet(districtDict["临潼"])
xixianxinquDict = getpinOfstreet(districtDict["西咸新区"])
huyiquDict = getpinOfstreet(districtDict["鄠邑"])
daxingxinquDict = getpinOfstreet(districtDict["大兴新区"])
zhouzhixianDict = getpinOfstreet(districtDict["周至"])
lantianxianDict = getpinOfstreet(districtDict["蓝田"])
yanliangquDict = getpinOfstreet(districtDict["阎良"])
xianzhoubiancDict = getpinOfstreet(districtDict["西安周边"])
gjgwqxaDict = getpinOfstreet(districtDict["国际港务区"])

def showStreetnames(dict):
    for street in dict.keys():
        showstreetname.append(street)
    print(showstreetname)
def urlsearchBylocation():
    showDistrictnames()
    cndistrict = input("请输入区名：")
    pinyindistrict = districtDict[cndistrict]

    if cndistrict =="未央":
        showStreetnames(weiyangqDict)
    elif cndistrict =="雁塔":
        showStreetnames(yantaquDict)
    elif cndistrict =="高新区":
        showStreetnames(gaoxinxaDict)
    elif cndistrict =="经开区":
        showStreetnames(jingkaiquxDict)
    elif cndistrict =="莲湖":
        showStreetnames(lianhuquDict)
    elif cndistrict =="碑林":
        showStreetnames(beilinquDict)
    elif cndistrict =="长安":
        showStreetnames(changanbDict)
    elif cndistrict =="新城":
        showStreetnames(xinchengquDict)
    elif cndistrict =="曲江新区":
        showStreetnames(qujiangxinquDict)
    elif cndistrict =="灞桥":
        showStreetnames(baqiaoquDict)
    elif cndistrict =="高陵":
        showStreetnames(gaolingDict)
    elif cndistrict =="浐灞":
        showStreetnames(chanbaDict)
    elif cndistrict =="临潼":
        showStreetnames(lintongquDict)
    elif cndistrict =="西咸新区":
        showStreetnames(xixianxinquDict)
    elif cndistrict =="鄠邑":
        showStreetnames(huyiquDict)
    elif cndistrict =="大兴新区":
        showStreetnames(daxingxinquDict)
    elif cndistrict =="周至":
        showStreetnames(zhouzhixianDict)
    elif cndistrict =="蓝田":
        showStreetnames(lantianxianDict)
    elif cndistrict =="阎良":
        showStreetnames(yanliangquDict)
    elif cndistrict =="西安周边":
        showStreetnames(xianzhoubiancDict)
    elif cndistrict =="国际港务区":
        showStreetnames(gjgwqxaDict)

    cnstreet = input("请输入街道名：")
    if cnstreet in weiyangqDict:
        pinyinstreet = weiyangqDict[cnstreet]
    elif cnstreet in yantaquDict:
        pinyinstreet = yantaquDict[cnstreet]
    elif cnstreet in gaoxinxaDict:
        pinyinstreet = gaoxinxaDict[cnstreet]
    elif cnstreet in jingkaiquxDict:
        pinyinstreet = jingkaiquxDict[cnstreet]
    elif cnstreet in lianhuquDict:
        pinyinstreet = lianhuquDict[cnstreet]
    elif cnstreet in beilinquDict:
        pinyinstreet = beilinquDict[cnstreet]
    elif cnstreet in changanbDict:
        pinyinstreet = changanbDict[cnstreet]
    elif cnstreet in xinchengquDict:
        pinyinstreet = xinchengquDict[cnstreet]
    elif cnstreet in qujiangxinquDict:
        pinyinstreet = qujiangxinquDict[cnstreet]
    elif cnstreet in baqiaoquDict:
        pinyinstreet = baqiaoquDict[cnstreet]
    elif cnstreet in gaolingDict:
        pinyinstreet = gaolingDict[cnstreet]
    elif cnstreet in chanbaDict:
        pinyinstreet = chanbaDict[cnstreet]
    elif cnstreet in lintongquDict:
        pinyinstreet = lintongquDict[cnstreet]
    elif cnstreet in xixianxinquDict:
        pinyinstreet = xixianxinquDict[cnstreet]
    elif cnstreet in huyiquDict:
        pinyinstreet = huyiquDict[cnstreet]
    elif cnstreet in daxingxinquDict:
        pinyinstreet = daxingxinquDict[cnstreet]
    elif cnstreet in zhouzhixianDict:
        pinyinstreet = zhouzhixianDict[cnstreet]
    elif cnstreet in lantianxianDict:
        pinyinstreet = lantianxianDict[cnstreet]
    elif cnstreet in yanliangquDict:
        pinyinstreet = yanliangquDict[cnstreet]
    elif cnstreet in xianzhoubiancDict:
        pinyinstreet = xianzhoubiancDict[cnstreet]
    elif cnstreet in gjgwqxaDict:
        pinyinstreet = gjgwqxaDict[cnstreet]
    else:
        return "https://xa.zu.anjuke.com/fangyuan/changanb-q-dongda/"
    url2combine = "https://xa.zu.anjuke.com/fangyuan/" + pinyindistrict + "-q-" + pinyinstreet
    return url2combine

# MAIN PART
datalist = []
filename = '安居客未央大学城租房信息表.xls'
requesturl = urlsearchBylocation()
print(requesturl)
#url 4 database`s saving name
pattern_url4dbsv = re.compile(r'https://xa.zu.anjuke.com/fangyuan/(.*)')
url4dbsv = re.findall(pattern_url4dbsv, requesturl)
url4dbsv_rpd = url4dbsv[0].replace("-","_")
print(url4dbsv)

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

def initDb(url):
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
    '''%url
    # databaseName = "Anjuke-"+ locationIndex
    conn = sqlite3.connect("Anjuke_Data.db")
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    conn.close()

def insert2Db(datalist,url):
    #判断database文件是否存在
    filedir = './Anjuke_Data.db'
    initDb(url)
    conn = sqlite3.connect("Anjuke_Data.db")
    cur = conn.cursor()
    for data in datalist:
        for index in range(len(data)):
            if index == 1:
                continue
            data[index] = "'"+data[index]+"'"
        sql = '''
        insert into '%s' (title,price,structure,address,renttype,direction,elevator,detailsite)values(%s)''' %(url, ",".join(data))

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
    # saveData(datalist,filename) 以表格的形式储存
    insert2Db(datalist,url4dbsv_rpd)
