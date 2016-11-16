import urllib.request
from bs4 import BeautifulSoup

urlstring='http://www.larson-tech.com/PSU'
htmlstring=urllib.request.urlopen(urlstring).read()
#print (htmlstring)
soupcollection=BeautifulSoup(htmlstring)
print (soupcollection)
"""
tags=soupcollection('a')
print (tags)
for tag in tags:
  print (tag.get('href'))
"""
