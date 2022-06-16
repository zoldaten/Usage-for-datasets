# -*- coding: utf-8 -*-
"""
2022-03-29
@author: yan

2022-03-31 修改算影像張數 
改為:
FileName = eachClassSavePath+datasoure+"_"+classList[tag]+"_"+str(len(globals() ['classFile'+str(tag)]))+".txt"
原本:
FileName = eachClassSavePath+datasoure+"_"+classList[tag]+"_"+str(int(InstanceClass[tag]))+".txt"

下面三個要改
datasoure="/obj365"

eachClassSavePath = 'ClassSets/Main'

txtsavepath = 'ImageSets/Main'


##can comment 這裡可以直接省略

起因: 為了能夠讀取label檔案，然後公平的分train/val資料


images影像資料可以不管
準備:
/labels
classes.txt



輸出:
/EachClass
    此資料夾內有所有的各類別影像數量，並且將檔案名稱存起來，用以後面的split去公平分ImageSet

txtsavepath = 'ImageSets/Main'


##0616改
因為為了要系統性的家東西所以要歸類名稱
所有產生的東西盡量前面都有名稱如:o12v1_Main1
setName="o12v1_Main4"


//0616v2
要做一個可以在ClassSets內中知道空標註檔案在哪裡影像有多少個
影該也要在這裡當成訓練資料
我有模擬none01.txt、none02.txt
不然以前都沒有空標註當訓練資料有點可惜

在此是成功弄好了，但是想想覺得好像優勢不大所以還是止步於此

"""



#%% setting the path of works

from pathlib import Path
import random
import numpy as np
import os

os.chdir(os.path.dirname(__file__))
# os.chdir(os.path.dirname(__file__)) #window need comment this line
# os.chdir(os.path.dirname(__file__)) # linux need this line

filterpath=Path(os.path.dirname(__file__))

#%% setting the i/o states

classFile ='classes.txt'

datasoure="/obj365"

setName="o12v1_Main6"

eachClassSavePath = 'ClassSets/'+setName

txtsavepath = 'ImageSets/'+setName

classList=np.array([])
with open(classFile, "r") as f:
    classList=np.append(classList,f.read().split('\n'))


labelfilepath = Path('labels')

totalLabelFile = os.listdir(labelfilepath)
"""可以用下面代替
用os就是另外創立一個list去存但是我只是要開啟，而且Path這樣code比較clear
labelfilepath = Path('labels')

totalLabelFile = os.listdir(labelfilepath)
"""

if not os.path.exists(eachClassSavePath):
    os.makedirs(eachClassSavePath)

#%%create globals for calculatee instace
# for i in range(len(classList)-1):
#     globals() ['InstanceClass'+str(i)]=[]
InstanceClass=np.zeros(len(classList)-1)

#%%create globals for calculatee each file of label
"""
利用這裡儲存的list去創立最後的txtfile ，也可以利用這裡做train/val分割
"""

for i in range(len(classList)):
    globals() ['classFile'+str(i)]=[]
#%%Definde for calculate each label instance
def classCounter(classLen):
    for i in range(classLen-1):
        locals() ['class'+str(i)]=[]



#%%先用一個檔案測試
# annoFile = 'labels/'+totalLabelFile[0] #先一個個檔案測試
#這裡花最多時間
for annoFile in labelfilepath.iterdir():

    #open file to get annoData
    with open(annoFile,"r") as f:
        annoData = f.read().split('\n')[:-1] #不要最後的空行
        # print(annoData) #all anno saved as list

    # print(annoFile) #check where error
    #getting Label ID from each anno
    annoCounter=np.zeros(len(classList)-1)
    for data in annoData:
        # print(data.split(' ')[0]) #label id (0~N)
        annoCounter[int(data.split(' ')[0])] += 1

    #add instance 因為同維度阿
    InstanceClass += annoCounter
    #where counter > 0
    recodeFileIndex=np.where(annoCounter>0)
    

    for index in recodeFileIndex[0]:
        globals() ['classFile'+str(index)].append(annoFile.stem) #stem 是Path中把.txt弄掉 純名稱
    
    #record noneLabel
    if(np.sum(annoCounter)==0):
        globals() ['classFile'+str(len(classList)-1)].append(annoFile.stem) #stem 是Path中把.txt弄掉 純名稱



