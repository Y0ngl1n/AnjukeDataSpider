import urllib.request
from bs4 import BeautifulSoup
import ssl
import re
import time
import xlwt
import sqlite3

ssl._create_default_https_context = ssl._create_unverified_context
showdistrictname = []
showstreetname = []
districtDict = {"未央": "weiyangq", "雁塔": "yantaqu", "高新区": "gaoxinxa", "经开区": "jingkaiqux", "莲湖": "lianhuqu",
                "碑林": "beilinqu", "长安": "changanb", "新城": "xinchengqu", "曲江新区": "qujiangxinqu", "灞桥": "baqiaoqu",
                "高陵": "gaoling", "浐灞": "chanba", "临潼": "lintongqu", "西咸新区": "xixianxinqu", "鄠邑": "huyiqu",
                "大兴新区": "daxingxinqu", "周至": "zhouzhixian", "蓝田": "lantianxian", "阎良": "yanliangqu",
                "西安周边": "xianzhoubianc", "国际港务区": "gjgwqxa", }
def showDistrictnames():
    for key in districtDict.keys():
        showdistrictname.append(key)
    print(showdistrictname)

#通过re匹配网页中街道与拼音一一对应关系组成字典
# def getpinOfstreet(districtname):
#
#     url = "https://xa.zu.anjuke.com/fangyuan/"+districtname
#     head = {
#     "method": "GET",
#     "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
#     "accept-language": "zh-CN,zh;q=0.9",
#     "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
# }
#     request = urllib.request.Request(url, headers=head)
#     response = urllib.request.urlopen(request)
#     html = response.read().decode("utf-8")
#     bs = BeautifulSoup(html, "html.parser")
#     districtinfos = bs.find_all('div',class_="sub-items sub-level2")[0]
#     districtinfo = str(districtinfos)
#
#     pattern1 = re.compile(r'<a href="https://xa.zu.anjuke.com/fangyuan/.*-q-(.*)/" title=".*">.*</a>', re.M)
#     pattern2 = re.compile(r'<a href="https://xa.zu.anjuke.com/fangyuan/.*" title=".*">(.*)</a>', re.M)
#     result1 = re.findall(pattern1, districtinfo)
#     result2 = re.findall(pattern2, districtinfo)
#     streetDict = dict(zip(result2,result1))
#
#     return streetDict


#通过网页匹配到区名与对应拼音，返回字典
# def getpinOfdistrict():
#
#     url = "https://xa.zu.anjuke.com/fangyuan/"
#     head = {
#     "method": "GET",
#     "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
#     "accept-language": "zh-CN,zh;q=0.9",
#     "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
# }
#     request = urllib.request.Request(url, headers=head)
#     response = urllib.request.urlopen(request)
#     html = response.read().decode("utf-8")
#     bs = BeautifulSoup(html, "html.parser")
#     districtinfos = bs.find_all('div',class_="sub-items sub-level1")[0]
#     districtinfo = str(districtinfos)
#
#     pattern1 = re.compile(r'<a href="https://xa.zu.anjuke.com/fangyuan/.*" title=".*">(.*)</a>', re.M)
#     pattern2 = re.compile(r'<a href="https://xa.zu.anjuke.com/fangyuan/(.*)/" title=".*">.*</a>', re.M)
#     result1 = re.findall(pattern1, districtinfo)
#     result2 = re.findall(pattern2, districtinfo)
#     districtDict = dict(zip(result1,result2))
#     return districtDict

#各区所含街道以及对应的url作为键值对的字典
#weiyangqDict = getpinOfstreet(districtDict["未央"])   获取每个区对应的街道汉字拼音键值对组成的字典
weiyangqDict = {'阿房宫遗址': 'afgyizhi', '北二环西段': 'behxdxa', '大明宫': 'dmgxa', '二府庄': 'erfuzhuang', '方新村': 'fangxincun', '经济技术开发区': 'jingjijskfq', '明光南路': 'xagml', '三桥': 'sanqiao', '太元路': 'xatyl', '太华北路': 'thblxa', '文景南路': 'wenjinglu', '玄武东路': 'xalhc', '辛家庙': 'xinjiamao', '皂河': 'zaohe'}

