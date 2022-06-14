# -*- coding: utf-8 -*-
"""
2022-03-20
@author: yan


起因: 就是改變資料集時，針對對於非使用現有資料集(如coco or obj365)的標註改變，參考我exp60跟exp61
因為延長線在舊的labelID是15(第16類)但是新ID的是12，要全部轉換。


images影像資料可以不管
準備:
/labels_old
classes_old.txt

使用轉換目標的參考:
classes_new.txt

輸出:
/labels_new 內的txt資料ID要改變，但是BB box不能改變

outline:
input:
classe


"""



#%% setting the path of works
from pathlib import Path
import numpy as np
import os 

os.chdir(os.path.dirname(__file__))
filterpath=Path(os.path.dirname(__file__))

#%% setting the i/o states

old_class='classes_old.txt'
new_class='classes_new.txt'

labels_old='labels_old'
labels_new='labels_new/'

#%% read class
old,new=np.array([]),np.array([])
with open(old_class, "r") as f:
    old=np.append(old,f.read().split('\n'))

with open(new_class, "r") as f:
    new=np.append(new,f.read().split('\n'))  
# %% 先建立舊資料清單
oldFileList=[]

for i in Path(labels_old).iterdir():
    oldFileList.append(i)

# %% 先使用讀取舊資料清單

## first file

""" test1
先開啟old-label資料夾內的資料逐一比對現資料
    開啟後將內容複寫至new-label資料夾
"""
#%% 初步完成完全複製檔案至另一邊
for annofile in oldFileList:
    with open(annofile,"r") as f :
        old_data = f.read().split('\n') 
        #開啟新檔案
        with open(labels_new+annofile.name,"w") as w :
                #多少行貼多少次
            for i in old_data[:-1]:
                    w.write(i)
                    w.write('\n')
    

# %%寫兌換label Id的
""" test2
先用一個檔案測試
好了後包成function給上面
"""
annofile = oldFileList[0] #先一個個檔案測試
with open(annofile,"r") as f :
    oldData = f.read().split('\n') 
    #開啟新檔案
    with open(labels_new+annofile.name,"w") as w :
            #多少行貼多少次
        for i in oldData[:-1]:
            #每行第一個側標籤tag print(i.split(' ')[0])
            tag = int(i.split(' ')[0])
            if old[tag] == new[tag]: #label name的ID 是否相同? >>相同就直接複製貼上
                print(i.split(' ')[0])
                w.write(i)
                w.write('\n')
            else:
                """
                #舊的標籤在新標籤哪裡?
                如果有在 >>直接輸出new的位置 更改ID
                沒有     >>[] PASS
                """
                index = np.where(new==old[tag]) #舊的標籤在新標籤哪裡?
                if index != []:
                    print("where label?")
                    bbox=i.split(' ')
                    w.write(f"{index[0][0]} {bbox[1]} {bbox[2]} {bbox[3]} {bbox[4]}\n")
                    

#%%
""" test1+test2
整合全部

"""
for annofile in oldFileList:
    annofile = oldFileList[0] #先一個個檔案測試
    with open(annofile,"r") as f :
        oldData = f.read().split('\n') 
        #開啟新檔案
        with open(labels_new+annofile.name,"w") as w :
                #多少行貼多少次
            for i in oldData[:-1]:
                #每行第一個側標籤tag print(i.split(' ')[0])
                tag = int(i.split(' ')[0])
                if old[tag] == new[tag]: #label name的ID 是否相同? >>相同就直接複製貼上
                    print(i.split(' ')[0])
                    w.write(i)
                    w.write('\n')
                else:
                    """
                    #舊的標籤在新標籤哪裡?
                    如果有在 >>直接輸出new的位置 更改ID
                    沒有     >>[] PASS
                    """
                    index = np.where(new==old[tag]) #舊的標籤在新標籤哪裡?
                    if index != []:
                        print("where label?")
                        bbox=i.split(' ')
                        w.write(f"{index[0][0]} {bbox[1]} {bbox[2]} {bbox[3]} {bbox[4]}\n")
                





# %%

tag = 15
#判斷有無相等

old[tag] == new[tag]


# %%


