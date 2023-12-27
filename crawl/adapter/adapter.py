from requests import get
from urllib.parse import urljoin
import chardet

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

	def search(self,keyword:str=""):
		comic = {
			'title': "",
			'url'  : ""
		}
		return comic
		
	def crawl_chapters(self, comic_url):
		chapter_soup_list = [None] # <a href='{url}'>{title}</a>
		return chapter_soup_list

	def crawl_images(self,comic_url,chapter_href):
		images = [] # list of images' url
		return images
	
	def get(self, target:str):
		if "http" not in target:
			target = urljoin(self.domain,target)
		response = get(target,headers=self.config['headers'])
		encoding = chardet.detect(response.content)['encoding']
		response.encoding = encoding
		return response