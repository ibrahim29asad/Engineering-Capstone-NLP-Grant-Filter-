import requests
import os
from bs4 import BeautifulSoup, SoupStrainer

url = "https://www.endocrinology.org"
sub_urls = set()

check_list = ['grant', 'proposal', 'award', 'fellowship', 'opportunities', 'opportunity', 'partnership', 'prize', 'medal', 'fund', 'scholarship']

#Set user agent
#Allows access to websites prevent web-scraping
headers = {'User-Agent': 
		   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}

try:
	res = requests.get(url, headers=headers)
	
	if res.status_code == 200:
		for link in BeautifulSoup(res.text, parse_only=SoupStrainer('a'), features="html.parser"):
			if link.has_attr('href'):
				actual_url = link['href']
				
				if any(x in actual_url for x in check_list):
					sub_urls.add(url + actual_url)
			
	else:
		try:
			fo_list_path = os.path.join(os.getcwd() + "\FO_List.txt")
			
			fo_list_file = open(fo_list_path, "a", encoding="utf-8")
			fo_list_write = url + " Did not get status code 200. \n"
			fo_list_file.write(fo_list_write)
			fo_list_file.close()
			
		except Exception as error:
			print("Error encountered while creating and writing to file:",error)
		
except Exception as error:
	try:
		fo_list_path = os.path.join(os.getcwd() + "\FO_List.txt")
		
		fo_list_file = open(fo_list_path, "a", encoding="utf-8")
		fo_list_write = url + " Did not get status code 200. \n"
		fo_list_file.write(fo_list_write)
		fo_list_file.close()
		
	except Exception as error:
		print("Error encountered while creating and writing to file:",error)
		
print(sub_urls)