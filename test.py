import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import os

main_url = 'http://books.toscrape.com'

def getSideCategoryNames(url):
    categories = []
    sauce = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(sauce, "html.parser")
    categories_tag = soup.find(class_ = "side_categories").strings

    for i in categories_tag:
        categories.append(i)
    
    categories = [s.strip() for s in categories]    # cleaning the
    categories = [i for i in categories if i]       # list 
    categories.remove("Books")                      # Removing 'Books' category which includes all books 
    return categories

def getCategoryPagesUrls(categoryName):
    sauce = urllib.request.urlopen(main_url).read()
    soup = BeautifulSoup(sauce, "html.parser")
    urls = []
    if soup.find(text = "next"):
        print("Yes")
        tag = soup.find(text = categoryName).parent 
        urls.append(tag["href"])
        sauce = urllib.request.urlopen(urls[0]).read()
        soup = BeautifulSoup(sauce, "html.parser")

        count = 1
        while soup.find(text ="next"):
            tag = soup.find(text = "next").parent 
            urls.append(tag["href"])
            sauce = urllib.request.urlopen(urls[count]).read()
            soup = BeautifulSoup(sauce, "html.parser")
            count += 1

    return urls

getCategoryPagesUrls(main_url)
