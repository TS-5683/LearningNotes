# utf-8
# 删除图片文件夹中的无效图片


import os


# 判断文本文件fileName是否包含关键词word
def inFile(word:str ,fileName:str) -> bool:
    file = open(fileName, encoding='utf-8')
    if word in file.read(): 
        file.close()
        return True
    file.close()
    return False


imgList = os.listdir('images')
fileList = ['网络协议.md' ,'C++11内存.md', 'C++并发.md' ,'C++新标准.md' ,'MySQL常用.md']

# 图片循环
for imgName in imgList:
    flag = False
    for file in fileList:
        if inFile(imgName, file):
            flag = True
            break
    if not flag:
        print('删除图片：'+imgName)
        os.remove('images\\'+imgName)
