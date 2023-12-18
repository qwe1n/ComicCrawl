from welcome import welcomeFun
from qimanwu import Qimanwu
from fengche import Fengche
from crawl import Crawl
import argparse

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a','--adapter',type=str,default="fengche",help="适配器")
    parser.add_argument('-c','--comic',type=str,default='',help="漫画名称")
    args = parser.parse_args()
    return args

if __name__ == '__main__':
      welcomeFun()
      adapter = {
           'fengche': Fengche,
           'qimanwu': Qimanwu
	  }
      args = parseArgs()
      crawl = Crawl(adapter[args.adapter]())
      crawl.run(args.comic)
    
