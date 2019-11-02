# -*- coding: UTF-8 -*-

import os,sys
stdi,stdo,stde=sys.stdin,sys.stdout,sys.stderr  
reload(sys)  
sys.setdefaultencoding( "utf-8" ) 
sys.stdin,sys.stdout,sys.stderr=stdi,stdo,stde
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
sys.path.insert(0,parentdir)
sys.path.insert(0,parentdir+"/Common")

import math
from bs4 import BeautifulSoup
import re
import jieba
import jieba.analyse

def SepWord(sentence):
    jieba.analyse.set_stop_words('E:\\UnderGraduateDesign\\ExperimentSample\\stopwords.txt')
    return jieba.analyse.extract_tags(sentence, topK = 99999, withWeight = False, allowPOS = ())

#计算优势率
#A 为词条 t 和spam样本同时出现的块数目
#B 为词条 t 和非spam样本同时出现的块数目
#C 为所有的spam样本的块数目
#D为所有非spam样本的块数目
def ComputeOR(A,B,C,D):
    #print A,B,C,D
    A=A+1
    B=B+1
    #if A*(D-B)!=0 and B*(C-A) !=0  :
    return (A*(D-B))/(B*(C-A))
    #elif A*(D-B)==0:
    #   return 0
    #elif B*(C-A)==0:
    #    return 10000000000

# 计算Text在head中的A,B,C,D，并返回Text字典，其中键为词，值为A和B，还要返回C和D
# 其中非spam样本数不包括不存在title和meta的head
def HeadTextORCompute(HeadSpamPath,HeadNonSpamPath):
    TextDict={}
    SpamHtmlFiles = os.listdir(HeadSpamPath)
    NonSpamHtmlFiles = os.listdir(HeadNonSpamPath)
    C = 0
    D = 0
    for f in SpamHtmlFiles:
        fo = open(HeadSpamPath + "\\" + f, "r")
        html = fo.read()
        fo.close()
        soup = BeautifulSoup(html,"html5lib")
        metas = soup.head.find_all('meta')
        text = ""
        array = [0,0]
        flag=0
        for meta in metas:
            flag=1
            for key in meta.attrs:
                if key == "content":
                    text=text+meta.attrs[key]
                    array[0]=1
                    #print meta.attrs[key]
                    #print TAG.Generate(meta.attrs[key])
        titles = soup.head.find_all('title')
        for title in titles:
            flag=1
            array[1]=1
            text = text+title.text
            #print "title:",title.text
        #print text
        if flag==1:
            C=C+1
        strings = ','.join(SepWord(text.decode("utf8"))).split(",")
        for word in strings:
            TextDict.setdefault(word, [0,0])
            TextDict[word][0] = TextDict[word][0] +1
    for f in NonSpamHtmlFiles:
        fo = open(HeadNonSpamPath + "\\" + f, "r")
        html = fo.read()
        fo.close()
        soup = BeautifulSoup(html,"html5lib")
        metas = soup.head.find_all('meta')
        text = ""
        array = [0,0]
        flag=0
        for meta in metas:
            flag=1
            for key in meta.attrs:
                if key == "content":
                    text=text+meta.attrs[key]
                    array[0]=1
                    #print meta.attrs[key]
                    #print TAG.Generate(meta.attrs[key])
        titles = soup.head.find_all('title')
        for title in titles:
            flag=1
            array[1]=1
            text = text+title.text
            #print "title:",title.text
        #print text
        if flag==1:
            D=D+1
        strings = ','.join(SepWord(text.decode("utf8"))).split(",")
        for word in strings:
            #if word == u"突鹰":
                    #print f
            TextDict.setdefault(word, [0,0])
            TextDict[word][1] = TextDict[word][1] +1
    return TextDict,C,D

