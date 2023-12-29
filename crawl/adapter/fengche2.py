from urllib.parse import urljoin
from crawl.adapter import Adapter
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options


class Fengche(Adapter):
	def __init__(self):
		super().__init__("风车漫画", "https://www.qyy158.com")
		options = Options()
		options.add_argument('--headless') 
		self.browser = webdriver.Firefox(options=options)


	def search(self, keyword:str=""):
		self.get(f'/search/{keyword}/')
		comic_list = self.browser.find_elements(By.CSS_SELECTOR, ".cart-item")
		if (len(comic_list) == 0):
			return []
		return [{"title": x.find_elements(By.CSS_SELECTOR, ".hover-a")[0].text,"url":x.find_elements(By.CSS_SELECTOR, "div > a")[0].get_attribute("href")} for x in comic_list]
	
	def crawl_chapters(self, comic_url):
		self.get(comic_url)
		chapter_list = self.browser.find_elements(By.CSS_SELECTOR, ".chapter-list > li > a")
		return [{"title": x.text.strip(), "href": x.get_attribute("href")} for x in chapter_list]

	def crawl_images(self,comic_url,chapter_href):
		self.get(urljoin(comic_url,chapter_href))
		images = []
		images_container = self.browser.find_elements(By.CSS_SELECTOR, ".chapter-content > img")
		for image in images_container:
			if 'http' in image.get_attribute("data-original"):
				images.append(image.get_attribute("data-original"))
			else:
				images.append(urljoin(self.domain,image.get_attribute("data-original")))
		return images
	
	def get(self, target:str):
		if "http" not in target:
			target = urljoin(self.domain,target)
		self.browser.get(target)

	def __del__(self):
		self.browser.quit()