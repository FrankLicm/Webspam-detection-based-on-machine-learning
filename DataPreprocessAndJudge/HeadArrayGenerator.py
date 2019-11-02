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
import TextArrayGenerator as TAG

def Generate(html):
    soup = BeautifulSoup(html,"html5lib")
    metas = soup.head.find_all('meta')
    text = ""
    array = [0,0]
    for meta in metas:
        for key in meta.attrs:
            if key == "content":
                text=text+meta.attrs[key]
                array[0]=1
                #print meta.attrs[key]
                #print TAG.Generate(meta.attrs[key])
    titles = soup.head.find_all('title')
    for title in titles:
        array[1]=1
        text = text+title.text
        #print "title:",title.text
    print text
    return array+TAG.Generate(text)

def GenerateHeadText(html):
    soup = BeautifulSoup(html,"html5lib")
    metas = soup.head.find_all('meta')
    text = ""
    array = [0,0]
    for meta in metas:
        for key in meta.attrs:
            if key == "content":
                text=text+meta.attrs[key]
                array[0]=1
                #print meta.attrs[key]
                #print TAG.Generate(meta.attrs[key])
    titles = soup.head.find_all('title')
    for title in titles:
        array[1]=1
        text = text+title.text
        #print "title:",title.text
    return text
    
if __name__ == '__main__':
    fo = open("E:\UnderGraduateDesign\Tests\TestHtml.html","r")
    html = fo.read()
    fo.close()
    Generate(html)
    
