from urllib.parse import urljoin
from crawl.seleniumAdapter import Adapter
from selenium.webdriver.common.by import By

class Godness(Adapter):
	def __init__(self):
		super().__init__("女神漫画","https://www.yfxxeeh.cn/")

	def search(self, keyword:str=""):
		self.get('index.php/search?key='+keyword)
		comic_list = self.browser.find_elements(By.CSS_SELECTOR, ".common-comic-item")
		if (len(comic_list) == 0):
			return []
		return [{"title": x.find_elements(By.CSS_SELECTOR, ".comic__title > a")[0].text.strip(),"url":x.find_elements(By.CSS_SELECTOR, "div > a")[0].get_attribute("href")} for x in comic_list]
	

	def crawl_chapters(self,comic_url):
		self.get(comic_url)
		chapter_list = self.browser.find_elements(By.CSS_SELECTOR, ".j-chapter-link")
		return [{"title": x.text.strip(), "href": x.get_attribute("href")} for x in chapter_list]


	def crawl_images(self,comic_url, chapter_href):
		self.get(chapter_href)
		images = []
		images_container = self.browser.find_elements(By.CSS_SELECTOR, ".read-container > .rd-article-wr > .rd-article__pic > img")
		for image in images_container:
			if 'http' in image.get_attribute("data-original"):
				images.append(image.get_attribute("data-original"))
			else:
				images.append(urljoin(self.domain,image.get_attribute("data-original")))
		return images