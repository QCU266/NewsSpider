#!/usr/bin/env python
# coding=utf-8

import urllib2
from threading import Thread, Lock
from Queue import Queue
import time
import copy
import random

class Fetcher:

    def __init__(self, threads):
        #self.header = self.newHeader()
        # self.opener = urllib2.build_opener(urllib2.HTTPHandler)
        self.opener = urllib2.build_opener()
        self.lock = Lock()  # 线程锁
        self.q_req = Queue()  # 任务队列
        self.q_ans = Queue()  # 完成队列
        self.threads = threads
        for i in range(threads):
            t = Thread(target=self.threadget)  # 括号中的是每次线程要执行的任务
            t.setDaemon(True)  # 设置子线程是否随主线程一起结束，必须在start()
            # 之前调用。默认为False
            t.start()  # 启动线程
        self.running = 0  # 设置运行中的线程个数
        self.newHeader()

    def newHeader(self):
        headers = [
            {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},
            {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
            {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
            {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},
            {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0'},
            {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'}
        ]
        # 用于爬取网页前，随机获取一个header
        self.header = lambda : headers[random.randint(0, len(headers)-1)]
        self.opener.addheaders = [('User-Agent', (self.header())['User-Agent'])]


    def __del__(self):  # 解构时需等待两个队列完成
        time.sleep(0.5)
        self.q_req.join()  # Queue等待队列为空后再执行其他操作
        self.q_ans.join()

    # 返回还在运行线程的个数，为0时表示全部运行完毕
    def taskleft(self):
        return self.q_req.qsize() + self.q_ans.qsize() + self.running

    def push(self, req):
        self.q_req.put(req)

    def pop(self):
        return self.q_ans.get()

        # 线程执行的任务，根据req来区分
    def threadget(self):
        while True:
            req = self.q_req.get()

            # Lock.lock()操作，使用with可以不用显示调用acquire和release，
            # 这里锁住线程，使得self.running加1表示运行中的线程加1，
            # 如此做防止其他线程修改该值，造成混乱。
            # with下的语句结束后自动解锁。

            with self.lock:
                self.running += 1
            try:
                #request = urllib2.Request(req)
                #request.add_header(self.header)
                #ans = urllib2.urlopen(request).read()
                self.opener.addheaders
                ans = self.opener.open(req).read()
            except Exception, what:
                ans = ''
                print what
            self.q_ans.put((req, ans))  # 将完成的任务压入完成队列，在主程序中返回
            with self.lock:
                self.running -= 1
            self.q_req.task_done()  # 在完成一项工作之后，Queue.task_done()
            # 函数向任务已经完成的队列发送一个信号
            time.sleep(0.1)  # don't spam

class downloader:
    def download(self, urls, threads):
        contents = []
        dic = dict()
        f = Fetcher(threads)
        print f.header()
        for url in urls:
            f.push(url)

        count = 0
        while f.taskleft():
            #contents[i] = dict()
            if count == 20:
                f.newHeader()
                count = 0
            count +=1
            dic['url'], dic['content'] = f.pop()
            tmp = copy.deepcopy(dic)  # 深拷贝
            contents.append(tmp)
            #print dic['url']
            #print len(contents)
            #print contents[len(contents)-1]['url']
            print 'Get  ', dic['url'], '   ', len(dic['content']), 'B!'
        #for content in contents:
        #    print content['url']
        return contents

if __name__ == "__main__":
    links = ['http://news.163.com/photoview/3R710001/2187934.html','http://news.163.com/photoview/6QQD0001/2187173.html']
    #links = [u'http://news.163.com/photoview/3R710001/2187934.html',u'http://news.163.com/photoview/3R710001/2187799.html',u'http://news.163.com/photoview/3R710001/2187495.html',u'http://news.163.com/photoview/6QQD0001/2187173.html',u'http://news.163.com/16/0617/17/BPPFMOQ0000159VM.html',u'http://news.163.com/photoview/6QQD0001/119958.html',u'http://news.163.com/16/0701/16/BQTDJE8100014PRF.html',u'http://news.163.com/16/0701/21/BQTURR9000014PRF.html',u'http://news.163.com/16/0630/07/BQPSU59G00014PRF.html',u'http://news.163.com/16/0701/07/BQSFT44100014PRF.html',u'http://news.163.com/photoview/00AP0001/2188140.html',u'http://news.163.com/photoview/00AO0001/2188125.html',u'http://news.163.com/photoview/00AO0001/2188125.html',u'http://news.163.com/photoview/00AN0001/2188102.html',u'http://news.163.com/photoview/00AN0001/2188102.html',u'http://news.163.com/photoview/00AP0001/2188139.html',u'http://news.163.com/photoview/00AP0001/2188139.html']
    netease = downloader()
    text = netease.download(links, 1)
    print text[0]
    print text[1]['url']
