# -*- coding: UTF-8 -*-

def ReadConf():
    fo = open("InputPath.conf", "r")
    inputPath = fo.read()
    fo1 = open("OutputPath.conf","r")
    outputPath = fo1.read()
    fo2 = open("ErrorPath.conf","r")
    errorPath = fo2.read()
    return inputPath,outputPath,errorPath

if __name__ == '__main__':
    print ReadConf()

    
    
