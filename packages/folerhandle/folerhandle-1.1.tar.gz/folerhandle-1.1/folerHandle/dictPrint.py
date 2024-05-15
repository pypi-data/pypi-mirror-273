# -*- coding:utf-8 -*-
"""
@Author: 风吹落叶
@Contact: waitKey1@outlook.com
@Version: 1.0
@Date: 2024/5/15 15:10
@Describe: 
"""
import json

def print_dict_as_treeV2(d, indent=0):
    """
    递归打印一个字典，模仿文件树的格式。

    :param d: 要打印的字典
    :param indent: 当前缩进级别
    """
    if indent==0:
        outStr='{:<36} DirSize:{:<8} FileNum:{}'.format('DirName:'+d['DirName'][:16],d['TotalSize'],d['FileNum'])
    else:
        outStr = '{:<36} DirSize:{:<8} FileNum:{}'.format('..' * (indent) + '|--' + 'DirName:' + d['DirName'][:16], d['TotalSize'],d['FileNum'])
    print(outStr)
    dirs=d['Dirs']
    for dir in dirs:
        print_dict_as_treeV2(dir,indent+1)


if __name__ == '__main__':
    print('---*--- 哲灵文件结构简要分析 ---*---')
    print('文件夹树如下：')
    # 示例字典
    with open('test.json', 'r', encoding='utf-8') as r:
        jsonData = json.load(r)
    print_dict_as_treeV2(jsonData)
    print('注：下一层全部文件夹大小之和<=上一层文件夹大小，是因为一个目录下的总大小计算公式是：文件夹大小和+文件大小和')
    print('为了方便就不列出详细的文件树了，详情请查看导出的Json文件')