#%%Create file

with open(setName+"_InstanceClass.txt","w") as f:
    for i in range(len(InstanceClass)):
        f.write(str(int(InstanceClass[i])))
        f.write(' : ')
        f.write(classList[i])
        f.write('\n')

#%%create multiple file

"""
這裡是創建能夠各自類別產生檔案名到ClassSets但是!!!!
等到多資料源時其實沒有什麼意義了QQ
"""
##can comment
for tag in range(len(classList)):

    FileName = eachClassSavePath+datasoure+"_"+classList[tag]+"_"+str(len(globals() ['classFile'+str(tag)]))+".txt"

    fileData = open(FileName,'w')
    for i in globals() ['classFile'+str(tag)]:
        # print(i)
        fileData.write(str(i)+"\n")
        
    fileData.close()



# %% 
#少至多的順序
sortIndex = np.argsort(InstanceClass)
# np.flip(np.argsort(InstanceClass))#多至少的順序
file_train=[]
file_val=[]


train_percent = 0.9


# sortIndex=[7] #指定哪個檔案

count=0
for tag in sortIndex: #少至多的順序

    if InstanceClass[tag]>0: # instace>0 ?
        #split train /val 
        #trinIndex
        num = len(globals() ['classFile'+str(tag)]) 
        listIndex = range(num) #(0,n)
        trinNum = int(num * train_percent)
        trainIndex = random.sample(listIndex, trinNum)

        for i in listIndex:
            if i in  trainIndex:
                file_train.append(globals() ['classFile'+str(tag)][i])
            else:
                file_val.append(globals() ['classFile'+str(tag)][i])

        #將後續的sort檔案排除已經進入
        for delIndex in sortIndex[count+1:]: #本身因該不用了，因為已經看完了
            #判斷在此tag的檔案內是否有存在在後續的檔案內?
            for i in listIndex:
                #如果存在就刪除
                if globals() ['classFile'+str(tag)][i] in  globals() ['classFile'+str(delIndex)]:
                    globals() ['classFile'+str(delIndex)].remove(globals() ['classFile'+str(tag)][i])
                    
    count+=1


##noneLabelFile to train(only train)
num = len(globals() ['classFile'+str(len(classList)-1)]) 
listIndex = range(num) #(0,n)
# trinNum = int(num * train_percent)
# trainIndex = random.sample(listIndex, trinNum)

for i in listIndex:
    file_train.append(globals() ['classFile'+str(len(classList)-1)][i])



#%% save train/val in ImageSets/Main


"""
file_train=[]
file_val=[]
這裡面的資料
"""

if not os.path.exists(txtsavepath):
    os.makedirs(txtsavepath)

sets = ['train', 'val']
for tag in sets:
    FileName = txtsavepath+"/"+tag+".txt"

    fileData = open(FileName,'w')
    for data in globals() ['file_'+tag]:
    # print(i)
        fileData.write(data+"\n")
    fileData.close()


# %% 生成檔案路徑給model 訓練

sets = ['train', 'val']
FILE = Path(__file__).absolute()
abs_path=FILE.parents[0].as_posix()
for image_set in sets:
    if not os.path.exists('labels'):
        os.makedirs('labels')
    image_ids = open(txtsavepath+'/%s.txt' % (image_set)).read().strip().split()
    list_file = open('%s.txt' % (image_set), 'w')
    for image_id in image_ids:
        list_file.write(abs_path + '/images/%s.jpg\n' % (image_id))
       #convert_annotation(image_id)
    list_file.close()

# %%
