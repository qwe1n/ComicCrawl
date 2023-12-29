from bs4 import BeautifulSoup
from urllib.parse import urljoin
from crawl.adapter import Adapter

class Fengche(Adapter):
	def __init__(self):
		super().__init__("风车漫画", "https://www.qyy158.com")

	def search(self, keyword:str=""):
		html = self.get(f'/search/{keyword}/').text
		soup = BeautifulSoup(html,'html.parser')
		comic_list = soup.select(".cart-item")
		if (len(comic_list) == 0):
			return []
		return [{"title": x.select(".hover-a")[0].text,"url":x.select("div > a")[0]['href']} for x in comic_list]
	
	def crawl_chapters(self, comic_url):
		html = self.get(comic_url).text
		soup = BeautifulSoup(html,'html.parser')
		chapter_soup_list = soup.select(".chapter-list > li > a")
		return chapter_soup_list

	def crawl_images(self,comic_url,chapter_href):
		html = self.get(urljoin(comic_url,chapter_href)).text
		soup = BeautifulSoup(html,'html.parser')
		images = []
		image_soup_list = soup.select(".chapter-content > img")
		for image_soup in image_soup_list:
			if 'http' in image_soup['data-original']:
				images.append(image_soup['data-original'])
			else:
				images.append(urljoin(self.domain,image_soup['data-original']))
		return images