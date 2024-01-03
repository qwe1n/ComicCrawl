from urllib.parse import urljoin
from crawl.seleniumAdapter import Adapter
from selenium.webdriver.common.by import By

class Qimanwu(Adapter):
	def __init__(self):
		super().__init__("奇漫屋","https://www.eafomfg.cn")

	def search(self, keyword:str=""):
		self.get('search?key='+keyword)
		comic_list = self.browser.find_elements(By.CSS_SELECTOR, ".mh-item")
		if (len(comic_list) == 0):
			return []
		return [{"title": x.find_elements(By.CSS_SELECTOR, "div > div > h2 > a")[0].text.strip(),"url":x.find_elements(By.CSS_SELECTOR, "div > a")[0].get_attribute("href")} for x in comic_list]

	def crawl_chapters(self,comic_url):
		self.get(comic_url)
		chapter_list = self.browser.find_elements(By.CSS_SELECTOR, "#chapterlistload .detail-list-form-item")
		return [{"title": x.text.strip(), "href": x.get_attribute("href")} for x in chapter_list]

	def crawl_images(self,comic_url, chapter_href):
		self.get(chapter_href)
		images = []
		images_container = self.browser.find_elements(By.CSS_SELECTOR, ".main-item > img")
		for image in images_container:
			if 'http' in image.get_attribute("src"):
				images.append(image.get_attribute("src"))
			else:
				images.append(urljoin(self.domain,image.get_attribute("src")))
		return images