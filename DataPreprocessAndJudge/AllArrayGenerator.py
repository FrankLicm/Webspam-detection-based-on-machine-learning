# -*- coding: UTF-8 -*-

import os,sys
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
import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn import svm
from sklearn.externals import joblib
import csv
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import MultinomialNB
import re

#主要功能:
#1.处理Html中Head标签，生成其文本内容的特征向量
#2.切分Html中Body标签为块，生成块的特征向量
#详细流程:
#1.分离Html中Head标签，为每一个网址建立一个文件夹将生成的内容特征向量存入Head.txt中
#2.切分Html中Body标签为块，将块信息按网址分文件夹存入*.txt，其中*为非0自然数，即块号
#3.以网址中的块为单位从2中读入块信息，分别生成标签、属性键、属性值、文本内容的特征向量
#4.将3中生成的每个一维特征向量补0对齐，并合并成一个多维特征向量
#5.将4中生成的特征向量存入一个的CSV文件中
def main(HtmlDataPath,BlockDataPath,AllArrayGeneratePath,ORValueFilePath,WordDictFilePath,KeyEnumFilePath,AttributesDirectoryPath,isSpam,ArrayDataCSVFilePath):
    #HtmlFiles = os.listdir(HtmlDataPath)
    #for f in HtmlFiles:
        #fo = open(HtmlDataPath + "\\" + f, "r")
        #html = fo.read()
        #fo.close()
        #path = AllArrayGeneratePath+"\\"+f
        #isExists=os.path.exists(path)
        # 判断结果
        #if not isExists:
            # 如果不存在则创建目录
            # 创建目录操作函数
            #os.makedirs(path)
        #fo = open(path+"\\"+"Head.txt","w")
        #Headarray = HAG.Generate(html)
        #print str(Headarray)
        #fo.write(str(Headarray))
        #fo.close()
    #HBS.Separate(HtmlDataPath,BlockDataPath)
    x=[]
    y=[]
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
    wordlist =[]
    fo=open(WordDictFilePath,"r")
    while 1:
        line = fo.readline()
        if not line:
            break
        wordlist.append(line.split(" ")[0].decode("utf8"))
    fo.close()
    BlockDataPaths = os.listdir(BlockDataPath)
    i=0
    for path in BlockDataPaths:
        i+=1
        print i
        paths = os.listdir(BlockDataPath+"\\"+path)
        for pa in paths:          
            Allarray=[]
            Allarray.append(isSpam)
            fo= open(BlockDataPath+"\\"+path+"\\"+pa,"r")
            text=""
            tagarray=[]
            attrarray = []
            while 1:
                line = fo.readline()
                if not line:
                    break;
                if "tag:" in line:
                    pass
                    tagarray = TAG.Generate(line.split(":")[1].split("-body")[0])
                elif "elem:" in line:
                    #print line.split("elem:")[1]
                    text = text+line.split("elem:")[1]
                elif "attrs:" in line:
                    attrsarray,text = AAG.Generate(str(line.split("attrs:")[1]),text,worddict,wordlist,KeyList,AllkeyValueDict)
                    #print attrsarray[0]
                    attrarray = attrsarray
                    #Allarray.extend(attrsarray)
                    #print "attrsarray[0]len:",len(attrsarray[0])
                    if len(attrsarray)!=3949:
                        print "attrsarraylen:",len(attrsarray)
            textReg = "[^\s]"
            if text!="" and re.match(textReg,text,re.I):
                 Allarray.extend(tagarray)
                 Allarray.extend(attrarray)
                 #orvalue,unexist = TAG1.ComputeORValue(worddict,text)
                 #if orvalue!=-99999:
                 #for word in unexist:
                 #    print word
                 #    fo = open(ORValueFilePath,"ab+")
                 #    fo.write(word+" "+1)
            else:
                continue                    
            if len(Allarray) != 4072:
                print path,pa
                print "len:",len(Allarray)
            #print "nomArray:",nomArray      
            fo.close()
            with open(ArrayDataCSVFilePath,"ab+") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(Allarray)
                
