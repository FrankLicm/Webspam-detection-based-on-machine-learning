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
import linecache as lc
import TagTreeExtractor as tte
import  WordSeperater as ws

def main():
    HtmlTagNbData= "E:\\UnderGraduateDesign\\ExperimentSample\\AssetValue\\tagnb.txt"
    HtmlWordNbData = "E:\\UnderGraduateDesign\\ExperimentSample\\AssetValue\\wordnb.txt"
    HtmlTagWeightData = "E:\\UnderGraduateDesign\\ExperimentSample\\AssetValue\\tagassess.txt"
    HtmlWordWeightData = "E:\\UnderGraduateDesign\\ExperimentSample\\AssetValue\\wordassess.txt"
    TagDict ={}
    WordDict ={}
    TagWeight = {}
    WordWeight = {}
    Tags = lc.getlines(HtmlTagNbData)
    Words = lc.getlines(HtmlWordNbData)
    TagWeights = lc.getlines(HtmlTagWeightData)
    WordWeights = lc.getlines(HtmlWordWeightData)
    Total = 125
    Spam = 29
    NonSpam = 96
    for tag in Tags:
        tag1 = tag.split(" ")[0]
        proba = tag.split(" ")[1]
        proba = proba.split("\n")[0]
        TagDict.setdefault(tag1,proba)
    for word in Words:
        word1 = word.split(" ")[0]
        proba = word.split(" ")[1]
        proba = proba.split("\n")[0]
        WordDict.setdefault(word1,proba)
    for tagweight in TagWeights:
        tagweight1 = tagweight.split(" ")[0]
        fun = tagweight.split(" ")[1]
        fun = fun.split("\n")[0]
        TagWeight.setdefault(tagweight1,fun)
    for wordweight in WordWeights:
        wordweight1 = wordweight.split(" ")[0]
        fun = wordweight.split(" ")[1]
        fun = fun.split("\n")[0]
        WordWeight.setdefault(wordweight1,fun)
    HtmlDataPath = "E:\UnderGraduateDesign\ExperimentSample\HtmlSource2"
    HtmlFiles = os.listdir(HtmlDataPath)
    HtmlProbDict = {}
    for f in HtmlFiles:
        fo = open(HtmlDataPath + "/" + f,"r")
        html = fo.read()
        fo.close()
        taglist = tte.Extract(html)
        words = ws.ExtractCharacter(html)
        wordlist = ','.join(ws.SepWord(words)).split(",")
        Tprob = 1.0
        Wprob = 1.0
        for tag in taglist:
            if TagDict.has_key(tag) and TagWeight.has_key(tag):
                Tprob = Tprob*float(TagDict[tag])*float(TagWeight[tag])
        for word in wordlist:
            if WordDict.has_key(word) and WordWeight.has_key(word):
                 Wprob = Wprob*float(WordDict[word])*float(WordWeight[word])
        Tprob = Spam*Tprob
        Wprob = Spam*Wprob
        Allprob = Tprob*Wprob
        HtmlProbDict.setdefault(fng.DeGenerate(f),Allprob)
        print fng.DeGenerate(f),":",Allprob
    FunList = sorted(HtmlProbDict.items(), key=lambda e:e[1], reverse=True)
    for fun in FunList:
        print fun
main()
