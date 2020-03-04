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

def downloadImages(url):
    sauce = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(sauce, "html.parser")

    imgs = soup.find_all("img")
    imageURLs = []
    for i in imgs:
        imageURLs.append(main_url + i["src"])
    
    return imageURLs

# def createFolder(name):
#     path = 'C:/Users/User/Desktop/Scraping/' + name
#     return os.mkdir(path)

# def downloadCategoryPage(url):
#     # sauce = urllib.request.urlopen(url).read()
#     # soup = BeautifulSoup(sauce, "html.parser")

#     for i in getSideCategoryNames(main_url):
#         # folder = createFolder(i)
#         url = getCategoryPagesUrls(i)
#         titles = downloadTitles(url)
#         prices = downloadPrices(url)
#         count = 0
#         for k in downloadImages(url):
#             urllib.request.urlretrieve(k, i + "/" + str(titles[count]) + "/n" + str(prices[count]))

# root_path = 'C:/Users/User/Desktop/Scraping'
# count = 2
# for folder in ategories:
#     os.mkdir(os.path.join(root_path,str(folder)))    #creates folder for each item in list 
#     path = root_path + "/" + str(folder)
#     url = main_url + "catalogue/category/books/" + str(folder).lower() + "_" + str(count) + "/index.html"
#     sauce = urllib.request.urlopen(url).read()
#     soup = BeautifulSoup(sauce, "html.parser")
#     #print(url)

    

    

#     imgs = soup.find_all("img")
#     count_images = 0

#     for i in imgs:
#         print(main_url + i["src"].strip("../"), str(folder) + "/" + str(titles[count_images]) + str(prices[count_images]) + ".jpg")
#         download = urllib.request.urlretrieve(main_url + i["src"].strip("../"), str(folder) + "/" + str(titles[count_images]) + str(prices[count_images]) + ".jpg")
#         count_images += 1 

#     while soup.find(text ="next"):
#         count_images = 0
#         next_tag = soup.find(text ="next").parent
#         next_page_url = url.replace("index.html",next_tag["href"])
#         sauce = urllib.request.urlopen(next_page_url).read()
#         soup = BeautifulSoup(sauce, "html.parser")
#         imgs = soup.find_all("img")
        
#         for i in imgs:
#             download 
#             count_images += 1
            
        
#     count += 1

    

def main():

    # sauce = urllib.request.urlopen(url).read()
    # soup = BeautifulSoup(sauce, "html.parser")

    for i in getSideCategoryNames(main_url):
        # folder = createFolder(i)
        url = getCategoryPagesUrls(i)
        titles = downloadTitles(url)
        prices = downloadPrices(url)
        count = 0
        for k in downloadImages(url):
            urllib.request.urlretrieve(k, i + "/" + str(titles[count]) + "/n" + str(prices[count]))
            count += 1

        time.sleep(1)

main()