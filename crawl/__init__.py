__version__ = "1.0"

import os
import asyncio
import aiohttp
import aiofiles
from tqdm import tqdm
import yaml
from base64 import b64decode

___all__ = ['Crawl','__version__']

class Crawl():
	def __init__(self, adapter, path:str=os.path.join(os.getcwd(), 'resources')):
		self.adapter = adapter
		self.comic = {
			'adapter': adapter.name,
			'domain': self.adapter.domain,
			'title'	: "",
			'url'	: "",
			'chapter_list': [],
			'stage' : 0
		}
		self.config = {
			'max_threads': 10,
			"download_path": path #漫画保存路径
		}
		if not os.path.exists(path):
			os.mkdir(path)
		"""
		comic :
			domain	: 网站域名
			title	: 漫画名称
			url		: 漫画主页链接
			chapter_list	: 漫画各章节信息
				- href	: 章节链接
				- title	: 章节标题
				- images: 漫画图片链接
					- []
		"""
	
	def parseYaml(self):
		if not os.path.exists(os.path.join(self.config['download_path'],self.comic['title'], 'comic.yaml')):
			return
		with open(os.path.join(self.config['download_path'],self.comic['title'], 'comic.yaml'), 'r') as f:
			self.comic = yaml.safe_load(f)
	
	def dumpYaml(self):
		with open(os.path.join(self.config['download_path'],self.comic['title'], 'comic.yaml'), 'w') as f:
			yaml.dump(self.comic, f)
	
	def search(self,keyword:str=""):
		if keyword == "":
			keyword = input("请输入搜索关键词：")
		comic_list = self.adapter.search(keyword)
		index = 1
		for comic in comic_list:
			print(f"{index}.{comic['title']}")
			index += 1
		choice = input("请输入要选择的序号：")
		if choice.isdigit():
			choice = int(choice)
			if choice <= len(comic_list) and choice >= 1:
				self.comic['title'] = comic_list[choice-1]['title']
				self.comic['url'] = comic_list[choice-1]['url']
				if not os.path.exists(os.path.join(self.config['download_path'],self.comic['title'].strip())):
					os.mkdir(os.path.join(self.config['download_path'],self.comic['title'].strip()))
				self.comic['stage'] = 1
				return
			else:
				print("输入有误，请重新输入！")
				return
		else:
			print("输入有误，请重新输入！")
			return

	def crawl_chapters(self):
		if self.comic['stage'] < 1:
			print("请先确定漫画!")
			return
		chapter_list = self.adapter.crawl_chapters(self.comic['url'])
		self.comic['chapter_list'] = []
		for chapter in chapter_list:
			self.comic['chapter_list'].append({
				'href'	: chapter['href'],
				'title'	: chapter['title'],
				'images'	: [],
				'downloaded'	: False,
			})
		self.comic['stage'] = 2

	async def download(self,url:str,chapter_title:str, filename:str):
		filename = os.path.join(os.getcwd(), 'resources', self.comic['title'].strip(), chapter_title.strip(), filename)
		async with asyncio.Semaphore(self.config['max_threads']):
			if url.startswith('data:image'):
				base64_data = url.split(',')[1]
				image_data = b64decode(base64_data)
				async with aiofiles.open(filename, mode='wb+') as f:
					await f.write(image_data)
					await f.close()
			else:
				for i in range(3):
					try:
						async with aiohttp.ClientSession() as session:
							async with session.get(url, headers=self.adapter.config['headers']) as resp:
								if resp.status == 200:
									async with aiofiles.open(filename,mode='wb+') as f:
										await f.write(await resp.content.read())
										await f.close()
									break
								else:
									print(f"\nError downloading {url}. Retrying...")
					except Exception as e:
						print(f"\nFailed to download {url} after 3 attempts")
						await asyncio.sleep(1)
	
	async def save_images(self):
		for chapter in self.comic['chapter_list']:
			if not os.path.exists(os.path.join(self.config['download_path'], self.comic['title'].strip(), chapter['title'].strip())):
				os.mkdir(os.path.join(self.config['download_path'], self.comic['title'].strip(), chapter['title'].strip()))
			if chapter['downloaded'] == True:
				print(f"\n{chapter['title']} already downloaded")
				continue
			tasks = []
			if len(chapter['images']) == 0:
				chapter['images'] = self.adapter.crawl_images(self.comic['url'],chapter['href'])
			images = chapter['images']
			index = 1
			pbar = tqdm(total=len(images), desc=chapter['title'], unit='item')
			for image in images:
				task = asyncio.create_task(self.download(image,chapter['title'] , str(index).rjust(2,'0')+'.jpg'))
				def callback():
					pbar.update(1)
				task.add_done_callback(lambda t: callback())
				tasks.append(task)
				index += 1
			await asyncio.wait(tasks)
			pbar.close()
			chapter['downloaded'] = True

	def run(self, title:str=""):
		if self.comic['stage'] == 0:
			self.search(title)
		self.parseYaml()
		if self.comic['adapter'] != self.adapter.name:
			print("配置文件与适配器不兼容")
			print(f"请更换适配器为{self.comic['adapter']} 或者删除配置文件comic.yaml")
			return
		try:
			if self.comic['stage'] < 2:
				self.crawl_chapters()
			print(f"将要爬取的章数为:\t"+str(len(self.comic['chapter_list'])))
			asyncio.get_event_loop().run_until_complete(self.save_images())
		except Exception as e:
			raise e
		finally:
			self.dumpYaml()
			print("配置文件已保存")
		print("爬取完成")