yantaquDict = {'北山门': 'beishanmen', '翠华路': 'cuihualuxa', '城南客运站': 'cnkyzxa', '长安西路': 'caxlxa', '电子一路': 'xadzyl', '电视塔': 'dianshita', '大雁塔': 'dayanta', '电子城': 'dianzicheng', '电子正街': 'dianzizhengjie', '等驾坡': 'dengjiapo', '东仪路': 'dylxa', '国展中心': 'guozhanzhongxin', '含光路': 'xahgl', '后村西路': 'hcxlxa', '吉祥诚信商业街': 'xajxcx', '吉祥村': 'jixianglu', '明德门': 'mingdemen', '青龙寺': 'xaqls', '青松路': 'xaqsl', '三森国际家俱城': 'sanyao', '太白南路': 'tbnlxa', '西斜七路': 'xaxxql', '西影路': 'xiyinglu', '小寨': 'xiaozhailu', '雁塔西路': 'xaytxl', '永松路': 'yongsonglu', '雁环中路': 'yhzlxa'}

gaoxinxaDict = {'创业园': 'cyyxa', '大寨路': 'xadzl', '都市之门': 'dushizhimen', '二环南路西段': 'xaehnl', '高新管委会': 'xagxgwh', '高新六路': 'xagxll', '高新一中': 'xagxyz', '高新三小': 'gaoxinerlu', '高新路': 'gaoxinlu', '光华路': 'guanghualu', '高新四路': 'gaoxinsilu', '锦业路': 'jylxa', '科技六路': 'xakjll', '昆明路': 'xakml', '科技四路西段': 'kejisilu', '科技路西口': 'kejiluxikou', '科技路中段': 'kjlzdxa', '科技西路': 'kjxlxa', '科技西路西段': 'kjxlxdxa', '科技路': 'kjlxa', '绿地世纪城': 'lvdishijiecheng', '木塔寺公园': 'mtsgyxa', '软件园': 'rjyxa', '陕西大会堂': 'shanxidahuitang', '唐延路': 'tylxa', '旺座现代城': 'wangzuoxdc', '逸翠园': 'ycyxa', '鱼化寨': 'yhzxa', '丈八东路': 'xazbdl', '丈八北路': 'zhangbaxilu', '紫薇田园都市': 'ziweitianyuandushi', '丈八西路': 'zbxlxa'}

jingkaiquxDict = {'百花村': 'bhcxa', '北苑': 'byxa', '北客站': 'beikezhan', '城市运动公园': 'xacsydgy', '长安医院': 'cayyxa', '常青路': 'cqlxa', '草滩': 'caotan', '凤城五路': 'xafcwl', '汉城湖': 'hchxa', '汉城商业街': 'hcsyjxa', '经发学校北区': 'jfxxbqxa', '经发学校南区': 'jfxxnqxa', '市图书馆': 'xastsg', '未央湖': 'weiyanglu', '西安中学': 'xazx', '西安第三医院': 'xadsyyxa', '徐家湾': 'xujiawan', '行政中心': 'xingzhenghzongxin', '永城路': 'yclxa', '张家堡': 'zhangjiabao'}

lianhuquDict = {'北院门': 'beiyuanmen', '北大街': 'beidajiexa', '北关': 'beiguanxa', '城西客运站': 'chengxikeyunzhan', '大白杨': 'xaxby', '大庆路': 'xadql', '大唐西市': 'datangxishixa', '丰庆路': 'qingfenglu', '丰庆公园': 'fqgyxa', '汉城路': 'hanchenglu', '红庙坡': 'hongmiaopo', '红光路': 'hglxa', '锦园小区': 'jinyuanxiaoqu', '开远门': 'kaiyuanmen', '劳动路': 'laodonglu', '莲湖公园': 'lianhugognyuan', '龙首村': 'longshoucun', '南小巷': 'nxxxa', '洒金桥': 'sjqxa', '甜水井': 'tianshuijing', '土门': 'tumenxa', '桃园路': 'taoyuanlu', '西大街': 'xidajie', '西关正街': 'xiguanxa', '西稍门': 'xishaomen', '玉祥门': 'xayxm', '枣园': 'zaoyuan'}

