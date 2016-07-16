#!/usr/bin/env python
# coding=utf-8


from url_manager import UrlManager
from htmlAnalyze import HtmlAnalyze
import multiThreadDownloader
import re
import MySQLdb


escape_dict={'\a':r'\a',
             '\b':r'\b',
           '\c':r'\c',
           '\f':r'\f',
           '\n':r'\n',
           '\r':r'\r',
           '\t':r'\t',
           '\v':r'\v',
           '\'':r'\'',
           '\"':r'\"',
           '\0':r'\0',
           '\1':r'\1',
           '\2':r'\2',
           '\3':r'\3',
           '\4':r'\4',
           '\5':r'\5',
           '\6':r'\6',
           '\7':r'\7',
           '\8':r'\8',
           '\9':r'\9'}

def raw(text):  # 将每个可能的转义字符都进行了替换
    """Returns a raw string representation of text"""
    new_string=''
    for char in text:
        try: new_string+=escape_dict[char]
        except KeyError: new_string+=char
    return new_string


class NewsCrawler:

    def __init__(self):
        self.seed = ['', 'http://news.163.com/' ] # 网易新闻首页
        self.downloader = multiThreadDownloader.downloader()
        self.analyze = HtmlAnalyze()
        self.craw_url_man = UrlManager()
        self.page_url_man = UrlManager()
        self.conn = MySQLdb.connect(
            host='localhost', user='root', passwd='toor',
            db='newsGather', charset='utf8')
        self.cur = self.conn.cursor()

        # 将数据库中已下载的url加入url管理器的old_urls中
        self.cur.execute("select url from news_info;")
        results = self.cur.fetchall()
        exist_urls = list()
        if results == ():
            pass
        else:
            for i in results:
                exist_urls.append(i[0])
            self.page_url_man.add_old_urls(exist_urls)

    def get_news(self, website):  # 处理url管理器中的新的新闻url
        news = list()
        dic = dict()
        count = 0
        new_urls = self.page_url_man.get_new_urls(len(self.page_url_man.new_urls))
        print "获取新闻网页："
        pages = self.downloader.download(new_urls, 6)
        print "分析新闻网页并存储新闻...."
        for page in pages:
            dic = self.analyze.Content(website, page['content'])
            if dic:
                dic['url'] = page['url']
                news.append(dic)
                try:
                    print 'save ',dic['url']
                    sql_raw = "INSERT IGNORE INTO news_info (url, post_time, title,  keywords, content, source, origin) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', \"%s\")" % (dic['url'], dic['post_time'], dic['title'], dic['keywords'], raw(dic['content']), dic['source'], dic['origin'])
                    spider.cur.execute(sql_raw)
                    spider.conn.commit()
                    count += 1
                except:
                    print "save error!"
        print '抓取新闻数：%d' % count
        return news

    def craw(self, news_num, website, expand_patt, news_patt):  # 新闻抓取
        # print "hello"
        self.craw_url_man.add_new_url(self.seed[website])
        news = list()
        dic = dict()
        count = 0
        i = 0
        while self.craw_url_man.has_new_url:
            print "第%d次扩展：" % i
            #print "获取待扩展页面："
            craw_num = len(self.craw_url_man.new_urls)
            if craw_num < 60:
                new_urls = self.craw_url_man.get_new_urls(craw_num)
            else:
                new_urls = self.craw_url_man.get_new_urls(60)
            
            pages = self.downloader.download(new_urls, 6)
            print "分析待扩展页面....."
            for page in pages:
                craw_new_urls = self.analyze.getUrl(page['content'], expand_patt)
                self.craw_url_man.add_new_urls(craw_new_urls)
                page_new_urls = self.analyze.getUrl(page['content'], news_patt)
                #count = count + len(page_new_urls)
                self.page_url_man.add_new_urls(page_new_urls)
                count = len(self.page_url_man.new_urls)
                if count > news_num:
                    news += self.get_news(website)
                    break
            else:
                i = i + 1
                news += self.get_news(website)
                continue

            break
        return news


if __name__ == "__main__":
    netease_expand_patt = re.compile("http://news\.163\.com/.*?")
    netease_news_patt = re.compile("(http://news\.163\.com)/1[456]/(\d{4})/\d+/(\w+)\.html$")
    spider = NewsCrawler()
    while 1:
        try:
            num = int(raw_input("请输入要抓取的新闻数："))
        except:
            print "输入有误，请重新输入！"
            continue
        break
    spider.craw(num, 1, netease_expand_patt, netease_news_patt)
    spider.conn.close()
