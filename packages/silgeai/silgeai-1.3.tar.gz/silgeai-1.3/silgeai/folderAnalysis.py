# -*- coding:utf-8 -*-
"""
@Author: 风吹落叶
@Contact: waitKey1@outlook.com
@Version: 1.0
@Date: 2024/5/15 14:25
@Describe: 
"""
import json
import os
from .dictPrint import print_dict_as_treeV2

def GetDirSize(dirpath):
    dirJson={}
    dirJson['DirName'] = os.path.basename(dirpath)
    dirJson['TotalSize'] = 0
    dirJson['Dirs'] = []
    dirJson['Files']=[]

    SumSize=0
    filenum=0
    if os.path.isdir(dirpath):
        fileNames=os.listdir(dirpath)
        for fileName in fileNames:
            path=os.path.join(dirpath,fileName)
            if os.path.isdir(path):
                size,dirChildJson=GetDirSize(path)
                dirJson['Dirs'].append(dirChildJson)
                SumSize+=size
                filenum+=dirChildJson['FileNum']
            else:
                dirJson['Files'].append({'FileName':fileName,'FileSize':int(os.stat(path).st_size/1024)})
                SumSize+= int(os.stat(path).st_size/1024)
    else:
        return 0
    dirJson['TotalSize'] = SumSize
    dirJson['Dirs']=sorted(dirJson['Dirs'],key=lambda x:x['TotalSize'],reverse=True)

    dirJson['Files'] = sorted(dirJson['Files'], key=lambda x: x['FileSize'],reverse=True)
    dirJson['FileNum'] = len(dirJson['Files'])+filenum
    return SumSize,dirJson

def GetFileSize(filePath):
    return os.stat(filePath).st_size/1024

def DirAnalysis(dirpath,outpath='analysis.json'):
    print('解析文件夹：{} 结构如下 单位： kb'.format(dirpath))
    SumSize, dirJson = GetDirSize(dirpath)
    try:
        if outpath=='analysis.json':
            outpath=os.path.basename(dirpath)+'.json'
        if not outpath.endswith('json'):
            with open(outpath,'w',encoding='utf-8')as w:
                w.write(str(dirJson))
            print('output请用Json格式')
        else:
            json.dump(dirJson, open(outpath, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
            print_dict_as_treeV2(dirJson)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    dirpath = r'I:\Downloads\MuseTalk3\MuseTalk1\assets'
    SumSize,dirJson=GetDirSize(dirpath)
    json.dump(dirJson,open('test.json','w',encoding='utf-8'),ensure_ascii=False,indent=2)

