#! /usr/bin/env python3
# -*- coding:utf-8 -*-
# @Time : 2023/11/14 14:03 
# @Author : JY
"""
文件操作相关
有些文件中文会报错，可以尝试encoding=‘gbk’
"""


class file:
    ENCODING_UTF8 = 'utf-8'
    ENCODING_GBK = 'gbk'

    def __init__(self):
        pass

    # 一次性读取txt文件的全部内容
    @staticmethod
    def readTxtFile(filePath, encoding=ENCODING_UTF8):
        with open(filePath, 'r', encoding=encoding) as f:
            content = f.read()
        return content

    # 按行读取txt的内容,返回一个生成器对象，如果想要数组结果，可以使用list把结果转一下：list(file.readTxtFileByLine('x.txt'))
    @staticmethod
    def readTxtFileByLine(filePath, encoding=ENCODING_UTF8):
        with open(filePath, 'r', encoding=encoding) as f:
            # 按行读取内容
            line = f.readline()
            while line:
                # 去除换行符并处理每行内容
                line = line.strip()
                # 打印每行内容或进行其他操作
                yield line
                line = f.readline()

    # 以追加的形式写文件
    @staticmethod
    def writeTxtFileAppendMode(filePath, content, encoding=ENCODING_UTF8):
        with open(filePath, 'a', encoding=encoding) as f:
            f.write(content)

    # 清空文件后写入
    @staticmethod
    def writeTxtFileNewMode(filePath, content, encoding=ENCODING_UTF8):
        with open(filePath, 'w', encoding=encoding) as f:
            f.write(content)

    # 得到文件的行数
    @staticmethod
    def countLines(filePath, encoding=ENCODING_UTF8):
        with open(filePath, 'r', encoding=encoding) as f:
            line_count = sum(1 for line in f)
        return line_count


if __name__ == '__main__':
    print(file.countLines(''))
