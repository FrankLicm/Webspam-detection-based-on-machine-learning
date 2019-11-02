# -*- coding: UTF-8 -*-

import os,sys
stdi,stdo,stde=sys.stdin,sys.stdout,sys.stderr  
reload(sys)  
sys.setdefaultencoding( "utf-8" ) 
sys.stdin,sys.stdout,sys.stderr=stdi,stdo,stde
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
sys.path.insert(0,parentdir)
sys.path.insert(0,parentdir+"/Common")

import jieba
import jieba.analyse
import linecache as lc
import re
import  chardet

def SepWord(sentence):
    jieba.analyse.set_stop_words('E:\\UnderGraduateDesign\\Source\\DataJudgement\\stopwords.txt')
    return jieba.analyse.extract_tags(sentence, topK = 99999, withWeight = False, allowPOS = ())

def AddToSpam(word):
    fo =  open("E:\UnderGraduateDesign\ExperimentSample\Dict\SpamDict1.txt","ab+")
    fo.write(word+"\n")
    fo.close()
    
def IsSpam(word):
    words = lc.getlines("E:\UnderGraduateDesign\ExperimentSample\Dict\SpamDict1.txt")
    if word in words:
        return True
    return False
    
def BuildSpamDict():
    words = lc.getlines("E:\UnderGraduateDesign\ExperimentSample\DataSource\sss.log")
    wdict=[]
    for line in words:
        word = line.split("	")[1].split("\n")[0]
        if word not in wdict:
            AddToSpam(word)
            wdict.append(word)
            print word

def ExtractCharacter(s):
    r = re.sub(u"[^\u4e00-\u9fa5]", "", s.decode("utf-8",'ignore'))
    return r

if __name__ == '__main__':
    HtmlDataPath = "E:\UnderGraduateDesign\ExperimentSample\HtmlSource"
    SpamDataPath = "E:\UnderGraduateDesign\ExperimentSample\Classification3\spam"
    NonSpamDataPath = "E:\UnderGraduateDesign\ExperimentSample\Classification3\\nonspam"
    HtmlFiles = os.listdir(HtmlDataPath)
    SpamFiles = os.listdir(SpamDataPath)
    NonSpamFiles = os.listdir(NonSpamDataPath)
    SpamNum = 29
    NonSpamNum = 96
    Total = SpamNum + NonSpamNum
    WordDict = {}
    #for f in HtmlFiles:
       #fo = open(HtmlDataPath + "/" + f, "r")
       #html = fo.read()
       #fo.close()
       #words = ExtractCharacter(html)
       #print words
       #strings = ','.join(SepWord(words)).split(",")
       #for string in strings:
           #WordDict.setdefault(string, [0,0])
    for f in SpamFiles:
       fo = open(SpamDataPath + "/" + f, "r")
       html = fo.read()
       chardit1 = chardet.detect(html)
       html=html.decode(chardit1['encoding'],"ignore").encode('utf-8',"ignore")
       fo.close()
       words = ExtractCharacter(html)
       strings = ','.join(SepWord(words)).split(",")
       for string in strings:
           WordDict.setdefault(string, [0,0])
           WordDict[string][0] = WordDict[string][0] +1
    for f in NonSpamFiles:
       fo = open(NonSpamDataPath + "/" + f, "r")
       html = fo.read()
       fo.close()
       words = ExtractCharacter(html)
       strings = ','.join(SepWord(words)).split(",")
       for string in strings:
           WordDict.setdefault(string, [0,0])
           WordDict[string][1] = WordDict[string][1] +1
    FunDict = {}
    for key in WordDict:
        A = float(WordDict[key][0])
        B = float(WordDict[key][1])
        C = float(SpamNum - A)
        D = float(NonSpamNum - B)
        P = A/SpamNum
        #fun = Total*(((A*D-C*B)*(A*D-C*B))/((A+C)*(B+D)*(A+B)*(C+D)))
        fun = P
        if (A*D-C*B)>0:
            FunDict[key] = fun
    FunList = sorted(FunDict.items(), key=lambda e:e[1], reverse=True)
    for function in FunList:
        fo = open("E:\UnderGraduateDesign\ExperimentSample\AssetValue\\wordnb.txt", "ab+")
        fo.write(function[0]+" "+str(function[1])+"\n")
        fo.close()
        print function[0]," ",function[1]
           
