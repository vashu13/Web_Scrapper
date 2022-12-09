#!/usr/bin/python3

#IMPORT_SECTION

import requests
from bs4 import BeautifulSoup
import urllib
import re

#INPUT_SECTION

ip=input("Enter Web Address : ")

#EDIT_SECTION

pt=r"(\.\w{2,10}\/?$)"		#regex_pattern
p=re.compile(pt)		#regex_compile

if not ip.startswith("http"):
	ip="https://"+ip

if not re.search(p,ip):
	ip=ip+'.com'

print("\n")
print(ip)			#print link for double check

site_map=set()			#creating set to store extracted links without repeat for better file format

success=0			#to check the success for saving file


#SCRAPRE_SECTION

try:
	sc=urllib.request.urlopen(ip).getcode()		#checting if the links exists
except:
	sc=404
if sc==200:
	try:
		p=requests.get(ip)
		con=p.content

		soup=BeautifulSoup(con,'html.parser')

		anc=soup.find_all('a')
		for i in anc:
			if not i.get('href').startswith("http"):
				print(ip+"/"+i.get('href') if not ip.endswith('/') else ip+i.get('href'))
				site_map.add(ip+"/"+i.get('href') if not ip.endswith('/') else ip+i.get('href'))
			else:
				print(i.get('href'))
				site_map.add(i.get('href'))

	except AttributeError:			#when no data is extracted
		success=0
		print("\n\n")
		print("\033[1;31m"+"OOPS...SEEMS LIKE SOMETHING WENT WRONG")
		print("\033[1;31m"+"NO DATA COULD BE EXTRACTED")
		print("\n")
		print("\033[1;31m"+"POSSIBLE_REASON: SITE DOESN'T HAVE ANY LINKS")

else:
	success=0
	print("\n"+"\033[1;31m"+"COULD'T FIND THE GIVEN SITE, MAYBE SITE DOESN'T EXIST...")		#page doesn't exists
	print("\033[1;31m"+"TRY ANOTHER SITE")

for site in site_map.copy():				#further scraping extracted links
	try:
		sc=urllib.request.urlopen(ip).getcode()
	except:
		sc=404
	if sc==200:
		try:
			q=requests.get(site)
			con1=q.content
	
			soup1=BeautifulSoup(con1,'html.parser')
	
			anc1=soup1.find_all('a')
			for j in anc1:
				if not j.get('href').startswith("http"):
					print(site+"/"+j.get('href') if not site.endswith('/') else site+j.get('href'))
					site_map.add(site+"/"+j.get('href') if not site.endswith('/') else site+j.get('href'))
				else:
					print(j.get('href'))
					site_map.add(j.get('href'))
			success=1
		except AttributeError:
			continue
			
			
#DOCUMENTATION_SECTION

if success==1:
	print("\nDo you want to store it in a file ? ")
	while True:
		choice=input("\ny for yes and n for no:  ")
		if choice=="Y" or choice=="y":
			name=input("\nEnter name of your text file (dont't forget .txt): ")
			if name.endswith('.txt'):
				f=open(name,'a')
				for k in site_map:
					f.write(k+"\n")
				f.close()
				print("EXITING...\n")
				break
			else:
				name1=name+".txt"
				f=open(name1,'a')
				for k in site_map:
					f.write(k+"\n")
				f.close()
				print("EXITING...\n")
				break
		if choice=="N" or choice=="n":
			print("EXITING...\n")
			break
		else:
			print("\nInput not recognised.\nPlease choose from the given options...")

