from bs4 import BeautifulSoup
from urllib.parse import urljoin
from crawl.adapter import Adapter

class Yinghua(Adapter):
	def __init__(self):
		super().__init__("樱花漫画","https://www.shuanglilock.com.cn/")

	def search(self, keyword:str=""):
		html = self.get('/search?searchkey='+keyword).text
		soup = BeautifulSoup(html,'html.parser')
		search_msg = soup.select(".search-msg")[0].text
		if "结果为空" in search_msg:
			return []
		comic_list = soup.select(".comics-card")
		if (len(comic_list) == 0):
			return []
		return [{"title": x.select("div > a")[0]['title'].strip(),"url":x.select("div > a")[0]['href']} for x in comic_list]

	
	def crawl_chapters(self,comic_url):
		html = self.get(comic_url).text
		soup = BeautifulSoup(html,'html.parser')
		chapter_soup_list = soup.select("#layout > div > div:nth-child(2) > div > div:nth-child(7) > div > a")
		return [{"title": x.select("span")[0].text.strip(), "href": x['href']} for x in chapter_soup_list]
		

	def crawl_images(self,comic_url, chapter_href):
		html = self.get(chapter_href).text
		soup = BeautifulSoup(html,'html.parser')
		images = []
		image_soup_list = soup.select(".lazy-img")
		for image_soup in image_soup_list:
			if 'http' in image_soup['data-original']:
				images.append(image_soup['data-original'])
			else:
				images.append(urljoin(self.domain,image_soup['data-original']))
		return images