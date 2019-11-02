# -*- coding: UTF-8 -*-
import os,sys
stdi,stdo,stde=sys.stdin,sys.stdout,sys.stderr  
reload(sys)  
sys.setdefaultencoding( "utf-8" ) 
sys.stdin,sys.stdout,sys.stderr=stdi,stdo,stde
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
sys.path.insert(0,parentdir)
sys.path.insert(0,parentdir+"/Common")

import URLExtractor as urle
import FileNameGenerator  as fng
import HtmlContentGetter as hcg
import linecache as lc
from bs4 import BeautifulSoup
import re
import chardet

def main():
    fo = open("InputPath.conf", "r")
    inputPath = fo.read()
    dataFile = "E:\UnderGraduateDesign\ExperimentSample\DataSource\SuspectedLinks.log"
    autoDirectory = "E:\\UnderGraduateDesign\\ExperimentSample\\AutoDataTagging\\"
    fo.close()
    fo = open("OutputPath.conf","r")
    outputPath = fo.read()
    fo.close()
    files= os.listdir(inputPath) 
    for f in files:
         lineNumber = int(str(f).split("~")[0])+1
         print lineNumber
         word = lc.getline(dataFile, lineNumber).split("	")[1].split("\n")[0]
         if isinstance(word, unicode):
             pass
         else:
             codesty = chardet.detect(word)
             word=word.decode(codesty['encoding'])
         print word
         print urle.ExtractFromFileName(str(f))
         fo = open(inputPath+"/"+f,"r")
         html = fo.read()
         fo.close()
         soup = BeautifulSoup(html,"lxml")
         txt = re.compile(word)
         print "txt:",txt
         for elem in soup(text = txt):
            dname = ""
            for parent in elem.parents:
               dname=dname +"-"+ fng.Generate(str(parent.name))
            autoPath = autoDirectory+dname
            if not os.path.exists(autoPath):           
                os.mkdir(autoPath)
            if dname is not "":
                try:
                    foo = open(autoPath + "\\"+f,"wb")
                    foo.write(html)
                    foo.close()
                except Exception as e:
                    pass

if __name__ == '__main__':
    main()
