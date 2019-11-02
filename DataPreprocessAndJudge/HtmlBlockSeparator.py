# -*- coding: UTF-8 -*-

import os,sys
stdi,stdo,stde=sys.stdin,sys.stdout,sys.stderr  
reload(sys)  
sys.setdefaultencoding( "utf-8" ) 
sys.stdin,sys.stdout,sys.stderr=stdi,stdo,stde
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
sys.path.insert(0,parentdir)
sys.path.insert(0,parentdir+"/Common")

from bs4 import BeautifulSoup
import re

def Separate(HtmlDataPath,BlockDataPath):
    blocklist = []
    HtmlFiles = os.listdir(HtmlDataPath)
    for f in HtmlFiles:
    #if True:
        print f
        tagList = []
        elemList = []
        attrList = []
        fo = open(HtmlDataPath + "/" + f, "r")
        #fo = open("E:\\UnderGraduateDesign\\Tests\\TestHtml4.html","r")
        html = fo.read()
        fo.close()
        soup = BeautifulSoup(html,"html5lib")
        #print soup.get_text("|")
        #切分html head
        #print soup.head.find_all('meta')
        #for meta in soup.head.find_all('meta'):
            #print meta.attrs
        #print soup.head.find_all('title')
        #切分html body
        #print len(list(soup.body.children))
        txt = re.compile("[^-~]")
        for elem in soup.body(text = txt):
            dname=""
            for parent in elem.parents:
                dname = dname + "-" + str(parent.name)
            if elem !=u'\n' and str(elem.parent.name) != "script":
                #print "dname:",dname
                #print "elem:",elem
                #print elem.parent.attrs
                tagList.append(dname)
                elemList.append(elem)
                attrList.append(elem.parent.attrs)
        for elem in soup.body(text =""):
            dname=elem.name
            for parent in elem.parents:
                dname = dname + "-" + str(parent.name)
            if str(elem.parent.name) != "script" and str(elem.name) != "script":
                #print "dname:",dname
                #print "elem:",""
                #print elem.attrs
                tagList.append(dname)
                elemList.append("")
                attrList.append(elem.attrs)
        print len(tagList)
        print len(elemList)
        print len(attrList)
        path = BlockDataPath+"\\"+f
        isExists=os.path.exists(path)
        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            # 创建目录操作函数
            os.makedirs(path) 
        i=0
        for tag in tagList:
            fo = open(BlockDataPath+"\\"+f+"\\"+str(i)+".txt", "ab+")
            fo.write("tag:"+tag+"\r\n")
            fo.write("elem:"+elemList[i]+"\r\n")
            fo.write("attrs:"+str(attrList[i])+"\r\n")
            fo.close()
            i=i+1
def SeparateWithHtml(html):
        tagList = []
        elemList = []
        attrList = []
        soup = BeautifulSoup(html,"html5lib")
        txt = re.compile("[^-~]")
        for elem in soup.body(text = txt):
            dname=""
            for parent in elem.parents:
                dname = dname + "-" + str(parent.name)
            if elem !=u'\n' and str(elem.parent.name) != "script":
                #print "dname:",dname
                #print "elem:",elem
                #print elem.parent.attrs
                tagList.append(dname)
                elemList.append(elem)
                attrList.append(elem.parent.attrs)
        for elem in soup.body(text =""):
            dname=elem.name
            for parent in elem.parents:
                dname = dname + "-" + str(parent.name)
            if str(elem.parent.name) != "script" and str(elem.name) != "script":
                #print "dname:",dname
                #print "elem:",""
                #print elem.attrs
                tagList.append(dname)
                elemList.append("")
                attrList.append(elem.attrs)
        return tagList,elemList,attrList
    
if __name__ == '__main__':
    #HtmlDataPath = "E:\\UnderGraduateDesign\\ExperimentSample\\Classification3\\Html"
    #BlockDataPath = "E:\\UnderGraduateDesign\\ExperimentSample\BlockSeparator\\all"
    #Separate(HtmlDataPath,BlockDataPath)
    htmlpath = "E:\\UnderGraduateDesign\\ExperimentSample\\Classification4\\nonspam\\http#9#2#261.191.61.213#98086"
    fo = open(htmlpath, "r")
    html = fo.read()
    fo.close()
    tagList,elemList,attrList=SeparateWithHtml(html)
    i=0
    for tag in tagList:
        blockarray =[]
        print tag
        text = elemList[i]
        print text
        i=i+1
