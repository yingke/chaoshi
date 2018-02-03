#获取本地超市消费记录
#通过Fiddler 获取手机APP 请求接口 用python 分析 并存入数据库

import requests
import time
import json
import pymongo

headers = {
    'Appkey': '',
    'Appversion': '3.4.02',
    'Os': 'android',
    'Osversion': '7.1.1',
    'servername': 'online',
    'Unique': '',
    'Userid': '',
    'Usersession': ''
}



def getorders():

    connection = pymongo.MongoClient('localhost', 27017)
    # 连接airdata数据库，没有则自动创建
    tdb = connection.jialeyuan
    # 连接airdatas 集合 没有则自动创建
    post = tdb.Orders

    i = 1

    while(i < 8):
        ordersurl = 'http://www.subuy.com/api/jointorders/newOrders?page={i}&per_page=10&parentids=&rangeId=1'.format(i=i)

        orders = requests.get(ordersurl, headers=headers)


        i += 1
        text = json.loads(orders.text)
        ordersjson = text['dataList']

        for jsonor in ordersjson:

            orsertime = jsonor['time']
            transactionNo = jsonor['transactionNo']

            detail = getCustDetail(time, transactionNo)

            alloders= dict(jsonor, **detail)
            post.insert(alloders)



            time.sleep(5)



def getCustDetail(time,transactionNo):

    postheaders = {
        'Appkey': '',
        'Appversion': '3.4.02',
        'Os': 'android',
        'Osversion': '7.1.1',
        'servername': 'online',
        'Unique': '',
        'Userid': '',
        'Usersession': '',
        'Content - Length': '59',
         'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'www.subuy.com',
        'Connection': 'Keep - Alive'
    }
    params = {'createTime': time, 'transactionNo': transactionNo}

    detali = requests.post('http://www.subuy.com/api/jointorders/getCustDetail', data=params ,headers=headers)

    time.sleep(5)

    return json.loads(detali.text)







if __name__ == '__main__':

    getorders()