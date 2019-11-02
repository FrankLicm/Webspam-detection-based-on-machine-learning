# -*- coding: UTF-8 -*-

import os,sys,shutil
stdi,stdo,stde=sys.stdin,sys.stdout,sys.stderr  
reload(sys)  
sys.setdefaultencoding( "utf-8" ) 
sys.stdin,sys.stdout,sys.stderr=stdi,stdo,stde
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
sys.path.insert(0,parentdir)
sys.path.insert(0,parentdir+"/Common")

import HtmlBlockSeparator as HBS
import HeadArrayGenerator as HAG
import AttributeArrayGenerator as AAG
import TagArrayGenerator as TAG
import TextArrayGenerator as TAG1
from sklearn.naive_bayes import MultinomialNB
from sklearn.externals import joblib
import numpy as np

from bs4 import BeautifulSoup
import re

def Judge(addr,worddict,html,ORValueFilePath,nb_clf,KeyList,AllkeyValueDict):
    definitethreshold = float(40)
    possiblethreshold = float(36)
    soup = BeautifulSoup(html,"html5lib")
    headtext = HAG.GenerateHeadText(html)
    headorvalue = float(0)
    flag =  0
    if headtext!="" and re.match("[^\s]",headtext,re.I):
        headorvalue,unexist,exist = TAG1.ComputeORValue(worddict,headtext)
        #print headorvalue
    if headorvalue > possiblethreshold:
        print addr," head is spam"
        unexistorvalue = float(36.8848708487)
        for word in unexist:
            worddict[word.decode("utf8")] = (1,0,unexistorvalue)
        for word in exist:
            #print word
            A = float(worddict[word.decode("utf8")][0])+1
            ORValue = (float(1)+float(1)/float(A))*float(worddict[word.decode("utf8")][2])
            newA= A+1
            worddict[word.decode("utf8")] = (newA,worddict[word.decode("utf8")][1],ORValue)
        flag = 1
    elif headorvalue>float(0) and headorvalue <=possiblethreshold:
        print addr," head is not spam"
        unexistorvalue = float(9.21942446043)
        for word in unexist:
            #print word
            worddict[word.decode("utf8")] = (0,1,unexistorvalue)
        for word in exist:
            #print word
            B = float(worddict[word.decode("utf8")][1])+1
            ORValue = (1/(float(1)+float(1)/float(B)))*float(worddict[word.decode("utf8")][2])
            newB= B+1
            worddict[word.decode("utf8")] = (worddict[word.decode("utf8")][0],newB,ORValue)
    else:
        pass
    tagList,elemList,attrList = HBS.SeparateWithHtml(html);
    i=0
    for tag in tagList:
        blockarray =[]
        tagarray = TAG.Generate(tag)
        text = elemList[i]
        attrsarray,text = AAG.Generate(str(attrList[i]),text,worddict,KeyList,AllkeyValueDict)
        i=i+1
        if text!="":
            #print text
            blockarray.extend(tagarray)
            blockarray.extend(attrsarray)
        else:
            continue
        if len(blockarray) != 4071:
                print "the lenth of the array is not correct:",addr
                print "len:",len(blockarray)
        orvalue,unexist,exist = TAG1.ComputeORValue(worddict,text)
        #print orvalue
        possibility = nb_clf.predict(blockarray)
        if orvalue>=definitethreshold:           
            flag = flag + 1
            print addr," block is spam"
            unexistorvalue = float(36.8848708487)
            for word in unexist:
                #print word
                worddict[word.decode("utf8")] = (1,0,unexistorvalue)
            for word in exist:
                #print word
                A = float(worddict[word.decode("utf8")][0])+1
                ORValue = (float(1)+float(1)/float(A))*float(worddict[word.decode("utf8")][2])
                newA= A+1
                worddict[word.decode("utf8")] = (newA,worddict[word.decode("utf8")][1],ORValue)
            if possibility!=[1]:
                nb_clf.partial_fit(blockarray, [1], classes=np.array([0, 1]))
        elif orvalue<definitethreshold and orvalue>possiblethreshold and possibility==[1]:
            flag = flag + 1
            print "possiblility:",possibility
            print addr," block is spam"
            unexistorvalue = float(36.8848708487)
            for word in unexist:
                #print word
                worddict[word.decode("utf8")] = (0,1,unexistorvalue)
            for word in exist:
                #print word
                A = float(worddict[word.decode("utf8")][0])+1
                ORValue = (float(1)+float(1)/float(A))*float(worddict[word.decode("utf8")][2])
                newA= A+1
                worddict[word.decode("utf8")] = (newA,worddict[word.decode("utf8")][1],ORValue)
            #nb_clf.partial_fit(blockarray, [0], classes=np.array([0, 1]))
        elif orvalue<definitethreshold and orvalue>possiblethreshold and possibility==[0]:
            #print "possiblility:",possibility
            #print addr," block is not spam"
            unexistorvalue = float(36.8848708487)
            for word in unexist:
                #print word
                worddict[word.decode("utf8")] = (1,0,unexistorvalue)
            for word in exist:
                #print word
                B = float(worddict[word.decode("utf8")][1])+1
                ORValue = (1/(float(1)+float(1)/float(B)))*float(worddict[word.decode("utf8")][2])
                newB= B+1
                worddict[word.decode("utf8")] = (worddict[word.decode("utf8")][0],newB,ORValue)
            #nb_clf.partial_fit(blockarray, [0], classes=np.array([0, 1]))
        elif orvalue<=possiblethreshold:
            #print "possiblility:",possibility
            #print addr," block is not spam"
            unexistorvalue = float(9.21942446043)
            for word in unexist:
                #print word
                worddict[word.decode("utf8")] = (0,1,unexistorvalue)
            for word in exist:
                #print word
                B = float(worddict[word.decode("utf8")][1])+1
                ORValue = (1/(float(1)+float(1)/float(B)))*float(worddict[word.decode("utf8")][2])
                newB= B+1
                worddict[word.decode("utf8")] = (worddict[word.decode("utf8")][0],newB,ORValue)
            if possibility!=[0]:
                 nb_clf.partial_fit(blockarray, [0], classes=np.array([0, 1]))
    if flag>0:
        return True,nb_clf,worddict
    else:
        return False,nb_clf,worddict

