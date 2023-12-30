from urllib.parse import urljoin
from crawl.seleniumAdapter import Adapter
from selenium.webdriver.common.by import By


class Yinghua(Adapter):
	def __init__(self):
		super().__init__("樱花漫画", "https://www.shuanglilock.com.cn")

	def search(self, keyword:str=""):
		self.get(f'/search?searchkey={keyword}')
		comic_list = self.browser.find_elements(By.CSS_SELECTOR, ".comics-card")
		if (len(comic_list) == 0):
			return []
		return [{"title": x.find_elements(By.CSS_SELECTOR, "div > a")[0].get_attribute("title"),"url":x.find_elements(By.CSS_SELECTOR, "div > a")[0].get_attribute("href")} for x in comic_list]
	
	def crawl_chapters(self, comic_url):
		self.get(comic_url)
		chapter_list = self.browser.find_elements(By.CSS_SELECTOR, "#layout > div > div:nth-child(2) > div > div:nth-child(7) > div > a")
		return [{"title": x.find_elements(By.CSS_SELECTOR, "span")[0].text.strip(), "href": x.get_attribute("href")} for x in chapter_list]

	def crawl_images(self,comic_url,chapter_href):
		self.get(urljoin(comic_url,chapter_href))
		images = []
		images_container = self.browser.find_elements(By.CSS_SELECTOR, ".lazy-img")
		for image in images_container:
			if 'http' in image.get_attribute("data-original"):
				images.append(image.get_attribute("data-original"))
			else:
				images.append(urljoin(self.domain,image.get_attribute("data-original")))
		return images