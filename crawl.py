from requests import get
from urllib.parse import urljoin
import os
import asyncio
import aiohttp
import aiofiles
from tqdm import tqdm
import yaml
import chardet
import base64
from io import BytesIO

class Crawl():
	def __init__(self, name ,domain, begin:int=0, end:int=-1):
		self.name = name
		self.domain = domain
		self.begin = begin
		self.end = end
		self.comic = {
			'domain': self.domain,
			'title'	: "",
			'url'	: "",
			'chapter_list': [],
			'status': {
				'chapter_downloaded': [],
				'chapter_loaded': [],
				'chapter_loaded_finished': False,
			}
		}
		self.config = {
			"semaphore" :asyncio.Semaphore(10),
			"headers"	:{
				"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
				"Referer"	: self.domain
			},
			"download_path": os.path.join(os.getcwd(), 'resources')
		}
		if not os.path.exists(os.path.join(os.getcwd(), 'resources')):
			os.mkdir(os.path.join(os.getcwd(), 'resources'))
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

	def get(self, target:str):
		if "http" not in target:
			target = urljoin(self.domain,target)
		response = get(target,headers=self.config['headers'])
		encoding = chardet.detect(response.content)['encoding']
		response.encoding = encoding
		return response
	
	def search(self):
		pass

	def crawl_images(self):
		pass 

	def crawl_chapters(self):
		pass

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
					async with session.get(url, headers=self.config['headers']) as resp:
						if resp.status == 200:
							async with aiofiles.open(filename,mode='wb+') as f:
								await f.write(await resp.content.read())
								await f.close()
						else:
							print("Error downloading " + url)
	
	async def save_chapter_images(self):
		for chapter in self.comic['chapter_list'][self.begin:self.end]:
			if not os.path.exists(os.path.join(self.config['download_path'], self.comic['title'].strip(), chapter['title'].strip())):
				os.mkdir(os.path.join(self.config['download_path'], self.comic['title'].strip(), chapter['title'].strip()))
			if chapter['title'] in self.comic['status']['chapter_downloaded']:
				print(f"{chapter['title']} already downloaded")
				continue
			tasks = []
			if len(chapter['images']) == 0:
				chapter['images'] = self.crawl_images(chapter['href'])
			images = chapter['images']
			index = 1
			pbar = tqdm(total=len(images), desc=chapter['title'], unit='item')
			for image in images:
				task = asyncio.create_task(self.download(image,self.comic['title'], chapter['title'] , str(index).rjust(2,'0')+'.jpg'))
				task.add_done_callback(lambda t: pbar.update(1))
				tasks.append(task)
				index += 1
			await asyncio.wait(tasks)
			pbar.close()
			self.comic['status']['chapter_downloaded'].append(chapter['title'])

	def run(self, title:str=""):
		self.search(title)
		self.parseYaml()
		try:
			if not self.comic['status']['chapter_loaded_finished'] == True:
				self.crawl_chapters()
			if self.end == -1:
				self.end = len(self.comic['chapter_list'])
			print(f"需要爬取的章数为:\t"+str(self.end - self.begin))
			asyncio.get_event_loop().run_until_complete(self.save_chapter_images())
		except Exception as e:
			raise e
		finally:
			self.dumpYaml()
		print("爬取完成")