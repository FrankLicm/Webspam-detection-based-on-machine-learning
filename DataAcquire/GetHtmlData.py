# -*- coding: UTF-8 -*-
import urllib2
import socket
import SaveDataInFile as sdif
def GetHtmlData(url):
    req = urllib2.Request(url)
    try:
        page = urllib2.urlopen(req,data=None,timeout=3)
        return 0,page.read()     
    except urllib2.URLError,e:
        if hasattr(e,"reason"):
            print "Failed to reach the server"
            print "The reason:",str(e.reason)
            return 1, str(e.reason)
        elif hasattr(e,"code"):
            print "The server couldn't fulfill the request"
            print "Error code:",str(e.code)
            print "Return content:",str(e.read())
            return 2, str(e.code), str(e.read())
    except socket.timeout as e:
        print( 'socket.timeout:', str(e))
        return 3,str(e)
    except socket.error as e:
        print( 'socket.error:', str(e))
        return 3,str(e)
    except Exception,e:
        return 3, str(e)
if __name__ == '__main__':
    html = GetHtmlData("http://zhaosheng.heuet.edu.cn")
    print html
