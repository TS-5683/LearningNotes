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

current_directory = os.getcwd()
imgList = os.listdir('images')
fileList = [f for f in os.listdir(current_directory) if 
            os.path.isfile(os.path.join(current_directory, f))]
print( fileList)

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
