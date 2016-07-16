# 新闻主题爬虫

目前只有网易新闻的爬取规则

## 使用方法

### 环境配置
* Python 2.7.x
* MySQL
* 第三方 Python 库
    * [jieba 中文分词](https://github.com/fxsjy/jieba)
    * BeautifulSoup 
    * requests
    * web.py

### 初始化数据库
* MySQL 数据库建一个表(见`initMySQL.sql`)文件(连接数据库相关配置，直接在`crawler.py`和`Search\main.py` 更改相关代码)

### 运行爬虫
* 直接运行`crawler.py`, 按提示输入此次要爬取的新闻条数

### 用户搜索
* 运行`Search\main.py`, 在浏览器输入`http://localhost:8080`即可使用

### 示例网站

[http://www.silird.xyz:8080](http://www.silird.xyz:8080)

