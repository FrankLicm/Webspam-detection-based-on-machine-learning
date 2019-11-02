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
import TextArrayGenerator as TAG
import numpy as np
import pandas as pd

def init(KeyEnumFilePath, AttributesDirectoryPath):
    KeyList =[]
    fo = open(KeyEnumFilePath,"r")
    while 1:
        line = fo.readline()
        if not line:
            break
        KeyList.append(line.split("\n")[   0])
    fo.close()
    AllkeyValueDict={}
    for key in KeyList:
        if key == "class" or key == "href" or key == "src" or key == "id" or key == "alog-custom" or key =='#"':
                continue
        fo = open(AttributesDirectoryPath+"\\"+key,"ab+")
        ValueList = []
        while 1:
            line = fo.readline()
            if not line:
                break
            ValueList.append(line.split("\n")[0])
        fo.close()
        AllkeyValueDict[key] = ValueList
    return KeyList,AllkeyValueDict

def Generate(attributes,text, worddict,KeyList,AllkeyValueDict):
    AllListArray =[] 
    KeyArray = [0 for n in range(len(KeyList))]
    AttrDict = eval(attributes)
    #print AttrDict
    KeyValueDict={}
    #生成键的特征向量
    for key in AttrDict:
        #print key,":",AttrDict[key]
        if key in KeyList:
            KeyArray[KeyList.index(key)] = 1
        else:
            continue
            #print key
            #fo = open(KeyEnumFilePath,"ab+")
            #fo.write(key+"\r\n")
            #fo.close()
            #KeyList.append(key)
            #print key
            #KeyArray.append(0)
            #KeyArray[KeyList.index(key)] = 1
    #print KeyArray
    AllListArray.extend(KeyArray)
    #生成值的特征向量
    for key in AttrDict:
        #值共有下面5种类型
        #1.数值型，一般后面有单位px等,如height
        #数值类型的特征是只有数字或者数字后出现px,em,ex,%,in,cm,mm,pt,pc等单位的值
        #我们不选择数值型属性的值作为特征，因为数值属性的值灵活度高，每一个html基本都有其定制化的大小和长度，特征不明显
        #所以我们只是在之前生成键特征向量的时候标识一下有此键即可
        #2.健值对类型，如style，style属性的值是CSS的健值对代码
        #健值对类型的特征是";"将键值与键值之间隔开，":"将键与值之间隔开。
        #我们考虑键值对类型的值作为特征，属性中的键值也有键和值之分，其中值的类型大体有数值类型，函数类型，内部值类型三种类型，数值类型我们一样不考虑值只考虑键，
        #函数类型的值和内部值类型我们直接和键一起作为一个特征项，因为其内容相对固定，具有明显特征
        #3.链接型，如href
        #链接型的特征一般是有http或者/组成的路径组成。我们不能把具体的链接当做特征项，因为链接本身不具有明显特征，所以我们只存入键不考虑链接型的值。
        #但是后期可以考虑将可疑链接输出
        #4.自定义字符型，如title
        #自定义字符类型按照自然语言处理的方法给分词编号有1无为0
        #5.HTML内部值类型，如target里有_blank,_parent,_self,_top等可供选择的值，再比如font-family中有宋体等值
        #内部值类型由于是有限个，给其编号后有为1无为0存入
        #键和值应该一一对应，所以我们应该为每一个键生成一个一维特征向量表示出现在该键的属性，如果在这个块中没有这个键那么是0
        if key == "class" or key == "href" or key == "src" or key == "id" or key == "alog-custom" or key =='#"':
            continue
        NumberReg = "^[0-9]+(?:px|em|ex|%|in|cm|mm|pt|pc)?$"
        KeyValueReg ="[^\s]+: *[^;]+;?"
        LinkReg ="[a-zA-z]+://[^\s]*"
        ChineseReg=u'[\u4E00-\u9FA5]+'
        try:
            if re.match(NumberReg,AttrDict[key],re.I):
                #print "1:",AttrDict[key]
                pass
            elif re.match(KeyValueReg,AttrDict[key],re.I):
                ValueList=AllkeyValueDict[key]
                ValueArray = [0 for n in range(len(ValueList))]
                for string in re.finditer(KeyValueReg,AttrDict[key],re.I):
                    #print "1:",string.group()
                    keyvalue = string.group().split(";")[0].replace(" ","")
                    #print keyvalue
                    value = keyvalue.split(":")[1]
                    if re.match(NumberReg,value,re.I)  or "url" in value:
                        key1=keyvalue.split(":")[0] 
                        if key1 not in ValueList:
                            continue
                            #ValueList.append(key1)
                            #fo = open(AttributesDirectoryPath+"\\"+key,"ab+")
                            #fo.write(key1+"\n")
                            #fo.close()
                            #ValueArray.append(0)
                        ValueArray[ValueList.index(key1)] = 1
                    else:
                        if keyvalue not in ValueList:
                            continue
                            #ValueList.append(keyvalue)
                            #fo = open(AttributesDirectoryPath+"\\"+key,"ab+")
                            #fo.write(keyvalue+"\n")
                            #fo.close()
                            #ValueArray.append(0)
                        ValueArray[ValueList.index(keyvalue)] = 1
                #print key,":",ValueArray
                KeyValueDict[key] = ValueArray
            elif re.match(LinkReg,AttrDict[key],re.I):
                #print "3:",AttrDict[key]
                pass
            elif re.match(ChineseReg,AttrDict[key],re.I):
                #本自定义字符只考虑含有中文的词
                #print "4:",AttrDict[key]
                text=text + AttrDict[key]
            else:
                ValueList=AllkeyValueDict[key]
                ValueArray = [0 for n in range(len(ValueList))]
                if AttrDict[key] not in ValueList:
                    continue
                    #ValueList.append(AttrDict[key])
                    #print key,AttrDict[key]
                    #fo = open(AttributesDirectoryPath+"\\"+key,"ab+")
                    #fo.write(AttrDict[key]+"\n")
                    #fo.close()
                    #ValueArray.append(0)
                ValueArray[ValueList.index(AttrDict[key])] = 1
                #print key,":",ValueArray  
                #print "5:",AttrDict[key]
                #print ValueList
                KeyValueDict[key] = ValueArray
        except TypeError:
            pass
                #ValueList=AllkeyValueDict[key]
                #ValueArray = [0 for n in range(len(ValueList))]
                #if AttrDict[key] not in ValueList:
                #    ValueList.append(str(AttrDict[key]))
                #    fo = open(AttributesDirectoryPath+"\\"+key,"ab+")
                #    fo.write(str(AttrDict[key])+"\n")
                #    fo.close()
                #    ValueArray.append(0)
                #ValueArray[ValueList.index(str(AttrDict[key]))] = 1
                #print key,":",ValueArray  
                #print "5:",AttrDict[key]
                #print ValueList
                #KeyValueDict[key] = ValueArray
        except IOError:
            pass
        except IndexError:
            pass
        except NameError:
            pass
        except KeyError:
            pass
        except ValueError:
            pass
    for key in KeyList:
        if key == "class" or key == "href" or key == "src" or key == "id" or key == "alog-custom" or key =='#"':
                continue
        if key in KeyValueDict:
            AllListArray.extend(KeyValueDict[key])
        else:
            ValueArray = [0 for n in range(len(AllkeyValueDict[key]))]
            AllListArray.extend(ValueArray)
    return AllListArray, text