# 计算text 在body中的A,B,C,D, 并计算出优势率，从大到小排序存入文件
# 其中spam样本数和非spam样本数以块为单位,并且只计入有TEXT内容的块
def BodyTextORCompute(BodyBlockSpamPath, BodyBlockNonSpamPath,TextDict,C,D,ORFilePath):
    BodyBlockSpamPaths=os.listdir(BodyBlockSpamPath)
    BodyBlockNonSpamPaths = os.listdir(BodyBlockNonSpamPath)
    for path in BodyBlockSpamPaths:
        paths = os.listdir(BodyBlockSpamPath+"\\"+path)
        for pa in paths:
            flag = 0
            text=""
            fo= open(BodyBlockSpamPath+"\\"+path+"\\"+pa,"r")
            while 1:
                line = fo.readline()
                if not line:
                    break;
                if "tag:" in line:
                    pass
                elif "elem:" in line:
                    text= text+line.split("elem:")[1]
                elif "attrs:" in line:
                    ChineseReg=u'[\u4E00-\u9FA5]+'
                    AttrDict = eval(line.split("attrs:")[1])
                    for key in AttrDict:
                        try:
                            if re.match(ChineseReg,AttrDict[key],re.I):
                                text= text+AttrDict[key]
                        except TypeError:
                            pass
            fo.close()
            #print text
            strings = ','.join(SepWord(text.decode("utf8"))).split(",")
            for word in strings:
                flag =1
                TextDict.setdefault(word, [0,0])
                TextDict[word][0] = TextDict[word][0] +1
            if flag==1:
                C=C+1
                
    for path in BodyBlockNonSpamPaths:
        paths = os.listdir(BodyBlockNonSpamPath+"\\"+path)
        for pa in paths:
            text=""
            flag = 0
            fo= open(BodyBlockNonSpamPath+"\\"+path+"\\"+pa,"r")
            while 1:
                line = fo.readline()
                if not line:
                    break;
                if "tag:" in line:
                    pass
                elif "elem:" in line:
                    text=  text+line.split("elem:")[1]
                elif "attrs:" in line:
                    ChineseReg=u'[\u4E00-\u9FA5]+'
                    AttrDict = eval(line.split("attrs:")[1])
                    for key in AttrDict:
                        try:
                            if re.match(ChineseReg,AttrDict[key],re.I):
                                text= text+AttrDict[key]
                        except TypeError:
                            pass
            fo.close()
            #print text
            strings = ','.join(SepWord(text.decode("utf8"))).split(",")
            for word in strings:
                flag=1
                #if word == u"开奖":
                   #print path
                TextDict.setdefault(word, [0,0])
                TextDict[word][1] = TextDict[word][1] +1
            if flag == 1:
                D=D+1
    ValueDict = {}
    #print "C:",C
    #print "D:",D
    i=0
    for key in TextDict:
        i+=1
        print i                                    
        A = float(TextDict[key][0])
        B = float(TextDict[key][1])
        ORValue = ComputeOR(A,B,float(C),float(D))
        #print ORValue
        ValueDict[key] = ORValue
    ValueList = sorted(ValueDict.items(), key=lambda e:e[1], reverse=True)
    for value in ValueList:
        fo = open(ORFilePath,"ab+")
        fo.write(value[0]+" "+str(TextDict[value[0]][0])+" "+str(TextDict[value[0]][1])+" "+str(value[1])+"\n")
        fo.close()


if __name__ == '__main__':
    HeadSpamPath = "E:\\UnderGraduateDesign\\ExperimentSample\\Classification3\\headspam"
    HeadNonSpamPath = "E:\\UnderGraduateDesign\\ExperimentSample\\Classification3\\nonheadspam"
    BodyBlockSpamPath ="E:\\UnderGraduateDesign\\ExperimentSample\\BlockSeparator\\spam"
    BodyBlockNonSpamPath = "E:\\UnderGraduateDesign\\ExperimentSample\\BlockSeparator\\nonspam"
    ORFilePath = "E:\\UnderGraduateDesign\\ExperimentSample\\AssetValue\\TextAB+1ORValueWithoutLog.txt"
    returnlist = HeadTextORCompute(HeadSpamPath,HeadNonSpamPath)
    BodyTextORCompute(BodyBlockSpamPath, BodyBlockNonSpamPath,returnlist[0],returnlist[1],returnlist[2],ORFilePath)





    
