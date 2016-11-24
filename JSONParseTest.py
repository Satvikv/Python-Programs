import urllib.request
import json
class JSONParser:

	
	

	def __init__(self):
		self.fullJSONString=''
		
	def parseJSONString(self,urlString,location):
		total_sum=0
		try:
			values={'sensor':'false','address':location}
			completeURL=urlString+'?'+urllib.parse.urlencode(values)
			localfile, headers= urllib.request.urlretrieve(completeURL)
			self.fullJSONString=open(localfile).read()
			print(self.fullJSONString)
			
			jsonTree=json.load(open(localfile))
			print(jsonTree.keys())
			if jsonTree['status']!='OK' or 'status' not in jsonTree: return "No Place ID"
			for elem in jsonTree['results']:
				return elem['place_id']
		except urllib.error.URLError as e:
		    print ("Exception occured",str(e))
			
while True:		
	loc=input('Enter a location: ');
	if len(loc) < 1: break
	print ("Place id",JSONParser().parseJSONString('http://python-data.dr-chuck.net/geojson',loc))