def iter_minibatches(data_stream, minibatch_size=1000):
    '''
    迭代器
    给定文件流（比如一个大文件），每次输出minibatch_size行，默认选择1k行
    将输出转化成numpy输出，返回X, y
    '''
    X = []
    y = []
    cur_line_num = 0
    csvfile = file(data_stream, 'rb')
    reader = csv.reader(csvfile)
    for line in reader:
        y.append(float(line[0]))
        X.append(map(eval,line[1:]))  # 这里要将数据转化成float类型
        
        cur_line_num += 1
        if cur_line_num >= minibatch_size:
            X, y = np.array(X), np.array(y)  # 将数据转成numpy的array类型并返回
            yield X, y
            X, y = [], []
            cur_line_num = 0
    csvfile.close()

if __name__ == '__main__':
    #HtmlDataPath="E:\\UnderGraduateDesign\\ExperimentSample\\HtmlSource";
    #BlockDataPath="E:\\UnderGraduateDesign\\ExperimentSample\\BlockSeparator\\spam";
    #BlockDataPath2 = "E:\\UnderGraduateDesign\\ExperimentSample\\BlockSeparator\\nonspam"
    #AllArrayGeneratePath="E:\\UnderGraduateDesign\\ExperimentSample\\BlockArray1\\Spam";
    #ORValueFilePath = "E:\\UnderGraduateDesign\\ExperimentSample\\AssetValue\\TextAB+1ORValue.txt"
    #WordDictFilePath = "E:\\UnderGraduateDesign\\ExperimentSample\\Dict\\ORSpamDict.txt"
    #KeyEnumFilePath = "E:\UnderGraduateDesign\ExperimentSample\\Key.txt"
    #AttributesDirectoryPath = "E:\\UnderGraduateDesign\\ExperimentSample\\Attributes"
    ArrayDataCSVFilePath = "E:\\UnderGraduateDesign\\ExperimentSample\\ArrayData\\ArrayDataWithoutTextWithText.csv"
    ModelFilePath = "E:\\UnderGraduateDesign\\ExperimentSample\\model\\nb_train_model_without_text_with_text.m"
    #main(HtmlDataPath,BlockDataPath,AllArrayGeneratePath,ORValueFilePath,WordDictFilePath,KeyEnumFilePath,AttributesDirectoryPath,1,ArrayDataCSVFilePath)
    #main(HtmlDataPath,BlockDataPath2,AllArrayGeneratePath,ORValueFilePath,WordDictFilePath,KeyEnumFilePath,AttributesDirectoryPath,0,ArrayDataCSVFilePath)
    #x.extend(m)
    #y.extend(n)
    #print "x:",len(x)
    #print "y:",len(y)
    #clf = svm.SVC()
    #clf.fit(x, y)
    #get support vectors
    #print "support vectors:", clf.support_vectors_
    #get indices of support vectors
    #print "of support vectors:", clf.support_
    #get number of support vectors for each class
    #print "number of support vectors for each class:", clf.n_support_
    #joblib.dump(clf, "E:\\UnderGraduateDesign\\ExperimentSample\\model\\svm_train_model.m")
    # 生成测试文件
    #minibatch_test_iterators = iter_minibatches(ArrayDataCSVFilePath, minibatch_size=5000)
    #X_test, y_test = minibatch_test_iterators.next()  # 得到一份测试文件
    nb_clf = MultinomialNB()  # MultinomialNB的参数设置可以参考sklearn官网
    minibatch_train_iterators = iter_minibatches(ArrayDataCSVFilePath, minibatch_size=5000)
    for i, (X_train, y_train) in enumerate(minibatch_train_iterators):
        # 使用 partial_fit ，并在第一次调用 partial_fit 的时候指定 classes
        nb_clf.partial_fit(X_train, y_train, classes=np.array([0, 1]))
        print("{} time".format(i))  # 当前次数
        #print("{} score".format(nb_clf.score(X_test, y_test)))  # 在测试集上看效果
    joblib.dump(nb_clf, ModelFilePath)
    
