#!/usr/bin/env python
# coding=utf-8


from url_manager import UrlManager
from htmlAnalyze import HtmlAnalyze
import multiThreadDownloader
import re
import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf8')



class neteaseNewsCrawler:

    def __init__(self):
        self.seed = 'http://news.163.com/'  # 网易新闻首页
        self.downloader = multiThreadDownloader.downloader()
        self.analyze = HtmlAnalyze()
        self.craw_url_man = UrlManager()
        self.page_url_man = UrlManager()
        self.conn = MySQLdb.connect(
            host='localhost', user='root', passwd='toor',
            db='newsGather', charset='utf8')
        self.conn.set_character_set('utf8')
        self.cur = self.conn.cursor()
        self.cur.execute('SET NAMES utf8;')
        self.cur.execute('SET CHARACTER SET utf8;')
        self.cur.execute('SET character_set_connection=utf8;')
        self.cur.execute('SET character_set_database=utf8;')

    def craw(self):  # 新闻抓取
        
        self.craw_url_man.add_new_url(self.seed)
        count = 0
        i = 1
        while self.craw_url_man.has_new_url:
            new_urls = self.craw_url_man.get_new_urls(len(self.craw_url_man.new_urls))
            pages = self.downloader.download(new_urls, 6)
            print "第%d次扩展" % i
            for page in pages:
                craw_new_urls = self.analyze.getUrl(page['content'], re.compile("http://news\.163\.com/.*?"))
                self.craw_url_man.add_new_urls(craw_new_urls)
                page_new_urls = self.analyze.getUrl(page['content'], re.compile(
                    "(http://news\.163\.com)/1[456]/(\d{4})/\d+/(\w+)\.html$"))
                #count = count + len(page_new_urls)
                self.page_url_man.add_new_urls(page_new_urls)
                count = len(self.page_url_man.new_urls)
                if count > 100:
                    break
            else:
                i = i + 1
                continue

            break

        new_urls = self.page_url_man.get_new_urls(len(self.page_url_man.new_urls))
        pages = self.downloader.download(new_urls, 6)

        news = list()
        dic = dict()
        for page in pages:
            dic = self.analyze.neteaseContent(page['content'])
            dic['url'] = page['url']

            patt = re.compile('/([a-zA-Z0-9]+.html)$')
            try:
                filename = './html/' + re.search(patt, dic['url']).group(1)
                f = open(filename, 'w')
                f.write(dic['content'])
                f.close()
            except:
                print "无法写出文件！"


            #dic['content'] = filename
            print dic['url']
            try:
                sql_raw = "INSERT IGNORE INTO news_info (url, post_time, title, origin, keywords, source) VALUES ('%s', '%s', '%s',  \"%s\", '%s', '%s')" % (dic['url'], dic['post_time'], dic['title'], dic['origin'], dic['keywords'], dic['source'])
                spider.cur.execute(sql_raw)
                spider.conn.commit()

                news.append(dic)
            except:
                print "crawl error!"
    #           spider.conn.rollback()
        return news


if __name__ == "__main__":
    spider = neteaseNewsCrawler()
    news = spider.craw()
    spider.conn.close()