if __name__ == '__main__':
    ORValueFilePath = "E:\\UnderGraduateDesign\\ExperimentSample\\AssetValue\\TextAB+1ORValue.txt"
    WordDictFilePath = "E:\\UnderGraduateDesign\\ExperimentSample\\Dict\\ORSpamDict.txt"
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
    #print Generate("{u'height':u'20px',u'style': u'line-height: 20px; font-family: \u5b8b\u4f53; color: rgb(0,0,0); text-decoration: none', u'href': u'http://www.reahat.com/', u'target': u'_blank', u'title': u'\u8db3\u7403\u7ade\u5f69\u7f51'}",[])
    #alllist = Generate("{'style': u'font-size:12px; width:140px; height:22px; border:#D2D2D2 solid 1px;background:url(images/inputbg.gif) 4px 4px no-repeat; background-color:#ffffff;  margin-right:4px; padding-left:24px; color:#858585; padding-top:4px', u'name': u'kw', u'value': u'\u7ad9\u5185\u5168\u6587\u641c\u7d22', u'onclick': u\"this.value=''\", u'type': u'text', u'id': u'kw'}","",worddict,wordlist)
    alllist = Generate("{u'name': u'kw', u'value': u'\u7ad9\u5185\u5168\u6587\u641c\u7d22', u'onclick': u\"this.value=''\", u'type': u'text', u'id': u'kw'}","",worddict,wordlist)
    attr = alllist[0]
    #print len(attr)

    
