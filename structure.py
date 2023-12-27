#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
import os
import asyncio

def parseArgs():
   parser = argparse.ArgumentParser()
   parser.add_argument('-d','--depth',type=int,default=5,help="递归深度")
   parser.add_argument('-p','--path',type=str,default=os.getcwd(),help="路径")
   parser.add_argument('-o','--output',type=str,default='./output.txt',help="输出文件")
   parser.add_argument('-s','--skip',type=bool,default=True)
   args = parser.parse_args()
   return args.depth, args.path, args.output, args.skip

async def draw(f:str, current:int, depth:int, path:str,prefix:str ,skipDotfiles:bool=True):
   entries = os.listdir(path)
   if len(entries) == 0:
        f.write('{}└──  <Empty>\n'.format(prefix))
   elif current == depth:
        f.write('{}└── ...\n'.format(prefix))
        return
   index = 0
   for entry in entries:
       full_path = os.path.join(path, entry)
       if os.path.isfile(full_path):
           index += 1
           if index == len(entries):
               f.write("{}└── {}\n".format(prefix,entry))
           else:
               f.write("{}├── {}\n".format(prefix,entry))
   for entry in entries:
       full_path = os.path.join(path, entry)
       if os.path.isdir(full_path):
           index += 1
           if index == len(entries):
              f.write("{}└── {}/\n".format(prefix,entry))
           else:
              f.write("{}├── {}/\n".format(prefix,entry))
           if not (entry.startswith(".")):
               if index == len(entries):
                   await draw(f,current+1,depth,full_path,prefix+"    ",skipDotfiles)
               else:
                   await draw(f,current+1,depth,full_path,prefix+"|   ",skipDotfiles)
async def main():
   depth, path, output, skip = parseArgs()
   f = open(output, 'w+', encoding='utf-8')
   f.write("{}/\n".format(os.path.basename(path)))
   await draw(f,0,depth,path," ",skip)
   print("任务完成")
   

if __name__ == '__main__':
   asyncio.run(main())
