# -*- coding: UTF-8 -*-


def Save(filePath,content):
    content = str(content)
    fo = open(filePath.decode('utf-8'),"wb")
    #print "saving...."
    fo.write(content)
    #print "saved."
    fo.close()
if __name__ == '__main__':
    Save("E:\UnderGraduateDesign\Tests\TestSave新化蛇.txt","Save success世纪东方可理解!")
