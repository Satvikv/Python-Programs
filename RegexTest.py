import re

fileName="SampleRegexData.txt"
fileHandler=open(fileName,'r')
numlist=list()
sumoffile=0
for line in fileHandler:
  line=line.rstrip()

  if len(numlist)< 1:
     numlist=re.findall('[0-9]+',line)
  else:
      numlist.extend(re.findall('[0-9]+',line))

print (numlist)
if len(numlist)< 1:
   print ("there are no numbers in the file")
else:
   for num in numlist:
      sumoffile+=int(num)
   print (sumoffile)
