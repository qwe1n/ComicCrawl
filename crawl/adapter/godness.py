from bs4 import BeautifulSoup
from urllib.parse import urljoin
from crawl.adapter import Adapter

class Godness(Adapter):
	def __init__(self):
		super().__init__("女神漫画","https://www.yfxxeeh.cn/")

	def search(self,keyword:str=""):
		html = self.get('index.php/search?key='+keyword).text
		soup = BeautifulSoup(html,'html.parser')
		comic_list = soup.select(".common-comic-item")
		if (len(comic_list) == 0):
			print("未找到相关漫画")
			return {}
		print("搜索结果如下：")
		i = 0
		for comic in comic_list:
			print(str(i) + "\t:\t" + comic.select(".comic__title > a")[0].text)
			i += 1
		print("请输入序号选择漫画：")
		choice = input()
		comic = {}
		comic['title'] = comic_list[int(choice)].select(".comic__title > a")[0].text.strip()
		comic['url'] = comic_list[int(choice)].select("div > a")[0]['href']
		return comic
	
	def crawl_chapters(self,comic_url):
		html = self.get(comic_url).text
		soup = BeautifulSoup(html,'html.parser')
		chapter_soup_list = soup.select(".j-chapter-link")
		return chapter_soup_list

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