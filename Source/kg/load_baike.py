import csv
import numpy as np
import re
import os

def find_files( workPath ):
    if len(workPath)==0:
        return []
        
    fileList = []
    dirs = os.listdir( workPath ) 
    for f in dirs:
        fPath = workPath + '/' + f
        if not os.path.isdir( fPath ):
            fileList.append(fPath)
    return fileList

#读取一个百科文本文件
def parse_baike( txtlines ):
    ret = {'实体':'', '简介':''}
    for l in txtlines:
        l = l.strip()
    return

csvlines = list()
txtFiles = find_files( './select' )
for fname in txtFiles:
    filepath = fname.split('/')
    with open(fname, 'r', encoding='utf-8') as f:
        txtlines = f.readlines()
        parse_baike( txtlines )
        
