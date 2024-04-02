# utf-8
# 删除图片文件夹中的无效图片
# 无效：在某个.md文件中通过文件名被引用即为有效

import os
import re
import sys

def read_all_text_files(directory):
    lineSet = set()
    for fileName in os.listdir(directory):
        if fileName.endswith('.md'):
            with open(fileName, encoding='utf-8') as f:
                for line in f:
                    if re.search(r'images', line, re.IGNORECASE):
                        lineSet.add(line.strip())
    return lineSet

current_directory = os.getcwd()
print("开始扫描\n---------------------")
n = 0

# 读取所有文本文件到lineSet
lineSet = set()
try:
    lineSet = read_all_text_files(current_directory)
except Exception as e:
    print(e)
    sys.exit(-1)

# 图片循环
imgList = os.listdir('images')
for imgName in imgList:
    if not any(re.search(imgName, line, re.IGNORECASE) for line in lineSet):
        try:
            os.remove(os.path.join('images', imgName))
            n += 1
            print(f'删除：{imgName}')
        except Exception as e:
            print(f"删除图片：{imgName} 失败\n{e}")
print("\n---------------------")
print(f"扫描结束，删除图片数量：{n}")