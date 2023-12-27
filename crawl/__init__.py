__version__ = "1.0"

import os
import asyncio
import aiohttp
import aiofiles
from tqdm import tqdm
import yaml
import base64

___all__ = ['Crawl']

class Crawl():
	def __init__(self, adapter, path):
		self.adapter = adapter
		self.comic = {
			'adapter': adapter.name,
			'domain': self.adapter.domain,
			'title'	: "",
			'url'	: "",
			'chapter_list': [],
			'status': {
				'chapter_downloaded': [],
				'chapter_loaded': [],
				'chapter_loaded_finished': False,
				'current_num_of_images': 0,
				'current_chapter': ''
			}
		}
		self.config = {
			"semaphore" :asyncio.Semaphore(10),
			"download_path": path #漫画保存路径
		}
		if not os.path.exists(path):
			os.mkdir(path)
		"""
		comic {
			domain	: 网站域名
			title	: 漫画名称
			url		: 漫画主页链接
			chapter_list	: 漫画各章节信息
				- href	: 章节链接
				- title	: 章节标题
				- images: 漫画图片链接
					- []
			status	: 爬取状态
				- downloaded	: 爬取完的章节
				- chapter_list_loaded	: 章节列表是否爬取
				- current_num_of_images : 目前在爬的章节的已爬图片数量
				- current_chapter : 目前在爬的章节
		}
		"""
	
	def parseYaml(self):
		if not os.path.exists(os.path.join(self.config['download_path'],self.comic['title'], 'config.yaml')):
			return
		with open(os.path.join(self.config['download_path'],self.comic['title'], 'config.yaml'), 'r') as f:
			self.comic = yaml.safe_load(f)
	
	def dumpYaml(self):
		with open(os.path.join(self.config['download_path'],self.comic['title'], 'config.yaml'), 'w') as f:
			yaml.dump(self.comic, f)
	
	def search(self,keyword:str=""):
		if keyword == "":
			keyword = input("请输入搜索关键词:\n")
		comic = self.adapter.search(keyword)
		if comic == {}:
			return
		self.comic['title'] = comic['title']
		self.comic['url'] = comic['url']
		if not os.path.exists(os.path.join(self.config['download_path'],self.comic['title'].strip())):
			os.mkdir(os.path.join(self.config['download_path'],self.comic['title'].strip()))

	def crawl_chapters(self):
		chapter_soup_list = self.adapter.crawl_chapters(self.comic['url'])
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

	async def download(self,url:str,comic_name:str, chapter_title:str, filename:str):
		filename = os.path.join(os.getcwd(), 'resources', self.comic['title'].strip(), chapter_title.strip(), filename)
		async with self.config['semaphore']:
			if url.startswith('data:image'):
				base64_data = url.split(',')[1]
				image_data = base64.b64decode(base64_data)
				async with aiofiles.open(filename, mode='wb+') as f:
					await f.write(image_data)
					await f.close()
			else:
				async with aiohttp.ClientSession() as session:
					async with session.get(url, headers=self.adapter.config['headers']) as resp:
						if resp.status == 200:
							async with aiofiles.open(filename,mode='wb+') as f:
								await f.write(await resp.content.read())
								await f.close()
						else:
							print("Error downloading " + url)
	
	async def save_chapter_images(self):
		for chapter in self.comic['chapter_list']:
			if not os.path.exists(os.path.join(self.config['download_path'], self.comic['title'].strip(), chapter['title'].strip())):
				os.mkdir(os.path.join(self.config['download_path'], self.comic['title'].strip(), chapter['title'].strip()))
			if chapter['title'] in self.comic['status']['chapter_downloaded']:
				print(f"{chapter['title']} already downloaded")
				continue
			if chapter['title'] != self.comic['status']['current_chapter']:
				self.comic['status']['current_chapter'] = chapter['title']
				self.comic['status']['current_num_of_images'] = 0
			tasks = []
			if len(chapter['images']) == 0:
				chapter['images'] = self.adapter.crawl_images(self.comic['url'],chapter['href'])
			images = chapter['images']
			index = self.comic['status']['current_num_of_images'] + 1
			pbar = tqdm(total=len(images), desc=chapter['title'], unit='item')
			pbar.update(self.comic['status']['current_num_of_images'])
			for image in images[self.comic['status']['current_num_of_images']:]:
				task = asyncio.create_task(self.download(image,self.comic['title'], chapter['title'] , str(index).rjust(2,'0')+'.jpg'))
				def callback():
					pbar.update(1)
					self.comic['status']['current_num_of_images'] += 1
				task.add_done_callback(lambda t: callback())
				tasks.append(task)
				index += 1
			await asyncio.wait(tasks)
			pbar.close()
			self.comic['status']['chapter_downloaded'].append(chapter['title'])

	def run(self, title:str=""):
		self.search(title)
		self.parseYaml()
		if self.comic['adapter'] != self.adapter.name:
			print("配置文件与适配器不兼容")
			print(f"请更换适配器为{self.comic['adapter']} 或者删除配置文件config.yaml")
			return
		try:
			if not self.comic['status']['chapter_loaded_finished'] == True:
				self.crawl_chapters()
			print(f"将要爬取的章数为:\t"+str(len(self.comic['chapter_list'])))
			asyncio.get_event_loop().run_until_complete(self.save_chapter_images())
		except Exception as e:
			raise e
		finally:
			self.dumpYaml()
			print("配置文件已保存")
		print("爬取完成")