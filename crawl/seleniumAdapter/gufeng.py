from urllib.parse import urljoin
from crawl.seleniumAdapter import Adapter
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoAlertPresentException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

"""
这个挺慢的
"""

class Gufeng(Adapter):
	def __init__(self):
		super().__init__("古风漫画", "https://www.gufengmh9.com")

	def search(self, keyword:str=""):
		self.get(f'search/?keywords={keyword}')
		comic_list = self.browser.find_elements(By.CSS_SELECTOR, ".item-lg > a")
		if (len(comic_list) == 0):
			return []
		return [{"title": x.get_attribute("title"),"url":x.get_attribute("href")} for x in comic_list]
	
	def crawl_chapters(self, comic_url):
		self.get(comic_url)
		chapter_list = self.browser.find_elements(By.CSS_SELECTOR, "#chapter-list-1 a")
		return [{"title": x.find_elements(By.CSS_SELECTOR,"span")[0].text.strip(), "href": x.get_attribute("href")} for x in chapter_list]

	def crawl_images(self,comic_url,chapter_href):
		self.get(urljoin(comic_url,chapter_href))
		images = []
		while True:
			images_container = self.browser.find_elements(By.CSS_SELECTOR, "#images > img")[0]
			images.append(images_container.get_attribute("src"))
			next_button = self.browser.find_elements(By.CSS_SELECTOR, "body > div.chapter-view > div:nth-child(4) > div > a:nth-child(5)")[0]
			next_button.click()
			try:
				alert = WebDriverWait(self.browser, 1).until(EC.alert_is_present())
				alert.dismiss()
				break
			except (NoAlertPresentException, TimeoutException):
				continue
		return images