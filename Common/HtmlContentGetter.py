from bs4 import BeautifulSoup
import re

def GetText(html):
    soup=BeautifulSoup(html, "lxml")
    for script in soup.findAll('script'):
        script.extract()
    for style in soup.findAll('style'):
        style.extract()
    soup.prettify()
    reg1 = re.compile("<[^>]*>")
    string = reg1.sub('',soup.prettify())
    return re.sub('\s','',string)

def GetInNonEnglish(html):
    soup=BeautifulSoup(html, "lxml")
    return re.sub('[ -~]|\s','',soup.prettify())
if __name__ == '__main__':
    fo = open("TestHtml.html", "r")
    html = fo.read()
    print GetInNonEnglish(html)
