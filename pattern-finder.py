#!/usr/bin/env python

import requests
import re
try:
	from BeautifulSoup import BeautifulSoup
except ImportError:
	from bs4 import BeautifulSoup
from fake_useragent import UserAgent
ua = UserAgent()

headers = {'User-Agent': ua.google}

url_list = []

has_file = input("Do you have a file to parse? (Please enter yes or no) ")

if has_file.lower() == 'yes' or has_file.lower() == 'y':

    with open(input("Please enter the name of the file containing your links: ")) as file:
        for line in file:
            line = line.rstrip('\n')
            url_list.append(line)

elif has_file.lower() == 'no' or has_file.lower() == 'n':

    website_name = input("Please enter the website name: ")
    website = requests.get(website_name, headers=headers)
    html = website.text
    soup = BeautifulSoup(html, "html.parser")
	
    for a in soup.find_all('a'):
        
        try:

            if a['href'].startswith( '/' ) or a['href'].startswith( '#' ):
                continue;
            elif re.search('(?<=\w).www\w+', a['href']):
                continue;
            elif a['href'] == '':
                continue;
            elif "linkedin" in a['href'] or "google" in a['href']:
                continue;
            elif "youtube" in a['href'] or "tel:" in a['href']:
                continue;
            elif "twitter" in a['href'] or "mailto:" in a['href']:
                continue;
            elif "javascript(void)" in a['href']:
                continue;
            
            url_list.append(a['href'])

        except KeyError:
            pass

else:
    print("Wrong value")
    exit(1)

print("\nThe total number of processed links is: ", end="")
print(len(url_list))

the_pattern = input("What's the search pattern?: ")
the_file = input("Which file should the results be written to?: ")
print("\n")

log = open(the_file, 'a')

for i in url_list:
    content = requests.get(i, headers=headers).text
    if the_pattern.lower() in content.lower():
        print(the_pattern + " found at " + i, file = log)
    else:
    	print("Status: Not found ")

log.close()
