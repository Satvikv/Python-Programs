import urllib
from bs4 import *

urlString=input('Enter url - ')
readHTML=urllib.request.urlopen(urlString).read()
soupcollection=BeautifulSoup(readHTML,"html5lib")
tags=soupcollection('span')
sum=0
for tag in tags:
    sum+=int(tag.contents[0])
print (sum)
