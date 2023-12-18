from crawl import Crawl
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin

class Qimanwu(Crawl):
	def __init__(self, begin:int=0, end:int=-1):
		super().__init__("奇漫屋","https://www.eafomfg.cn",begin,end)

	def search(self,keyword:str=""):
		if keyword == "":
			keyword = input("请输入搜索关键词:\n")
		html = self.get('search?key='+keyword).text
		soup = BeautifulSoup(html,'html.parser')
		comic_list = soup.select(".mh-item")
		if (len(comic_list) == 0):
			print("未找到相关漫画")
			return 
		print("搜索结果如下：")
		i = 0
		for comic in comic_list:
			print(str(i) + "\t:\t" + comic.select("div > div > h2 > a")[0]['title'])
			i += 1
		print("请输入序号选择漫画：")
		choice = input()
		self.comic['title'] = comic_list[int(choice)].select("div > div > h2 > a")[0]['title'].strip()
		self.comic['url'] = comic_list[int(choice)].select("div > a")[0]['href']
		if not os.path.exists(os.path.join(self.config['download_path'],self.comic['title'].strip())):
			os.mkdir(os.path.join(self.config['download_path'],self.comic['title'].strip()))
	
	def crawl_chapters(self):
		html = self.get(self.comic['url']).text
		soup = BeautifulSoup(html,'html.parser')
		chapter_soup_list = soup.select("#chapterlistload .detail-list-form-item")
		self.comic['chapter_list'] = []
		for chapter_soup in chapter_soup_list:
			if chapter_soup.text in self.comic['status']['chapter_loaded']:
				continue
			self.comic['chapter_list'].append({
				'href'	: chapter_soup['href'],
				'title'	: chapter_soup.text.strip(),
				'images'	: []
			})
			self.comic['status']['chapter_loaded'].append(chapter_soup.text)
		self.comic['status']['chapter_loaded_finished'] = True

	def crawl_images(self, chapter_href):
		html = self.get(chapter_href).text
		soup = BeautifulSoup(html,'html.parser')
		images = []
		image_soup_list = soup.select(".main-item > img")
		for image_soup in image_soup_list:
			if 'http' in image_soup['src']:
				images.append(image_soup['src'])
			else:
				images.append(urljoin(self.domain,image_soup['src']))
		return images