from requests import get
from urllib.parse import urljoin
import chardet

class Adapter():
	def __init__(self, name:str, domain:str):
		self.name = name
		self.domain = domain
		self.config = {
			"headers"	:{
				"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
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
		chapter_soup_list = None
		return chapter_soup_list

	def crawl_images(self,comic_url,chapter_href):
		images = []
		return images
	
	def get(self, target:str):
		if "http" not in target:
			target = urljoin(self.domain,target)
		response = get(target,headers=self.config['headers'])
		encoding = chardet.detect(response.content)['encoding']
		response.encoding = encoding
		return response