if __name__== '__main__':
    KeyEnumFilePath = "E:\UnderGraduateDesign\ExperimentSample\\Key.txt"
    ORValueFilePath = "E:\\UnderGraduateDesign\\ExperimentSample\\AssetValue\\TextAB+1ORValueWithoutLog.txt"
    NewORValueFilePath = "E:\\UnderGraduateDesign\\ExperimentSample\\AssetValue\\TextAB+1ORValueWithoutLogV10.txt"
    ModelFilePath = "E:\\UnderGraduateDesign\\ExperimentSample\\model\\nb_train_model_without_text_with_text.m"
    NewModelFilePath = "E:\\UnderGraduateDesign\\ExperimentSample\\model\\nb_train_model_without_text_with_text_v10.m"
    HtmlDataPath ="E:\\UnderGraduateDesign\\ExperimentSample\\HtmlSource2"
    SpamPath = "E:\\UnderGraduateDesign\\ExperimentSample\\Classification8\\spam"
    NonSpamPath = "E:\\UnderGraduateDesign\\ExperimentSample\\Classification8\\nonspam"
    AttributesDirectoryPath = "E:\\UnderGraduateDesign\\ExperimentSample\\Attributes"
    errordatapath = "E:\UnderGraduateDesign\ExperimentSample\errordata" 
    KeyList,AllkeyValueDict = AAG.init(KeyEnumFilePath, AttributesDirectoryPath)
    worddict = {}
    fo = open(ORValueFilePath,"r")
    while 1:
        line= fo.readline()
        if not line:
            break
        word = line.split(" ")[0]
        A = float(line.split(" ")[1])
        B = float(line.split(" ")[2])
        C = float(line.split(" ")[3])
        worddict[word.decode("utf8")] = (A,B,C)
    nb_clf = joblib.load(ModelFilePath)
    HtmlFiles = os.listdir(HtmlDataPath)
    k=0
    for f in HtmlFiles:
        k=k+1
        print k
        fo = open(HtmlDataPath + "\\" + f, "r")
        html = fo.read()
        fo.close()
        judge,nb_clf,wordict=Judge(str(f),worddict,html,ORValueFilePath,nb_clf,KeyList,AllkeyValueDict)
        if judge:
            print str(f)+"is spam"
            fo = open(SpamPath + "\\" + f, "w")
            fo.write(html)
            fo.close()
        else:
            print str(f)+"is not spam"
            fo = open(NonSpamPath + "\\" + f, "w")
            fo.write(html)
            fo.close()
    for word in worddict:
        fo  = open(NewORValueFilePath,"ab+")
        fo.write(word.decode("utf8")+" "+str(int(worddict[word.decode("utf8")][0]))+" "+str(int(worddict[word.decode("utf8")][1]))+" "+str(worddict[word.decode("utf8")][2])+"\n")
        fo.close()
    joblib.dump(nb_clf, NewModelFilePath)

#以下对于单个网页文件进行判断测试
if __name__!= '__main__':
    KeyEnumFilePath = "E:\UnderGraduateDesign\ExperimentSample\\Key.txt"
    ORValueFilePath = "E:\\UnderGraduateDesign\\ExperimentSample\\AssetValue\\TextAB+1ORValueWithoutLog.txt"
    NewORValueFilePath = "E:\\UnderGraduateDesign\\ExperimentSample\\AssetValue\\TextAB+1ORValueWithoutLogV9.txt"
    ModelFilePath = "E:\\UnderGraduateDesign\\ExperimentSample\\model\\nb_train_model_without_text_with_text.m"
    NewModelFilePath = "E:\\UnderGraduateDesign\\ExperimentSample\\model\\nb_train_model_without_text_with_text_v9.m"
    HtmlDataPath ="E:\\UnderGraduateDesign\\ExperimentSample\\HtmlSource2"
    SpamPath = "E:\\UnderGraduateDesign\\ExperimentSample\\Classification4\\spam"
    NonSpamPath = "E:\\UnderGraduateDesign\\ExperimentSample\\Classification4\\nonspam"
    AttributesDirectoryPath = "E:\\UnderGraduateDesign\\ExperimentSample\\Attributes"
    KeyList,AllkeyValueDict = AAG.init(KeyEnumFilePath, AttributesDirectoryPath)
    worddict = {}
    fo = open(NewORValueFilePath,"r")
    while 1:
        line= fo.readline()
        if not line:
            break
        word = line.split(" ")[0]       
        A = line.split(" ")[1]
        B = line.split(" ")[2]
        #print word,line.split(" ")[3]
        C = float(line.split(" ")[3])
        worddict[word.decode("utf8")] = (A,B,C)
    nb_clf = joblib.load( NewModelFilePath)
    htmlpath = "E:\\UnderGraduateDesign\\ExperimentSample\\TestClassification\\nonspamwrong\\http#9#2#2hqjt.nuaa.edu.cn#2"
    fo = open(htmlpath, "r")
    html = fo.read()
    fo.close()
    judge,nb_clf,wordict=Judge("http#9#2#2hqjt.nuaa.edu.cn#2",worddict,html,NewORValueFilePath,nb_clf,KeyList,AllkeyValueDict)
    print judge
