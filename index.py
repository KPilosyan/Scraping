import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import os
import re
import unidecode

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
            sauce = urllib.request.urlopen(urls[0]).read()
            soup = BeautifulSoup(sauce, "html.parser")
            count = 1
            while soup.find(text ="next"):
                tag = soup.find(text = "next").parent 
                next_url = first_url[:-10] + str(tag["href"])
                urls.append(next_url)
                sauce = urllib.request.urlopen(urls[count]).read()
                soup = BeautifulSoup(sauce, "html.parser")
                count += 1

    return urls

def downloadTitles(url):
    sauce = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(sauce, "html.parser")

    titles_tag = soup.find_all("img")
    titles = []
    for i in titles_tag:
        titles.append(i["alt"])
    
    return titles

def downloadPrices(url):
    sauce = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(sauce, "html.parser")

    prices_tag = soup.find_all("p")
    prices = []
    for i in prices_tag:
        if i.get("class") == ["price_color"]:
            prices.append(i.get_text())

    return prices

def deleteRepSubString(string, rep):
    if rep not in string:
        return string
    while rep in string:
        string = string.replace(rep, "")
    return string

def createFolder(path, folderName):
    if os.path.isdir(folderName)==True:
        pass
    else:
        os.mkdir(os.path.join(path,folderName))

# def resolveSpecialCharacters(s):
#     # punctuation = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
#     # return s.rstrip(punctuation)

def resolveSpecialCharacters(string):
    for i in string:
        if not i.isalnum():
            string = string.replace(i, " ")

    return string

def downloadImagesToFolder(url, category):
    
    sauce = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(sauce, "html.parser")

    imgs = soup.find_all("img")
    # imageURLs = []
    titles = downloadTitles(url)
    prices = downloadPrices(url)
    path = "C:/Users/User/Desktop/Scraping/"
    count = 0
    for i in imgs:
        createFolder(path, category)
        imageURL = main_url + deleteRepSubString(i["src"], "../")
        titles[count] = resolveSpecialCharacters(titles[count])
        urllib.request.urlretrieve(imageURL, category + "/" + titles[count] + " " + str(prices[count]) + ".jpg")
                
        count += 1
    
def main():

    for i in getSideCategoryNames(main_url):
        # folder = createFolder(i)
        url = getCategoryPagesUrls(i)
        for n in url:
            downloadImagesToFolder(n,i)
            # count = 0
            # for k in downloadImages(n):
            # urllib.request.urlretrieve(k, i + "/" + str(titles[count]) + "/n" + str(prices[count]))
            # count += 1

        # time.sleep(1)

main()
