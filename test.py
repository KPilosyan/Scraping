import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import os

main_url = 'http://books.toscrape.com/'

def getSideCategoryNames(url):
    categories = []
    sauce = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(sauce, "html.parser")
    categories_tag = soup.find(class_ = "side_categories").stripped_strings

    for i in categories_tag:
        categories.append(i)
    
    categories.remove("Books")                      # Removing 'Books' category which includes all books 
    return categories

def getCategoryPagesUrls(categoryName):
    sauce = urllib.request.urlopen(main_url).read()
    soup = BeautifulSoup(sauce, "html.parser")
    urls = []
    for i in soup.find_all("a"):
        if i.get_text(strip=True) == categoryName:
            tag = i
            first_url = main_url + str(tag["href"])
            urls.append(first_url)
            print(urls[0])
            sauce = urllib.request.urlopen(urls[0]).read()
            soup = BeautifulSoup(sauce, "html.parser")

            count = 1
            while soup.find(text ="next"):
                tag = soup.find(text = "next").parent 
                print("Ste em")
                next_url = first_url[:-10] + str(tag["href"])
                print(next_url)
                urls.append(next_url)
                sauce = urllib.request.urlopen(urls[count]).read()
                soup = BeautifulSoup(sauce, "html.parser")
                count += 1

    return urls

for i in getSideCategoryNames(main_url):
    getCategoryPagesUrls(i)
