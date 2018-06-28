#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author    : 奶权
# Action    : 微博监控
# Desc      : 微博监控启动模块

import time,hashlib,requests
import smtplib
import base64
from email.mime.text import MIMEText
from email.utils import formataddr
from email.header import Header

import requests,json,sys
from lxml import etree


DEBUG=0
class Weibo:
    def __init__(self):
        self.session = requests.session()
        self.LOGIN = False
        self.reqHeaders = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://passport.weibo.cn/signin/login',
            'Connection': 'close',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'
        }
        
    def login(self, userName, passWord):
        loginApi = 'https://passport.weibo.cn/sso/login'
        loginPostData = {
            'username':userName,
            'password':passWord,
            'savestate':1,
            'r':'',
            'ec':'0',
            'pagerefer':'',
            'entry':'mweibo',
            'wentry':'',
            'loginfrom':'',
            'client_id':'',
            'code':'',
            'qq':'',
            'mainpageflag':1,
            'hff':'',
            'hfp':''
        }
        #get user session
        try:
            r = self.session.post(loginApi,data=loginPostData,headers=self.reqHeaders)
            if DEBUG:
                pass
            js = r.json()
            if r.status_code == 200 and js['retcode'] == 20000000:
                self.echoMsg('Info','Login successful! UserId:'+json.loads(r.text)['data']['uid'])
                self.LOGIN = True
      
            else:
                self.echoMsg('Error','Logon failure!')
                print(js)
        
                sys.exit()
        except Exception as e:
            self.echoMsg('Error',e)
            sys.exit()

    """
        @   Class self  :
        @   String wbUserId  : The user you want to monitored
    """
    def get_cookies(self):
        if not self.LOGIN:return 
        r = ""
        for k,v in self.session.cookies.items():
            s = k+"="+v+ " "
            r += s
        return r.strip()
    
    
    def getWBQueue(self, wbUserId, cookies_str):
        #get user weibo containerid
        userInfo = 'https://m.weibo.cn/api/container/getIndex?uid=%s&type=uid&value=%s'%(wbUserId,wbUserId)
        cookie = dict()
        print(cookies_str)
        for item in cookies_str.split(" "):
            print(item)
            print(item.split("="))
            k,v = item.split("=")
            cookie.update({k:v})

        try:
            r = self.session.get(userInfo,headers=self.reqHeaders, cookies = requests.utils.cookiejar_from_dict(cookie, cookiejar=None, overwrite=True))
            if DEBUG:
                print(dir(r))
                         
                         
            js = r.json()["data"]
            for tab in js['tabsInfo']['tabs']:
                if tab['tab_type'] == 'weibo':
                    conId = tab['containerid']
        except Exception as e:
            self.echoMsg('Error',e)
            sys.exit()
        #get user weibo index
        self.weiboInfo = 'https://m.weibo.cn/api/container/getIndex?uid=%s&type=uid&value=%s&containerid=%s'%(wbUserId,wbUserId,conId)

    def startMonitor(self, ):
        try:
            r = self.session.get(self.weiboInfo,headers=self.reqHeaders)
            js = r.json()["data"]
            
            for card in js['cards']:
                if card["card_type"] == 9:
                    mblog = card["mblog"]
                    print(mblog['created_at'])
                    if mblog['created_at'] == "1分钟前":
                        return True
                        
            
        except Exception as e:
            self.echoMsg('Error',e)
            sys.exit()

    """
        @   String level   : Info/Error
        @   String msg     : The message you want to show
    """
    def echoMsg(self, level, msg):
        if level == 'Info':
            print ('[Info] %s'%msg)
        elif level == 'Error':
            print ('[Error] %s'%msg)


def sendMail(title = "千里发微博啦", _to = "614436985@qq.com"):
    flag = True
    text = "<html><body><h1>有新的消息请注意查收</h1></body></html>"
    _sender = "flykai769@sohu.com"
    _password = "2g5paeW92593GfD"
    _sender = "flybird36985@gmail.com"
    _password = input("请输入邮箱密码:")
    
    _recipient = _to #收件人
    
    msg = MIMEText(text, 'html', 'utf-8')
    msg['From'] = formataddr(["微博管家", _sender])
    msg['To'] = formataddr(["用户", _recipient])
    msg['Subject'] = Header(title,'utf-8').encode()
    print(msg.as_string())
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com',465)
        #server = smtplib.SMTP('smtp.sohu.com',25)
        server.login(_sender,_password)
        server.sendmail(_sender, _recipient, msg.as_string())
        server.quit()
    except Exception as e:
        print( e)
        flag = False
    return flag

def main(cookies, wbUserId):
    w = Weibo()
    w.getWBQueue(wbUserId, cookies)
    while 1:
        newWB = w.startMonitor()
        if newWB is not None:
            print("send mail")
            sendMail()
        time.sleep(36)

if __name__ == '__main__':
    sendMail()
    cookies = input("请输入cookies :\n")
    wbUserId = "1102309111"
    main(cookies,wbUserId)

