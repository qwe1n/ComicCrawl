from urllib.parse import urljoin
from crawl.seleniumAdapter import Adapter
from selenium.webdriver.common.by import By

"""
这个比较慢。
"""

class Baozi(Adapter):
	def __init__(self):
		super().__init__("包子漫画", "https://baozimh.org")

	def search(self, keyword:str=""):
		self.get(f'/s/{keyword}/')
		comic_list = []
		while True:
			next_page = self.browser.find_elements(By.CSS_SELECTOR, "body > main > div > div.flex.justify-between.items-center.md\:gap-4.mx-2.md\:mx-0.mt-5.mb-10 > a:nth-child(3) > button")
			comic_list += self.browser.find_elements(By.CSS_SELECTOR, ".pb-2")
			if len(next_page) > 0:
				next_page[0].click()
			else:
				break
		if (len(comic_list) == 0):
			return []
		return [{"title": x.find_elements(By.CSS_SELECTOR, ".cardtitle")[0].text,"url":x.find_elements(By.CSS_SELECTOR, "div > a")[0].get_attribute("href")} for x in comic_list]
	
	def crawl_chapters(self, comic_url):
		self.get(comic_url)
		see_all = self.browser.find_elements(By.CSS_SELECTOR,".my-unit-sm > a")
		if len(see_all) > 0:
			see_all[0].click()
		chapter_list_container = self.browser.find_elements(By.CSS_SELECTOR, ".chapteritem")
		chapter_list = [{"title": x.find_elements(By.CSS_SELECTOR, ".chaptertitle")[0].text.strip(), "href": x.find_elements(By.CSS_SELECTOR, "div > a")[0].get_attribute("href")} for x in chapter_list_container]
		return chapter_list

	def crawl_images(self,comic_url,chapter_href):
		self.get(urljoin(comic_url,chapter_href))
		images = []
		images_container = self.browser.find_elements(By.CSS_SELECTOR, ".lazypreload")
		for image in images_container:
			if 'http' in image.get_attribute("data-src"):
				images.append(image.get_attribute("data-src"))
			else:
				images.append(urljoin(self.domain,image.get_attribute("data-src")))
		return images