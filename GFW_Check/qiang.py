#-*- coding=utf-8 -*-
"""
Author: Abbey
Create Date: 2019-05-27
Script Description: 检测域名是否被墙
"""
import requests
import json
import time

class Qiang(object):
    """docstring for Qiang"""
    def __init__(self, domain):
        self.domain = domain
        self.session=requests.Session()
        self.session.headers={
            'Origin': 'https://00738.com',
            'Referer': 'https://00738.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
        }
        self.GetToken()

    def GetToken(self):
        url='https://cx.dtmqnx.com/domain/Api/getcode?_ajax=1&type=bq&rand=_{}'.format(int(time.time()*1000))
        self.session.options(url)
        r=self.session.post(url,data={'domains':self.domain})
        self.token=json.loads(r.text).get('token')

    def Query(self):
        url='https://cx.dtmqnx.com/domain/Api/check?_ajax=1&rand=_{}'.format(int(time.time()*1000))
        self.session.options(url)
        r=self.session.post(url,data={'token':self.token})
        data=json.loads(r.text)
        return data

    def main(self):
        rdata=[]
        for i in range(10):
            data=self.Query()
            bd=data.get('data').get('gfw')
            rdata.append(bd)
            print('第{}次查询，被墙域名：{}'.format(i+1,bd))
        return sum([self.domain in i for i in rdata])>0

if __name__=='__main__':
    q=Qiang(domain='google.com')
    block='被墙' if q.main() else '未被墙'
    print('{}查询结果：{}'.format(q.domain,block))