beilinquDict = {'边家村': 'bianjiacun', '长乐坊': 'changlefang', '东大街': 'dongdajie', '大差市': 'dachashi', '东关南街': 'dongguannanjie', '大学南路': 'daxuenanlu', '东关正街': 'dgzjxa', '广济街': 'guangjijie', '和平路': 'xahepinglu', '红缨路': 'zhangjiacun', '何家村': 'hejiacun', '环城南路': 'huanchengnanlu', '互助路立交': 'huzhululijiao', '李家村': 'lijiacun', '南大街': 'nandajie', '南门': 'nanmenxa', '南稍门': 'nanshaomen', '体育场': 'tiyuchang', '太乙路': 'taiyilu', '太白立交': 'tbljxa', '文艺路': 'wenyiluxa', '西安交通大学': 'xajtdx', '西工大': 'xigognda', '小雁塔': 'xiaoyanta', '友谊东路': 'xayydl', '友谊西路': 'xayyxl'}

changanbDict = {'长安广场': 'changanguangchang', '大学城': 'dongda', '东长安街': 'dongchanganjie', '凤栖原': 'fengxiyuan', '富力城': 'flcxa', '郭杜': 'guodu', '航天城': 'hangtiancheng', '航天一小': 'htyxxa', '绿源十字': 'lvyuanshizi', '韦曲': 'weiqu', '西长安街': 'xichanganjie', '西沣路': 'xflxa', '西寨': 'xzxa', '子午大道': 'ziwu'}

xinchengquDict = {'八府庄': 'bafuzhuang', '朝阳门': 'chaoyangmenxa', '长乐中路': 'changlezhonglu', '东五路': 'dongwulu', '华清路': 'xahql', '韩森寨': 'hansensai', '胡家庙': 'hujiamiao', '含元路': 'hanyuanlu', '建工路': 'xajgl', '解放路': 'jiefangluxa', '金花路': 'jinhualu', '金花南路': 'jhnlxa', '建国路': 'jglxa', '矿山路': 'xaksl', '康复路': 'kangfulu', '民乐园': 'mlyxa', '尚勤路': 'shangqinlu', '通化门': 'tonghuamen', '五路口': 'wulukou', '文昌门': 'wenchangmen', '万寿路': 'wanshoulu', '中山门': 'zhongshanmen', '自强东路': 'ziqianglu', '自强西路': 'zqxlxa'}

qujiangxinquDict = {'北池头': 'xabct', '翠华南路': 'xachnl', '创意谷': 'cygxa', '大唐芙蓉园': 'xadtfry', '芙蓉东路': 'xafrdl', '芙蓉西路': 'xafrxl', '公园南路': 'gynlxa', '寒窑路': 'hanyaolu', '海洋馆': 'xahyg', '交大曲江校区': 'xayxl', '金泘沱': 'jftxa', '龙湖星悦荟': 'lhxyhxa', '南湖': 'xaqjc', '曲江城市运动公园': 'qjcsydgyxa', '曲江三小': 'qjsxx', '曲江四小': 'qujiangsixiao', '曲江一中': 'qjyzxa', '陕师大': 'ssdxa', '行政商务中心': 'xaxzswzx', '新开门': 'xaxkm', '雁南三路': 'xaynsl', '雁南四路': 'xaynsil', '雁南五路': 'xaynwl', '雁展路': 'xayzl', '雁塔南路': 'ytnlxa'}

baqiaoquDict = {'安装四处': 'dongchengtaoyuan', '半坡立交': 'xabplj', '长乐坡': 'xaclp', '浐河东路': 'xasadf', '浐河西路': 'longhuxiangxing', '纺织城': 'fangzhicheng', '红旗': 'hongqixa', '洪庆': 'hongqing', '世博园': 'shiyuangongguan', '水香路': 'chanbaxincheng', '田家湾': 'xahdlz', '席王': 'xiwang', '御锦城': 'yujincheng'}

gaolingDict = {'高陵城区': 'gaolinxian', '泾河工业园': 'jhgyyxa', '泾渭新城': 'jwxcxa', '原点新城': 'ydxcxa'}

