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
import FileNameGenerator  as fng

def Extract(html):
    tagList=[]
    contentList=[]
    soup = BeautifulSoup(html,"lxml")
    txt = re.compile("[^-~]")
    for elem in soup(text = txt):
        dname=""
        for parent in elem.parents:
            dname = dname + "-" + fng.Generate(str(parent.name))
        if str(elem.parent.name) != "script" and dname not in tagList:
            tagList.append(dname)
    return tagList

def ExtractByWord(html,word):
    tagList=[]
    contentList=[]
    soup = BeautifulSoup(html,"lxml")
    txt = re.compile(word)
    for elem in soup(text = txt):
        dname=""
        for parent in elem.parents:
            dname = dname + "-" + fng.Generate(str(parent.name))
        if str(elem.parent.name) != "script" and dname not in tagList:
            tagList.append(dname)
    return tagList
    
if __name__ == '__main__':
    #foo = open("E:\UnderGraduateDesign\Tests\TestHtml.html","r")
    #html = foo.read()
    #foo.close()
    #print Extract(html)
    #print ExtractByWord(html, u"校")
    SpamNum = 29
    NonSpamNum = 96
    Total = SpamNum + NonSpamNum
    SpamDataPath = "E:\UnderGraduateDesign\ExperimentSample\Classification3\spam"
    NonSpamDataPath = "E:\UnderGraduateDesign\ExperimentSample\Classification3\\nonspam"
    SpamFiles = os.listdir(SpamDataPath)
    NonSpamFiles = os.listdir(NonSpamDataPath)
    TagDict ={}
    for f in SpamFiles:
       fo = open(SpamDataPath + "/" + f, "r")
       html = fo.read()
       fo.close()
       taglist = Extract(html)
       for tag in taglist:
           TagDict.setdefault(tag,[0,0])
           TagDict[tag][0] = TagDict[tag][0]+1
    for f in NonSpamFiles:
       fo = open(NonSpamDataPath + "/" + f, "r")
       html = fo.read()
       fo.close()
       taglist = Extract(html)
       for tag in taglist:
           TagDict.setdefault(tag,[0,0])
           TagDict[tag][1] = TagDict[tag][1]+1
    FunDict = {}
    for key in TagDict:
        A = float(TagDict[key][0])
        B = float(TagDict[key][1])
        C = float(SpamNum - A)
        D = float(NonSpamNum - B)
        P = A/SpamNum
        #fun = Total*(((A*D-C*B)*(A*D-C*B))/((A+C)*(B+D)*(A+B)*(C+D)))
        fun = P
        if (A*D-C*B)>0:
            FunDict[key] = fun
    FunList = sorted(FunDict.items(), key=lambda e:e[1], reverse=True)
    for function in FunList:
        fo = open("E:\UnderGraduateDesign\ExperimentSample\AssetValue\\tagnb.txt", "ab+")
        fo.write(function[0]+" "+str(function[1])+"\n")
        fo.close()
        print function[0]," ",function[1]
