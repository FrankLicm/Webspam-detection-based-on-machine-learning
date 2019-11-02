# -*- coding: UTF-8 -*-

import os,sys
stdi,stdo,stde=sys.stdin,sys.stdout,sys.stderr  
reload(sys)  
sys.setdefaultencoding( "utf-8" ) 
sys.stdin,sys.stdout,sys.stderr=stdi,stdo,stde
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
sys.path.insert(0,parentdir)
sys.path.insert(0,parentdir+"/Common")
import re
import jieba
import jieba.analyse
import TextAnalysis as TA

def SepWord(sentence):
    jieba.analyse.set_stop_words('E:\\UnderGraduateDesign\\ExperimentSample\\stopwords.txt')
    return jieba.analyse.extract_tags(sentence, topK = 99999, withWeight = False, allowPOS = ())

def Generate(text,worddict,wordlist):
    #print wordlist
    WordArray = [ 0 for n in range(len(wordlist))]
    #print text.decode("utf8"),":",[text]
    strings = ','.join(SepWord(text.decode("utf8"))).split(",")
    for string in strings:
        if string in wordlist:
            WordArray[wordlist.index(string)] = 1
    return WordArray

#计算所有分词的平均优势率，及优势率之和除以分词个数
#如果全部存在，则直接带入计算，返回平均优势率
#如果部分存在，计算存在部分平均优势率并返回不存在的词集合
#如果全部不存在，返回不存在的词集合
def ComputeORValue(worddict,text):
    strings = ','.join(TA.SepWord(text.decode("utf8"))).split(",")
    ORsum =0
    ORnum = 0
    unexist = []
    exist = []
    flag = 0
    strings2 = list(set(strings)) 
    for word in strings2:
        if word in worddict:
            ORsum = ORsum+worddict[word][2]
            ORnum +=1
            exist.append(word)
        else:
            flag = 1
            unexist.append(word)
    if ORnum == 0:
        return 0,unexist,exist
    return float(ORsum)/float(ORnum),unexist,exist
if __name__ == '__main__':
    print Generate("")
















    
    
