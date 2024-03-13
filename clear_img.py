# utf-8
# 删除图片文件夹中的无效图片


import os
import re

def read_all_text_files(directory):
    lineSet = set()
    for fileName in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, fileName)):
            with open(fileName, encoding='utf-8') as f:
                for line in f:
                    if re.search(r'images', line, re.IGNORECASE):
                        lineSet.add(line.strip())
    return lineSet


current_directory = os.getcwd()
print("开始扫描\n---------------------")
n = 0

# 读取所有文本文件到lineSet
lineSet = read_all_text_files(current_directory)

# 图片循环
imgList = os.listdir('images')
for imgName in imgList:
    if not any(re.search(imgName, line, re.IGNORECASE) for line in lineSet):
        try:
            os.remove(os.path.join('images', imgName))
            n += 1
            print(f'删除图片：{imgName} 成功')
        except Exception as e:
            print(f"删除图片：{imgName} 失败\n{e}")

print("\n---------------------")
print(f"扫描结束，删除图片数量：{n}")