# -*- coding: UTF-8 -*-

from bs4 import BeautifulSoup
import re

def GetHtmlTag(html,content):
    soup = BeautifulSoup(html,"lxml")
    txt = re.compile(content)
    for elem in soup(text = txt):
        for parent in elem.parents:
            print parent.name
    
if __name__ == '__main__':
    html = """<jj><h2>this is cool #12345678901</h2></jj><h2>this is nothing</h2><h1>foo #126666678901</h1><h2>this is interesting #126666678901</h2><h2>this is blah #124445678901</h2>"""
    content = 'cool'
    GetHtmlTag(html,content)
