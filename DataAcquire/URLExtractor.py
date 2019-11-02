# -*- coding: UTF-8 -*-

def Extract(text):
    text = str(text)
    if "http" in text:
        text = text.split("\t")
        return text[0]
    else:
        return ""
if __name__ == '__main__':
    print Extract("http://gjjyxy.cug.edu.cn	开奖结果")
    print Extract("dsfsad")
