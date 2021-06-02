import urllib.request
from bs4 import BeautifulSoup
import ssl
import re


ssl._create_default_https_context = ssl._create_unverified_context
districtDict = {"未央": "weiyangq", "雁塔": "yantaqu", "高新": "gaoxinxa", "经开区": "jingkaiqux", "莲湖": "lianhuqu",
                "碑林": "beilinqu", "长安": "changanb", "新城": "xinchengqu", "曲江新区": "qujiangxinqu", "灞桥": "baqiaoqu",
                "高陵": "gaoling", "浐灞": "chanba", "临潼": "lintongqu", "西咸新区": "xixianxinqu", "鄠邑": "huyiqu",
                "大兴新区": "daxingxinqu", "周至": "zhouzhixian", "蓝田": "lantianxian", "阎良": "yanliangqu",
                "西安周边": "xianzhoubianc", "国际港务区": "gjgwqxa", }



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


def urlsearchBylocation():
    cndistrict = input("请输入区名：")
    pinyindistrict = districtDict[cndistrict]
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
# finalresult = getpinyinOfdistrict(districtDict["未央"])
# print(finalresult)
# finalresult = getpinOfdistrict()
# print(finalresult)
# print(districtDict)
# requesturl = urlsearchBylocation()
# print(requesturl)