chanbaDict = {'灞河西路': 'xabhxl', '灞桥周边': 'baqiaozhoubian', '浐灞二路': 'elxa', '浐灞半岛': 'chanbabandao', '城北大学城': 'chengbeidaxuecheng', '广泰门': 'xahdmd', '十里铺': 'shilipu', '桃花潭': 'xathy', '西安国际会展中心': 'xianguojihzzx'}

lintongquDict = {'代王': 'daiwang', '骊山': 'lishanxa', '临潼周边': 'lintongzhoubian', '秦陵': 'qinling', '新丰': 'xinfengxa', '斜口': 'xiekou', '行者': 'xingzhe'}

xixianxinquDict = {'沣东新城': 'fdxcxa', '沣西新城': 'fxxcxa'}

huyiquDict = {'鄠邑城区': 'huxian'}

daxingxinquDict = {'大兴东路': 'dxdlxa', '丰禾路': 'fenghelu', '梨园路': 'lylxa'}

zhouzhixianDict = {'周至': 'zhouzhixian'}

lantianxianDict = {'蓝田城区': 'lantianxian'}

yanliangquDict = {'凤凰路': 'fenghuanglu', '关山': 'guanshan', '武屯': 'wudun', '新华路': 'xinhualuxa', '阎良周边': 'yanliangzhoubian'}

xianzhoubiancDict = {'咸阳': 'xianyangxa'}

gjgwqxaDict = {'保税区': 'baoishuiquxa', '港务大道': 'gangwudadao', '西安奥体中心': 'xianaotizhongxin', '西航花园': 'xihanghuayuan'}


def showStreetnames(dict):
    for street in dict.keys():
        showstreetname.append(street)
    print(showstreetname)
def urlsearchBylocation():
    showDistrictnames()
    cndistrict = input("请输入上方要查询的区名：")
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
    else :
        #default:WeiyangDistrict
        showStreetnames(weiyangqDict)

    cnstreet = input("请输入上方街道或具体位置：")
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

requesturl = urlsearchBylocation()
#url 4 database`s saving name
pattern_url4dbsv = re.compile(r'https://xa.zu.anjuke.com/fangyuan/(.*)')
url4dbsv = re.findall(pattern_url4dbsv, requesturl)
url4dbsv_rpd = url4dbsv[0].replace("-","_")


def geturlhtml(requesturl,datalist):
    head = {
        "method":"GET","accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9","accept-language":"zh-CN,zh;q=0.9","user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
    }
    for i in range(30):
        print("第%d页"%(i+1))
        url = requesturl+"/p"+str(i+1)+"/"
        request = urllib.request.Request(url,headers=head)
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        datalistresult = getHouseinfo(html,datalist)

    print("共%d房源"%(len(datalistresult)))
def getHouseinfo(html,datalist):
    bs = BeautifulSoup(html,"html.parser")

    houseinfos = bs.find_all('div',class_="zu-itemmod")
    if houseinfos != []:
        lenhouseinfos = len(houseinfos)
        print("该页：%d房源"%lenhouseinfos)
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

#存入xls
def save2xls(datalist,url):
    workbook = xlwt.Workbook(encoding="utf-8")
    worksheet = workbook.add_sheet("sheet_anjuke",cell_overwrite_ok=True)
    col = ('标题','价格','户型面积','地址','租房类型','朝向','有无电梯','详情页')
    for i in range(len(col)):
        worksheet.write(0,i,col[i])
    for j in range(len(datalist)):
        data = datalist[j]
        for k in range(len(data)):
            worksheet.write(j+1,k,data[k])
    excelname = url + ".xls"
    workbook.save(excelname)
    print("保存数据成功")

def initDb(url):
    #初始化数据库结构
    try:
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
        conn = sqlite3.connect("Anjuke_Data.db")
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        conn.close()
    except Exception as e:
        sql = "drop table '%s'"%url
        conn = sqlite3.connect("Anjuke_Data.db")
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()

        sql2 = '''
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
                ''' % url
        cur.execute(sql2)
        conn.commit()
        conn.close()

def insert2Db(datalist,url):
    #判断database文件是否存在

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
    save_type = input("保存到数据库请输入1，保存到excel表格请输入2:")
    if save_type == "1":
        insert2Db(datalist,url4dbsv_rpd)
    elif save_type == "2":
        save2xls(datalist,url4dbsv_rpd)

