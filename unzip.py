# Author: SuperJason
# Date: 2020.12.14
# usage: change srcpath、passwd in __main__
#        srcpath：zipfiles father folder
#        passwd：decompression passwd 
# description: 批量解压带密码的压缩包，并将文件名改为md5值

import zipfile
import os,re
import hashlib
import datetime

# srcpath是大量zip文件所在的文件夹，dstpath是解压的目的文件夹
def unzip(srcpath:str,dstpath:str,passwd:str):
    # zip文件全路径list
    print("解压压缩文件到文件夹"+dstpath)
    print("开始解压缩\t"+str(datetime.datetime.now()))
    zipfilelist=[]
    for root,dirs,files in os.walk(srcpath):
        for f in files:
            filepath=os.path.join(root,f)
            if zipfile.is_zipfile(filepath):
                zipfilelist.append(filepath)
    for i in zipfilelist:
        fz=zipfile.ZipFile(i,'r')
        print(fz.namelist())
        for f in fz.namelist():            
            fz.extract(f,path=dstpath,pwd=bytes(passwd,encoding="utf-8"))
    print("解压缩结束\t"+str(datetime.datetime.now()))

# 将解压好的文件名转为md5，dstpath待改名文件所在的文件夹，并且去重
def filename_to_md5(dstpath:str):
    print("开始重命名MD5\t"+str(datetime.datetime.now()))
    for root,dirs,files in os.walk(dstpath):
        for f in files:
            filepath=os.path.join(dstpath,f)
            hash_md5=hashlib.md5()
            with open(filepath,"rb") as fb:
                data=fb.read()
                hash_md5.update(data)
                md5=hash_md5.hexdigest()
            if not os.path.exists(os.path.join(dstpath,md5)):
                os.rename(filepath,os.path.join(dstpath,md5))
            else:
                os.remove(filepath)
    print("重命名MD5结束\t"+str(datetime.datetime.now()))


if __name__ == "__main__":
    starttime=datetime.datetime.now()
    srcpath="E:/Evasion Sample"
    dstpath=os.path.join(srcpath,"md5_Sample")  
    passwd="infected"
    # 解压缩密码为infected的压缩文件
    unzip(srcpath,dstpath,passwd)
    # 将指定文件夹文件改名为md5
    filename_to_md5(dstpath)
    endtime=datetime.datetime.now()
    print("times:\t"+str(endtime-starttime))
