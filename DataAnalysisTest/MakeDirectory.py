# -*- coding: UTF-8 -*-

import os

def mkdir(path):
    path=path.strip()
    path=path.strip()
    path=path.rstrip("\\")
 
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists=os.path.exists(path)
 
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path) 
 
        print "Create "+path+' successfully!'
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print path+' has already existed!'
        return False
mkpath="d:\\qttc\\web\\"
mkdir(mkpath)
