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

    def netease(self, html_doc):
        '网易新闻网页的新闻内容提取'
        try:
            soup = BeautifulSoup(html_doc, "lxml")
            [s.extract() for s in soup.find_all('script')]  # 去除<script>标签
            post_new = soup.find("div", class_="post_content post_area clearfix")
            news = dict()

            # 归档
            news['catgories'] = []
            for tag in post_new.find("div", "post_crumb").find_all("a"):
                news['catgories'].append(tag.string)
            news['catgories'] = ">".join(news['catgories'])

            # 标题
            post_content = soup.find("div", id="epContentLeft")
            news['title'] = post_content.find("h1").string

            # 发布时间
            time_patt = '(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})'
            news['post_time'] = re.search(time_patt, post_content.find(
               "div", "post_time_source").contents[0]).group()

            # 原始来源
            news['origin'] = dict()
            news['origin']['url'] = re.search(
                'href="(.*?)"', unicode(post_content.find("a", id="ne_article_source"))).group(1)
            news['origin']['name'] = post_content.find(
                "a", id="ne_article_source").string
            news['origin'] = unicode(news['origin'])

            # 正文提取
            #news['content'] = list(post_content.find(
            #    "div", id="endText").find_all("p"))
            main_content = post_content.find('div', 'post_body')

            tag = main_content.find('style')
            if tag:
                tag.extract()

            tag = main_content.find('div', 'nph_photo')
            if tag:
                tag.extract()

            tag = main_content.find('div', 'nph_photo_layout')
            if tag:
                tag.extract()

            tag = main_content.find('div', 'post_topshare_wrap')
            if tag:
                tag.extract()

            tag = main_content.find('div', 'post_btmshare')
            if tag:
                tag.extract()

            tag = main_content.find('div', 'post_end_ad')
            if tag:
                tag.extract()

            tag = main_content.find('div', 'gg200x300')
            if tag:
                tag.extract()
            
            news['content'] = unicode(main_content)


            # 关键字提取
            keywords = jieba.analyse.extract_tags(main_content.get_text())
            news['keywords'] = '|'.join(keywords)

            # 出处
            news['source'] = u"网易新闻"

            return news
        except:
            return None 

    def Content(self, website, html_doc):
        news = dict()
        if website == 1:
            news = self.netease(html_doc)

        elif website == 2:
            news = None
            pass

        else:
            print "站点分析规则不存在!"
            news = None
        
        return news

if __name__ == "__main__":
    ana = HtmlAnalyze()
    html = requests.get('http://news.163.com/16/0703/02/BR10VU4H00014AED.html')
    html_doc = html.content
    news = ana.neteaseContent(html_doc)
    print news
