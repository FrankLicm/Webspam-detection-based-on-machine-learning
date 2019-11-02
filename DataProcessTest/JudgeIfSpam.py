import os
import sys
stdi,stdo,stde=sys.stdin,sys.stdout,sys.stderr  
reload(sys)  
sys.setdefaultencoding( "utf-8" ) 
sys.stdin,sys.stdout,sys.stderr=stdi,stdo,stde

import TagTreeExtractor as tte

def main():
    SpamClassificationPath = "E:\UnderGraduateDesign\ExperimentSample\Clasification2\spam"
    UndefinedClassificationPath = "E:\UnderGraduateDesign\ExperimentSample\Clasification2\undefined"
    UndefinedTagTree = os.listdir(UndefinedClassificationPath)
    print "UndefinedTagTree:",UndefinedTagTree
    SpamClassifications = os.listdir(SpamClassificationPath)
    print "SpamClassifications:",SpamClassifications
    ActivityRecommendSpamTagTree  = os.listdir(SpamClassificationPath+"\\"+SpamClassifications[0])
    print "ActivityRecommendSpamTagTree:", ActivityRecommendSpamTagTree
    ChangeJsSpamTagTree  = os.listdir(SpamClassificationPath+"\\"+SpamClassifications[1])
    print "ChangJsSpamTagTree:", ChangeJsSpamTagTree
    CommentTagTree = os.listdir(SpamClassificationPath+"\\"+SpamClassifications[2])
    print "CommentTagTree:", CommentTagTree
    PASpamTagTree = os.listdir(SpamClassificationPath+"\\"+SpamClassifications[3])
    print "PASpamTagTree:", PASpamTagTree
    VisibleSpamTagTree = os.listdir(SpamClassificationPath+"\\"+SpamClassifications[4])
    print "VisibleSpamTagTree", VisibleSpamTagTree
    OutputSpamClassificationPath = "E:\UnderGraduateDesign\ExperimentSample\Clasification\spam"
    OutputUndefinedClassificationPath = "E:\UnderGraduateDesign\ExperimentSample\Clasification\undefined"
    
    HtmlDataPath = "E:\UnderGraduateDesign\ExperimentSample\HtmlSource"
    HtmlFiles = os.listdir(HtmlDataPath)
    for f in HtmlFiles:
       fo = open(HtmlDataPath + "/" + f, "r")
       html = fo.read()
       fo.close()
       tagList = tte.Extract(html)
       if len(list(set(tagList).intersection(set(UndefinedTagTree)))) > 0:
           foo = open(OutputUndefinedClassificationPath+"/"+f,"wb")
           foo.write(html)
           foo.close()
       if len(list(set(tagList).intersection(set(ActivityRecommendSpamTagTree)))) > 0:
           foo = open(OutputSpamClassificationPath+"/"+"activity_recommend/"+f,"wb")
           foo.write(html)
           foo.close()
       if len(list(set(tagList).intersection(set(ChangeJsSpamTagTree)))) > 0:
           foo = open(OutputSpamClassificationPath+"/"+"change_js/"+f,"wb")
           foo.write(html)
           foo.close()
       if len(list(set(tagList).intersection(set(CommentTagTree)))) > 0:
           foo = open(OutputSpamClassificationPath+"/"+"comment/"+f,"wb")
           foo.write(html)
           foo.close()
       if len(list(set(tagList).intersection(set(PASpamTagTree)))) > 0:
           foo = open(OutputSpamClassificationPath+"/"+"p_a/"+f,"wb")
           foo.write(html)
           foo.close()
       if len(list(set(tagList).intersection(set(VisibleSpamTagTree)))) > 0:
           foo = open(OutputSpamClassificationPath+"/"+"visible/"+f,"wb")
           foo.write(html)
           foo.close()
main()        
