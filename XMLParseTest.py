import urllib.request
import xml.etree.ElementTree as ET
class XMLParser:

	fullXMLString=str()
	

	def __init__(self):
		self.fullXMLString=''
		
	def parseXMLString(self,url):
		total_sum=0
		try:
			self.fullXMLString= urllib.request.urlopen(url).read()
			xmlTree=ET.fromstring(self.fullXMLString)
			for elem in xmlTree.findall('.//count'):
				total_sum+=int(elem.text)
			return total_sum
		except urllib.error.URLError as e:
		    print ("Exception occured",str(e))
			
		

print ("The count is",XMLParser().parseXMLString('http://python-data.dr-chuck.net/comments_321992.xml'))


