#!/usr/bin/env python

import requests
try:
	from BeautifulSoup import BeautifulSoup
except ImportError:
	from bs4 import BeautifulSoup
from fake_useragent import UserAgent
ua = UserAgent()

headers = {'User-Agent': ua.chrome}

url_list = []

def get_bool(prompt):
    while True:
        try:
           return {"yes":True,"no":False}[input(prompt).lower()]
        except KeyError:
           print ("Invalid input please enter True or False!")

print (get_bool("Do you have a file to parse? (Please enter yes or no) "))

if get_bool == True:

    with open(input("Please enter the name of the file containing your links\n")) as file:
        for line in file:
            line = line.strip()
        url_list.append(line)

else:

    website_name = input("Please enter the website name ")
    website = requests.get(website_name, headers=headers)
    html = website.text
    soup = BeautifulSoup(html, "html.parser")
	
    for a in soup.find_all('a'):
        if a['href'].startswith( '/' ) or a['href'].startswith( '#' ):
            continue;
        elif a['href'] == '':
            continue;
        elif "linkedin" in a['href'] or "google" in a['href']:
            continue;
        elif "youtube" in a['href'] or "tel:" in a['href']:
            continue;
        elif "twitter" in a['href']:
            continue;
        url_list.append(a['href'])

print("\nThe total number of processed links is: ", end="")
print(url_list, '\n')

the_pattern = input("What's the search pattern?\n")
the_file = input("Which file should the results be written to?\n")
print("\n")

log = open(the_file, 'a')

for i in url_list:
    content = requests.get(i, headers=headers).text
    if the_pattern in content:
        search_pattern = print(the_pattern + " found at " + i, file = log)
    else:
    	print("Status: Not found")

log.close()