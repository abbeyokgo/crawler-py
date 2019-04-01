#-*- coding=utf-8 -*-
import requests
import re
import os
import sys
import argparse
import datetime
import logging
import time
import random
import string
import execjs
import threading
from downloader import downloader

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
           'X-Forwarded-For': '', 'Accept-Language': 'zh-CN,zh;q=0.8'}
info_reg = re.compile(
    '''<div class="imagechannel[\W\w]*?<a target=blank href="(http://.*?91porn\.com/view_video.*?\.php\?viewkey=.*?)">[\W\w]*?<img src="(.*?)" width.*? title="(.*?)" />''')
mp4_reg = re.compile("""<source src='(.*?)' type='video/mp4'>""")
chars = string.ascii_letters

basedir=os.path.abspath('.')
video_path=os.path.join(basedir,'video')
if not os.path.exists(video_path):
    os.mkdir(video_path)

#找国内可用网址到这里：https://www.ebay.com/usr/91dizhi_1
porn91_url = 'http://91porn.com'
info_list=[]

js="""var encode_version = 'sojson.v5', lbbpm = '__0x33ad7',  __0x33ad7=['QMOTw6XDtVE=','w5XDgsORw5LCuQ==','wojDrWTChFU=','dkdJACw=','w6zDpXDDvsKVwqA=','ZifCsh85fsKaXsOOWg==','RcOvw47DghzDuA==','w7siYTLCnw=='];(function(_0x94dee0,_0x4a3b74){var _0x588ae7=function(_0x32b32e){while(--_0x32b32e){_0x94dee0['push'](_0x94dee0['shift']());}};_0x588ae7(++_0x4a3b74);}(__0x33ad7,0x8f));var _0x5b60=function(_0x4d4456,_0x5a24e3){_0x4d4456=_0x4d4456-0x0;var _0xa82079=__0x33ad7[_0x4d4456];if(_0x5b60['initialized']===undefined){(function(){var _0xef6e0=typeof window!=='undefined'?window:typeof process==='object'&&typeof require==='function'&&typeof global==='object'?global:this;var _0x221728='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=';_0xef6e0['atob']||(_0xef6e0['atob']=function(_0x4bb81e){var _0x1c1b59=String(_0x4bb81e)['replace'](/=+$/,'');for(var _0x5e3437=0x0,_0x2da204,_0x1f23f4,_0x3f19c1=0x0,_0x3fb8a7='';_0x1f23f4=_0x1c1b59['charAt'](_0x3f19c1++);~_0x1f23f4&&(_0x2da204=_0x5e3437%0x4?_0x2da204*0x40+_0x1f23f4:_0x1f23f4,_0x5e3437++%0x4)?_0x3fb8a7+=String['fromCharCode'](0xff&_0x2da204>>(-0x2*_0x5e3437&0x6)):0x0){_0x1f23f4=_0x221728['indexOf'](_0x1f23f4);}return _0x3fb8a7;});}());var _0x43712e=function(_0x2e9442,_0x305a3a){var _0x3702d8=[],_0x234ad1=0x0,_0xd45a92,_0x5a1bee='',_0x4a894e='';_0x2e9442=atob(_0x2e9442);for(var _0x67ab0e=0x0,_0x1753b1=_0x2e9442['length'];_0x67ab0e<_0x1753b1;_0x67ab0e++){_0x4a894e+='%'+('00'+_0x2e9442['charCodeAt'](_0x67ab0e)['toString'](0x10))['slice'](-0x2);}_0x2e9442=decodeURIComponent(_0x4a894e);for(var _0x246dd5=0x0;_0x246dd5<0x100;_0x246dd5++){_0x3702d8[_0x246dd5]=_0x246dd5;}for(_0x246dd5=0x0;_0x246dd5<0x100;_0x246dd5++){_0x234ad1=(_0x234ad1+_0x3702d8[_0x246dd5]+_0x305a3a['charCodeAt'](_0x246dd5%_0x305a3a['length']))%0x100;_0xd45a92=_0x3702d8[_0x246dd5];_0x3702d8[_0x246dd5]=_0x3702d8[_0x234ad1];_0x3702d8[_0x234ad1]=_0xd45a92;}_0x246dd5=0x0;_0x234ad1=0x0;for(var _0x39e824=0x0;_0x39e824<_0x2e9442['length'];_0x39e824++){_0x246dd5=(_0x246dd5+0x1)%0x100;_0x234ad1=(_0x234ad1+_0x3702d8[_0x246dd5])%0x100;_0xd45a92=_0x3702d8[_0x246dd5];_0x3702d8[_0x246dd5]=_0x3702d8[_0x234ad1];_0x3702d8[_0x234ad1]=_0xd45a92;_0x5a1bee+=String['fromCharCode'](_0x2e9442['charCodeAt'](_0x39e824)^_0x3702d8[(_0x3702d8[_0x246dd5]+_0x3702d8[_0x234ad1])%0x100]);}return _0x5a1bee;};_0x5b60['rc4']=_0x43712e;_0x5b60['data']={};_0x5b60['initialized']=!![];}var _0x4be5de=_0x5b60['data'][_0x4d4456];if(_0x4be5de===undefined){if(_0x5b60['once']===undefined){_0x5b60['once']=!![];}_0xa82079=_0x5b60['rc4'](_0xa82079,_0x5a24e3);_0x5b60['data'][_0x4d4456]=_0xa82079;}else{_0xa82079=_0x4be5de;}return _0xa82079;};if(typeof encode_version!=='undefined'&&encode_version==='sojson.v5'){function strencode(_0x50cb35,_0x1e821d){var _0x59f053={'MDWYS':'0|4|1|3|2','uyGXL':function _0x3726b1(_0x2b01e8,_0x53b357){return _0x2b01e8(_0x53b357);},'otDTt':function _0x4f6396(_0x33a2eb,_0x5aa7c9){return _0x33a2eb<_0x5aa7c9;},'tPPtN':function _0x3a63ea(_0x1546a9,_0x3fa992){return _0x1546a9%_0x3fa992;}};var _0xd6483c=_0x59f053[_0x5b60('0x0','cEiQ')][_0x5b60('0x1','&]Gi')]('|'),_0x1a3127=0x0;while(!![]){switch(_0xd6483c[_0x1a3127++]){case'0':_0x50cb35=_0x59f053[_0x5b60('0x2','ofbL')](atob,_0x50cb35);continue;case'1':code='';continue;case'2':return _0x59f053[_0x5b60('0x3','mLzQ')](atob,code);case'3':for(i=0x0;_0x59f053[_0x5b60('0x4','J2rX')](i,_0x50cb35[_0x5b60('0x5','Z(CX')]);i++){k=_0x59f053['tPPtN'](i,len);code+=String['fromCharCode'](_0x50cb35[_0x5b60('0x6','s4(u')](i)^_0x1e821d['charCodeAt'](k));}continue;case'4':len=_0x1e821d[_0x5b60('0x7','!Mys')];continue;}break;}}}else{alert('');};"""

