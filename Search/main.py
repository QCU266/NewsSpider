#!/usr/bin/env 
# coding: utf-8

import web
import MySQLdb
from bs4 import BeautifulSoup
import jieba
import re

punct = set(u'''/+%#:!),.:;?]}¢'"、。〉》」』】〕〗〞︰︱︳﹐､﹒
﹔﹕﹖﹗﹚﹜﹞！），．：；？｜｝︴︶︸︺︼︾﹀﹂﹄﹏､～￠
々‖•·ˇˉ―--′’”([{£¥'"‵〈《「『【〔〖（［｛￡￥〝︵︷︹︻
︽︿﹁﹃﹙﹛﹝（｛“‘-—_…''')
Letters_and_numbers = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
render = web.template.render('templates/')
urls=(
    "/", "index",
    "/news", "news"
)

class db:
    def __init__(self):
        self.connect = MySQLdb.connect(
            host='localhost', user='root', passwd='toor',
            db='newsGather', charset='utf8')
        self.cursor = self.connect.cursor()


class index:
    def __init__(self):
        pass

    def GET(self):
        data = web.input()
        if data:
            searchword = data.searchword
        else:
            searchword = ''
        news_list = list()
        #topic = list()
        if searchword:
            cut = jieba.cut_for_search(searchword)
            word_list = []
            for word in cut:
                if word not in punct and word not in Letters_and_numbers:
                    word_list.append(word.encode("utf8"))

            for word in word_list:
                #data = dict()
                dbsearch = db()
                raw_sql = """SELECT * FROM news_info WHERE keywords REGEXP '%s' OR title REGEXP '%s' ORDER BY post_time DESC;""" % (word, word)

                dbsearch.cursor.execute(raw_sql)
                results = dbsearch.cursor.fetchall()
                #bsearch.cursor.close()

                if results != ():
                    for result in results:
                        data = dict()
                        data['url'] = result[0]
                        data['time'] = unicode(result[1])
                        data['title'] = result[2]
                        data['keywords'] = result[3]
                        data['content'] = result[4]
                        data['source'] = result[5]
                        data['origin'] = dict()
                        data['origin'] = eval(result[6])

                        patt = re.compile('/([a-zA-Z0-9]+).html$')
                        data['id'] = re.search(patt, data['url']).group(1)

                        digest = ''
                        soup = BeautifulSoup(data['content'], "lxml")
                        soup = soup.find_all('p')
                        i = 0
                        if soup:
                            for p in soup:
                                if p.string:
                                    digest += unicode(p.string)
                                if i > 2:
                                    break
                                i = i + 1
                        data['digest'] = digest

                        news_list.append(data)

            dbsearch.connect.close()
        return render.index(searchword, news_list)

        
class news:
    def __init__(self):
        pass

    def GET(self):
        data=web.input()
        if data:
            ID=data.id
            news = dict()
            
            dbsearch = db()

            raw_sql = """SELECT * FROM news_info WHERE url REGEXP '%s';""" % ID
            dbsearch.cursor.execute(raw_sql)
            result = dbsearch.cursor.fetchall()

            if result != ():
                data = dict()
                data['url'] = result[0][0]
                data['time'] = unicode(result[0][1])
                data['title'] = result[0][2]
                #data['keywords'] = result[3]
                data['content'] = result[0][4]
                data['source'] = result[0][5]
                data['origin'] = dict()
                data['origin'] = eval(result[0][6])

            news = data
            
        dbsearch.connect.close()
        return render.news(news)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
