#!/usr/bin/env python
# coding=utf-8


from bs4 import BeautifulSoup
import re
import requests
import jieba.analyse

class HtmlAnalyze:
    '网页分析'

    def getUrl(self, html_doc, href_patt):
        '获取网页中符合正则表达式 href_patt 的所有链接'
        soup = BeautifulSoup(html_doc, 'lxml')
        new_urls = list()
        for a in soup.find_all("a", href=href_patt):
            new_urls.append(unicode(a['href']))

        return new_urls

    def neteaseContent(self, html_doc):
        '网易新闻网页的新闻内容提取'
        try:
            soup = BeautifulSoup(html_doc, "lxml")
            [s.extract() for s in soup.find_all('script')]  # 去除<script>标签
            post_news = soup.find("div", class_="post_content post_area clearfix")
            news = dict()

            news['catgories'] = []
            for tag in post_news.find("div", "post_crumb").find_all("a"):
                news['catgories'].append(tag.string)
            news['catgories'] = ">".join(news['catgories'])

            main_content = soup.find("div", id="epContentLeft")
            news['title'] = main_content.find("h1").string

            time_patt = '(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})'
            news['post_time'] = re.search(time_patt, main_content.find(
               "div", "post_time_source").contents[0]).group()

            news['origin'] = dict()
            news['origin']['url'] = re.search(
                'href="(.*?)"', unicode(main_content.find("a", id="ne_article_source"))).group(1)
            news['origin']['name'] = main_content.find(
                "a", id="ne_article_source").string
            news['origin'] = unicode(news['origin'])

            news['content'] = list(main_content.find(
                "div", id="endText").find_all("p"))
            for i in range(len(news['content'])):
                news['content'][i] = unicode(news['content'][i])
            news['content'] = ''.join(news['content'])

            keywords = jieba.analyse.extract_tags(news['content'])
            news['keywords'] = '|'.join(keywords)

            news['source'] = u"网易新闻"

            return news
        except:
            return {}

if __name__ == "__main__": # 模块测试代码
    ana = HtmlAnalyze()
    html = requests.get('http://news.163.com/16/0703/02/BR10VU4H00014AED.html')
    html_doc = html.content
    news = ana.neteaseContent(html_doc)
    print news