def Decrypt(content):
    ctx=execjs.compile(js)
    encodes=re.findall('strencode\("(.*?)","(.*?)"',content)[0]
    video=ctx.call('strencode',encodes[0],encodes[1])
    return video


def timenow():
    return datetime.datetime.now().strftime('%Y%m%d %H:%M:%S')


def randip():
    return str(random.randint(0, 255)) + "."\
            + str(random.randint(0, 255)) + "."\
            + str(random.randint(0, 255)) + "."\
            + str(random.randint(0, 255))

def randchar(): return ''.join(random.sample(chars, 5))

def exists(id):
    if not os.path.exists('history.txt'):
        return False
    with open('history.txt','r') as f:
        history=[i.strip() for i in f.readlines()]
    if id in history:
        return True
    else:
        return False

def get_list(url):
    print('start parse ' + url)
    videos=[]
    try:
        headers['X-Forwarded-For'] = randip()
        resp = requests.get(url, headers=headers)
        resp.encoding='utf-8'
        cont = resp.text
        urls = info_reg.findall(cont)
        print(url+ ' get {} videos'.format(len(urls)))
        for ul in urls:
            url, picture, title = ul
            url = url.replace('_hd', '')
            id = re.findall('viewkey=(.*?)&', url)[0]
            downpath=os.path.join(video_path,u'{}.mp4'.format(re.sub('[\\/:\*\?"><\|]','',title)))
            if not exists(id):
                videos.append({'id':id, 'url':url, 'picture':picture, 'downpath':downpath,'title':title})
                print(id + ' do not exists!')
        return videos
    except Exception as e:
        print(e)
        return False


def download_video(**kwargs):
    ds=[]
    url=kwargs['url']
    print('geting video from url {}'.format(url))
    try:
        headers['X-Forwarded-For'] = randip()
        resp = requests.get(url, headers=headers)
        resp.encoding='utf-8'
        cont = resp.text
        decrypt_cont=Decrypt(cont)
        print(decrypt_cont)
        video = mp4_reg.findall(decrypt_cont)[0]
        d=downloader(url=video,path=kwargs['downpath'],picture=kwargs['picture'],title=kwargs['title'],id=kwargs['id'])
        return d
    except Exception as e:
        print(e)
        return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', default='new')
    parser.add_argument('-a1', default=1, type=int)
    parser.add_argument('-a2', default=1, type=int)
    args = parser.parse_args()
    urls = {porn91_url: [args.a1, args.a2]}

    pagelists=[]
    for url in urls.keys():
        posts_url = url + '/video.php?viewtype=basic&category=hd&page=%d'
        for i in range(urls[url][0], urls[url][1] + 1):
            page_url = posts_url % i
            pagelists.append(page_url)

    #一页一页下载
    for page in pagelists:
        videopages=get_list(page)
        if videopages!=False:
            tasks=[]
            for video in videopages:
                d=download_video(**video)
                d.run()
        else:
            print('get list fail!')


if __name__=='__main__':
    main()

