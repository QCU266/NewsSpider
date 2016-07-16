#!/usr/bin/env python
# coding=utf-8


class UrlManager(object):
    def __init__(self):
        self.new_urls = set()
        self.old_urls = set()

    def add_new_url(self, url):
        if url is None:
            return
        if url not in self.old_urls:
            self.new_urls.add(url)

    def add_new_urls(self, urls):
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_new_url(url)

    def has_new_url(self):
        return len(self.new_urls) != 0

    def get_new_url(self):
        new_url = self.new_urls.pop()
        self.old_urls.add(new_url)
        return new_url

    def get_new_urls(self, num):
        new_urls = list()
        if num > len(self.new_urls):
            num = len(self.new_urls)
        for i in range(num):
            new_urls.append(self.get_new_url())
        return new_urls

if __name__ == "__main__":
    mana = UrlManager()
    mana.add_new_urls(["http://news.163.com/photoview/3R710001/2187934.html"])
    urls = mana.get_new_url()
    print mana.new_urls, mana.old_urls, urls