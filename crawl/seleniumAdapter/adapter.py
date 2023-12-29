from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

class Adapter():
	def __init__(self, name:str, domain:str):
		self.name = name
		self.domain = domain
		self.config = {
			"headers"	:{
				"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
				"Referer"	: self.domain
			},
		}
		options = Options()
		options.add_argument('--disable-infobars')
		options.add_argument('--blink-settings=imagesEnabled=false')
		options.add_argument('--disable-extensions')
		options.add_argument('--disable-gpu')
		options.add_argument('--disable-cache')
		options.add_argument('--disable-network-cache')
		options.add_argument('--headless') 
		self.browser = webdriver.Firefox(options=options)

	def search(self,keyword:str=""):
		comic = [{
			'title': "",
			'url'  : ""
		}]
		return comic
		
	def crawl_chapters(self, comic_url):
		chapter_list = [{
			'title': "",
			'href'  : ""
		}]
		return chapter_list

	def crawl_images(self,comic_url,chapter_href):
		images = [] # list of images' url
		return images
	
	def get(self, url:str):
		if "http" not in url:
			url = urljoin(self.domain, url)
		self.browser.get(url)

	def __del__(self):
		print("浏览器关闭中...")
		self.browser.quit()