import urllib
from bs4 import *

urlString=input('Enter url - ')
count=input('Enter count- ')
position=input('Enter position- ')

c=int(count)
pos=int(position)-1
while c>=0:
    print (urlString)
    readNewHTML=urllib.request.urlopen(urlString).read()
    newSoup=BeautifulSoup(readNewHTML,"html5lib")
    newTags=newSoup('a')
    urlString=newTags[pos].get('href')
    c-=1
