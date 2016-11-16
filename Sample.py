import re
print ("Hi, this is satvik")

str='X-DSPAM-Confidence: 0.9907'
list=re.findall('^X-DSPAM-Confidence:\s+([0-9.]*)',str)
print (list)

import re
print (sum( [ int(each) for each in re.findall('[0-9]+',open('SampleRegexData.txt','r').read()) ] ))
