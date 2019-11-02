# -*- coding: UTF-8 -*-
import FileNameGenerator as FNG

def Extract(text):
    text = str(text)
    if "http" in text:
        text = text.split("\t")
        return text[0]
    else:
        return ""

def ExtractFromFileName(name):
    name=str(name)
    if "http" in name and "~" in name:
        name=name.split("~")[1]
        name=FNG.DeGenerate(name)
        return name
    else:
        return ""
if __name__ == '__main__':
    #print Extract("http://gjjyxy.cug.edu.cn	开奖结果")
    #print Extract("dsfsad")
    print ExtractFromFileName("39~http#9#2#2www.lnsmzy.edu.cn#2xsyd#2tw#2schoolradio#22009122208180870910.shtml")
