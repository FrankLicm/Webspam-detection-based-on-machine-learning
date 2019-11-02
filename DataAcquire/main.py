# -*- coding: UTF-8 -*-
import GetHtmlData as ghd
import ReadConf as rc
import SaveDataInFile as sdif
import URLExtractor as urle
import FileNameGenerator as FNG
import os
import sys
stdi,stdo,stde=sys.stdin,sys.stdout,sys.stderr  
reload(sys)  
sys.setdefaultencoding( "utf-8" ) 
sys.stdin,sys.stdout,sys.stderr=stdi,stdo,stde

def main():
    conf = rc.ReadConf()
    inputPath = conf[0]
    outputPath = conf[1]
    errorPath = conf[2]
    files= os.listdir(inputPath)
    for f in files:
        if not os.path.isdir(f):
            fo = open(inputPath+"/"+f)
            #print f,"is opened successfully!"
            iter_f = iter(fo)
            #print iter_f
            count = -1
            for line in iter_f:
                count +=1
                print count
                html=""
                url=urle.Extract(line)
                if url != "":
                    print "url:",url, "is extracted successfully!"
                    req=ghd.GetHtmlData(url)
                    if req[0]==0:
                        #print "html data got successfully!"
                        outputFile=outputPath+ "\\" + FNG.Generate(url) 
                        #print outputFile
                        sdif.Save(outputFile,req[1])
                        print url,":Html data is successfully saved!"
                    elif req[0] == 1:
                        outputFile=errorPath+"\\"+FNG.Generate(url)
                        sdif.Save(outputFile,"Failed to reach the server \r\nThe reason:"+req[1])
                        print url,"Failed to reach the server \r\nThe reason:",req[1]
                    elif req[0] == 2:
                        outputFile=errorPath+"\\"+FNG.Generate(url)
                        sdif.Save(outputFile,"The server couldn't fulfill the request \r\nError code:"+req[1]+" \r\nReturn content:"+req[2])
                        print url,"The server couldn't fulfill the request \r\nError code:",req[1]," \r\nReturn content:",req[2]
                    elif req[0] == 3:
                        outputFile=errorPath+"\\"+FNG.Generate(url)
                        sdif.Save(outputFile,req[1])
                        print url,req[1]
                    else:
                        outputFile=errorPath+"\\"+FNG.Generate(url)
                        sdif.Save(outputFile,"Unknown error")
                        print url,"Unknown error"
            fo.close()
if __name__ == '__main__':
    main()
                
