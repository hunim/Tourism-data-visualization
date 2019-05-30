# Tourism-data-visualization
去哪儿旅游数据可视化
>之前一段时间把毕业论文搞完了。帮学弟对旅游景点的数据进行可视化的展示

### 一、数据准备
这里使用的是去哪儿的旅游数据，参考的是大吉大利小米酱的简书[https://www.jianshu.com/p/b7627e67b6b9](https://www.jianshu.com/p/b7627e67b6b9)有兴趣的可以去看看。[大吉大利小米酱](https://www.jianshu.com/u/8e45f2f3b6c1)
简书写的俏皮风趣（吾辈之楷模）。
```
import time,requests, re
from lxml import etree
import pandas as pd

def getPage(url):
    headers = {
        'Accept':'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection':'keep-alive',
        'cookie':'QN1=dXrghVzaM0cN+wYpRryRAg==; QN269=9B0D2CC075F511E9BCA9FA163ED025F3; _i=ueHd8xMxBTVXqvCA4qR470Um5eyX; QunarGlobal=10.86.213.150_21340582_16ab448be93_7a80|1557803849001; QN99=647; fid=eda14267-76af-406d-975d-9e098c9d50f4; __utma=183398822.428737805.1557803850.1557803850.1557803850.1; __utmz=183398822.1557803850.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic|utmctr=%E5%A5%BD123%E6%97%85%E6%B8%B8; _jzqa=1.1924495795568354000.1557803852.1557803852.1557803852.1; _jzqx=1.1557803852.1557803852.1.jzqsr=hotel%2Equnar%2Ecom|jzqct=/.-; QN71="NTguMjQzLjI1NC4xMjk65a6J5b69OjE="; QN57=15578038546700.26539516250028505; QN67=1211; cto_lwid=06e141f7-870f-42ca-9519-312c3587bed8; QN63=%E7%83%AD%E9%97%A8%E6%99%AF%E7%82%B9%7C%E5%AE%89%E5%BE%BD; csrfToken=ZrtgmFh4YnLvKzqP8dCzzti2JoLh7sFz; _vi=3di8PYGZ-R9GtBBMOJN2tlBVR_KX-2jyHo6YmCS3JC-NB1B9rZnnrT7ZlQIEIdYWcInEmtNp0xdr9Aaf4mU9WCoN7q_-8QEnQ3m2goXxwFZpqYH8gGaupHTLFP-ak8JMAES3K_yVSwvsNpRb_qYHXgc4xajzIvF93Hnj_YkbVQDN; Hm_lvt_15577700f8ecddb1a927813c81166ade=1557803855,1558319263; QN300=auto_4e0d874a; QN205=auto_4e0d874a; QN277=auto_4e0d874a; QN267=79056878cd9f7ec1; QN58=1558319262033%7C1558319518464%7C2; Hm_lpvt_15577700f8ecddb1a927813c81166ade=1558319519; JSESSIONID=A509706026389E421E058210F3BEF192; Request-Node=f6769d42991e67d1c5a98893de33d1f3; QN271=06f7c456-ac81-4bdb-b833-ddfbc81ab633',
        'Host':'piao.qunar.com',
        'Referer':'http://piao.qunar.com/ticket/list.htm?keyword=%E7%83%AD%E9%97%'
                  'A8%E6%99%AF%E7%82%B9&region=&from=mpl_search_suggest',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        'X-Requested-With':'XMLHttpRequest'
    }
    try:
        page = requests.get(url,headers = headers)
        print("page:")
        print(page)
        return page
    except Exception as e:
        print(str(e))

def getList():
    place = '热门景点'
    url = 'http://piao.qunar.com/ticket/list.htm?keyword='+ place +'&region=&from=mpl_search_suggest&page={}'
    i = 1
    sightlist = []
    while i < 3000:
        page = getPage(url.format(i))
        selector = etree.HTML(page.text)
        print('正在爬取第', str(i), '页景点信息')
        i += 1
        informations = selector.xpath('//div[@class="result_list"]/div')
        for inf in informations:
            try:
                sight_name = inf.xpath('./div/div/h3/a/text()')[0]
                sight_level = inf.xpath('.//span[@class="level"]/text()')
                if len(sight_level):
                    sight_level = sight_level[0].replace('景区','')
                else:
                    sight_level = 0
                sight_area = inf.xpath('.//span[@class="area"]/a/text()')[0]
                sight_hot = inf.xpath('.//span[@class="product_star_level"]//span/text()')[0].replace('热度 ','')
                sight_add = inf.xpath('.//p[@class="address color999"]/span/text()')[0]
                sight_add = re.sub('地址：|（.*?）|\(.*?\)|，.*?$|\/.*?$','',str(sight_add))
                sight_slogen = inf.xpath('.//div[@class="intro color999"]/text()')[0]
                sight_price = inf.xpath('.//span[@class="sight_item_price"]/em/text()')
                if len(sight_price):
                    sight_price = sight_price[0]
                else:
                    i = 0
                    break
                sight_soldnum = inf.xpath('.//span[@class="hot_num"]/text()')[0]
                sight_point = inf.xpath('./@data-point')[0]
                sight_url = inf.xpath('.//h3/a[@class="name"]/@href')[0]
                sightlist.append([sight_name,sight_level,sight_area,float(sight_price),int(sight_soldnum),float(sight_hot),sight_add.replace('地址：',''),sight_point,sight_slogen,sight_url])
                print("sightlist:")
                print(sightlist)
            except IndexError:
                pass

        time.sleep(10)
    return sightlist

def listToExcel(list,name):
    df = pd.DataFrame(list,columns=['景点名称','级别','所在区域','起步价','销售量','热度','地址','经纬度','标语','详情网址'])
    df.to_csv(name + ".csv", sep=',')

def main():
    sightlist = getList()
    listToExcel(sightlist,'hotplace')

if __name__=='__main__':
	main()
```
在pycharm中运行代码。将去哪儿网中热门的景点数据进行爬去保存为.csv数据，包括景点名称、级别、所在地区等信息。
![热门景点数据](https://upload-images.jianshu.io/upload_images/7393424-8bbf3162d4cbe49a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

但是这些数据并不能进行直接的可视化（这里小米酱将爬去的数据用python转换成json文件，用echart进行可视化）。
![小米酱的可视化](https://upload-images.jianshu.io/upload_images/7393424-ae15403e6098cd28.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### 二、数据处理工作
为了更好的将数据进行可视化。我们把csv数据做了分列处理，将经纬度分为两行。
![经纬度分列](https://upload-images.jianshu.io/upload_images/7393424-e8f97c3385a4c931.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![分列后](https://upload-images.jianshu.io/upload_images/7393424-899b93451be92711.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
然后将数据导入ArcMap中，在ArcMap中将景点数据转化为shp格式的点数据。
![i显示X、Y数据](https://upload-images.jianshu.io/upload_images/7393424-6dd541e60acaf1f6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
点击按X、Y显示数据后，X、Y字段和输入坐标的坐标系（我选的是WGS84）
![设置参数](https://upload-images.jianshu.io/upload_images/7393424-121b1a6426571523.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
点击确定，就可以将数据转换为shp格式的point数据（经纬度坐标值不能搞错了）。为了确保没有错，最好加载在线的地图确认数据转换的正确性。
![经纬度数据错误效果](https://upload-images.jianshu.io/upload_images/7393424-a5a1ca2770da821a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![数据转换](https://upload-images.jianshu.io/upload_images/7393424-632225a536b1eff3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
（POI数据也可以通过此方法转换为shp数据）然后将数据导出为shp即可。

### 三、数据可视化
>本次将数据转化为GeoJSON数据，通过leaflets的API进行展示。包括热力图、弹窗、标注、定位搜索。
![代码界面](https://upload-images.jianshu.io/upload_images/7393424-5078b6c471f38588.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![可视化效果](https://upload-images.jianshu.io/upload_images/7393424-3d949188240da132.gif?imageMogr2/auto-orient/strip)
