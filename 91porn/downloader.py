#-*- coding=utf-8 -*-
import requests
import threading
import os
import random
import math

def randip():
    return str(random.randint(0, 255)) + "."\
            + str(random.randint(0, 255)) + "."\
            + str(random.randint(0, 255)) + "."\
            + str(random.randint(0, 255))


class Downloader:
    def __init__(self,url,path,picture,title,id,offset=327680*10):
        self.url=url
        self.offset=offset
        self.path=path
        self.picture=picture
        self.title=title
        self.id=id
        r = requests.head(self.url)
        self.total = int(r.headers['Content-Length'])
        print(u'{} total size is {}'.format(self.title,self.total))

    def get_range(self):
        ranges=[]
        self.num=int(math.floor(self.total/self.offset)+1)
        for i in range(self.num):
            if i==self.num-1:
                ranges.append((i*self.offset,self.total))
            else:
                ranges.append((i*self.offset,(i+1)*self.offset))
        return ranges

    def download(self,start,end):
        #拼接Range字段,accept字段支持所有编码
        headers={'Range':'Bytes=%s-%s' % (start,end),'Accept-Encoding':'*','X-Forwarded-For':randip()}
        res = requests.get(self.url,headers=headers)
        print(u'{} download percent {}%'.format(self.title,round(float(end)/self.total,3)*100))
        #seek到start位置
        self.fd.seek(start)
        self.fd.write(res.content)

    def run(self):
        # 保存文件打开对象
        self.fd =  open(self.path,'wb')
        thread_list = []
        #一个数字,用来标记打印每个线程
        n = 0
        for ran in self.get_range():
            start,end = ran
            n+=1
            #创建线程 传参,处理函数为download
            thread = threading.Thread(target=self.download,args=(start,end))
            #启动
            thread.start()
            thread_list.append(thread)
        for i in thread_list:
            # 设置等待
            i.join()
        print(u'download %s load success'%(self.path))
        #关闭文件
        self.fd.close()
        with open('history.txt','a') as f:
            f.write('{}\n'.format(self.id))
