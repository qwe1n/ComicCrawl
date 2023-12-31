from bs4 import BeautifulSoup
from urllib.parse import urljoin
from crawl.adapter import Adapter

class Biqu(Adapter):
	def __init__(self):
		super().__init__("笔趣漫画","https://www.biqumh.com/")

	def search(self, keyword:str=""):
		html = self.get('index.php/search?key='+keyword).text
		soup = BeautifulSoup(html,'html.parser')
		comic_list = soup.select(".common-comic-item")
		if (len(comic_list) == 0):
			return []
		return [{"title": x.select(".comic__title > a")[0].text,"url":x.select("div > a")[0]['href']} for x in comic_list]

	def crawl_chapters(self,comic_url):
		html = self.get(comic_url).text
		soup = BeautifulSoup(html,'html.parser')
		chapter_soup_list = soup.select(".j-chapter-link")
		return [{"title": x.text.strip(), "href": x['href']} for x in chapter_soup_list]

	def crawl_images(self,comic_url, chapter_href):
		html = self.get(chapter_href).text
		soup = BeautifulSoup(html,'html.parser')
		images = []
		image_soup_list = soup.select(".read-container > .rd-article-wr > .rd-article__pic > img")
		for image_soup in image_soup_list:
			if 'http' in image_soup['data-original']:
				images.append(image_soup['data-original'])
			else:
				images.append(urljoin(self.domain,image_soup['data-original']))
		return images