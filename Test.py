s='hello'
t='hello'

stuff=dict()
print (stuff.get('candy',-1))
quit()

fh=open('romeo.txt','r')
for line in fh:
   if line.startswith('From:'):
       print (line)
quit()
	   
	   	   
for letter in 'banana':
 print (letter)
quit()
tuple={('a',1),('a',1),('c',3),('d',4),('e',5)}
newSet=set(tuple)

if s is 'hello':
   print (id(s),id(t))
   print (newSet)
else:
   print (tuple)

 

hrs = input("Enter Hours:")
h = float(hrs)
rate = input("Enter Rate per hour:")
r=float(rate)
pay=h*r
if h<=40:
  print (pay)
else:
  extra=int(h)-40
  extraPay=float(extra)*r*1.5
  totalPay=(h-extra)+extraPay
  print ((h*r))
  
 
