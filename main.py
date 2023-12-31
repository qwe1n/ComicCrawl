from welcome import welcomeFun
from crawl import Crawl, adapter, seleniumAdapter

import argparse
import os

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a','--adapter',type=str,default="fengche",help="适配器")
    parser.add_argument('-c','--comic',type=str,default='',help="漫画名称")
    parser.add_argument('-p','--path',type=str,default=os.path.join(os.getcwd(), 'resources'),help="漫画保存路径")
    args = parser.parse_args()
    return args

if __name__ == '__main__':
      welcomeFun()
      adapterDist = {
           'fengche': adapter.Fengche,
           'qimanwu': seleniumAdapter.Qimanwu,
           'godness': seleniumAdapter.Godness,
           'baozi'  : seleniumAdapter.Baozi,
           'gufeng' : seleniumAdapter.Gufeng,
           'yinghua': seleniumAdapter.Yinghua,
           'biqu'   : adapter.Biqu,
           'biqu2'  : seleniumAdapter.Biqu
	  }
      args = parseArgs()
      crawler = Crawl(adapterDist[args.adapter](),path=args.path)
      crawler.run(args.comic)