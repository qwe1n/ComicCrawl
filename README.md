# 一个支持爬取多个页面、易拓展的漫画爬虫

  

## 快速开始

```

python -m pip install -r requirements.txt

  

python main.py

```

## 参数
```
-a/--adapter: 适配器 # crawl/adapter目录和crawl/seleniumAdapter目录下放着各适配器

-c/--comic : 漫画名称

-p/--path : 漫画下载路径 默认当前目录的resource目录下
```
  

## 特点

- 支持爬取多个网站
- 易于拓展，将爬虫分为两部分：下载器和适配器，如果需要爬新的网站，只需仿造其他适配器，很容易就能再写一个新的适配器
	- crawl/adapter 目录下的适配器是基于beautifulsoup和requests爬取的
	- crawl/seleniumAdapter目录下的适配器是基于selenium爬取的

## 拓展说明
在适配器目录下新建py文件编写，按照下述格式
```
class NewAdapter(Adapter):

    def __init__(self):

        super().__init__("${网站名称}", "${网站网址}")

  

    def search(self, keyword:str=""):

        # 爬取搜索结果页面,返回格式如下
        return[
	        {
		        'title': '',
		        'url' : ''
	        }
        ]

    def crawl_chapters(self, comic_url):

        # 爬取章节，返回格式如下
        return[
	        {
		        'title': '',
		        'href' : ''
	        }
        ]

  

    def crawl_images(self,comic_url,chapter_href):

        # 爬取图片链接，返回链接字符串组成的列表

        return []
```
再在对应目录下__init__.py，把刚写好的适配器引入就ok了，要使用新适配器的话别忘在main.py里导入并添加进adapterDist里
