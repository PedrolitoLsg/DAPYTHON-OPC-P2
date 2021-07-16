from bs4 import BeautifulSoup
from slugify import slugify
import requests
import re
import csv
import os

main_url = "https://books.toscrape.com/index.html"


def get_all_categories():
    req = requests.get(main_url)
    soup = BeautifulSoup(req.text, "html.parser")
    result_main_cat = []
    if req.ok:
        balise = (
            soup.find("div", {"class": "side_categories"})
            .find("ul")
            .find("li")
            .find("ul")
        )
        liste_elem = balise.find_all("a", href=True)
        for elem_a in liste_elem:
            result_main_cat.append(
            "https://books.toscrape.com/"+ elem_a["href"]
            )

    return result_main_cat


def get_all_categories_names():
    req = requests.get(main_url)
    soup = BeautifulSoup(req.text, "html.parser")
    result_cat = []
    if req.ok:
        balise = (
            soup.find("div", {"class": "side_categories"})
                .find("ul")
                .find("li")
                .find("ul")
        )
        liste_elem = balise.find_all("a", href=True)

        for elem_a in liste_elem:
            result_cat.append(
                elem_a.text.strip()
            )

    return result_cat

def get_main2_urls():
    main_url = get_all_categories()
    main2_urls = []
    for url in main_url:
        req = requests.get(url)
        soup = BeautifulSoup(req.text, 'html.parser')
        number_of_pages_for_mystery = []
        if req.ok:
            if soup.find("ul", {"class":"pager"}):
                number_of_pages_for_mystery = int(soup.find('li', {'class':'current'}).text.split(' ')[31])
                i = 1
                while i <= number_of_pages_for_mystery:
                    main2_urls.append(
                    str(url)[:-10] + "page-" + str(i) +".html"
                    )
                    i+= 1

            else:
                # means that there is only one page for mystery category number_of_pages_for_mystery = 1
                main2_urls.append(url)
        else: # the requests is not working
            print("no worky")
    return main2_urls

def get_all_books_urls_from_main2_urls():
    urls = get_main2_urls()
    books_urls = []
    for url in urls:
        req = requests.get(url)
        soup = BeautifulSoup(req.text, "html.parser")
        if req.ok:
            for bookurl in soup.find_all('h3'):
                url = bookurl.a.get('href').replace("../../../", "https://books.toscrape.com/catalogue/")
                books_urls.append(url)
        else:
            print("----request for a main url in get all books urls from mystery is NOT WORKING-----")
    return books_urls

def get_book_info_from_url():
    urls =get_all_books_urls_from_main2_urls()
    results = []
    print("looping through books_urls to retrieve all data")
    for url in urls:
        response = requests.get(url)

        if response.ok :
            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.find('img')['alt']
            product_page_url = url
            product_information = soup.findAll('td') # contient les deux prix/stock/review&UPC
            universal_product_code = soup.findAll('td')[0].text#product_information[0]
            price_excluding_tax = soup.findAll('td')[2].text #product_information[2]
            price_including_tax = soup.findAll('td')[3].text #product_information[3]
            number_available_raw = (soup.findAll('td')[5].text)[-13:-11] #product_information[5]
            numbers = re.findall('[0-9]+', number_available_raw)
            number_available = numbers[0]
            image_url = "https://books.toscrape.com/" + soup.find('img')['src'][6:]
            category = (soup.findAll('li')[2].text)[1:-1]
            product_descriptionraw = (soup.find('meta', {"name": "description"}).get('content'))[1:-1]
            product_description = slugify(product_descriptionraw)

            if soup.find("p", class_= "star-rating Zero") :
                review_rating = 0
            elif soup.find('p', class_ = "star-rating One"):
                review_rating = 1
            elif soup.find('p', class_ = "star-rating Two"):
                review_rating = 2
            elif soup.find('p', class_ = "star-rating Three"):
                review_rating = 3
            elif soup.find('p', class_ = "star-rating Four"):
                review_rating = 4
            elif soup.find('p', class_ = "star-rating Five"):
                review_rating = 5
            else:
                review_rating = "Missing data"

            results.append(
                {
                "title":title,
                "url": url,
                "category": category,
                "universal product code": universal_product_code,
                "review rating": review_rating,
                "PET": price_excluding_tax,
                "PIT": price_including_tax,
                "stock": number_available,
                "image url":image_url,
                "product description": product_description
            }
            )
        else:
            print("url not responsive")


    return results

def fill_csvs():
    books = get_book_info_from_url()
    categories = get_all_categories_names()
    header = ['title', 'url', 'category', 'universal product code', 'review rating', 'PET', 'PIT', 'stock', 'image url',
              'product description']
    foldernamecsv = 'csvs'
    os.makedirs(foldernamecsv)
    for category in categories: # creation des csvs
        filename = category
        with open(os.path.join(foldernamecsv, filename + '.csv'), 'w') as tableau:
            writer = csv.writer(tableau, delimiter='/')
            writer.writerow(header) # fin de création des csv et ajout des headers
    for book in books: #remplissage des csvs
        title = book.get('title')
        category = book.get('category')
        url = book.get('url')
        universalproductcode = book.get('universal product code')
        review_rating = book.get('review rating')
        PET = book.get('PET')
        PIT = book.get('PIT')
        stock = book.get('stock')
        image_url = book.get('image url')
        product_description = book.get('product description')

        with open(os.path.join(foldernamecsv, category+'.csv'), 'a', newline="") as tableau2:
            writer = csv.writer(tableau2, delimiter='/')
            row = (title, url, category, universalproductcode, review_rating, PET, PIT, stock, image_url, product_description)
            writer.writerow(row)
    return


def dl_images():
    rawdata = get_book_info_from_url()
    foldername = 'img'
    #creation du folder
    os.makedirs(foldername)
    #with open ('allimg'+ datetime, 'wb')as folder:
    for book in rawdata:
        filenameraw = book.get('title')
        if len(filenameraw) > 35:
            filename = filenameraw[0:35]
        else:
            filename = filenameraw
        filenamelast = slugify(filename)

        image = book.get('image url')
        img_data = requests.get(image).content
        with open(os.path.join(foldername, filenamelast), 'wb') as downloader:
            downloader.write(img_data)
    print("-------All Images were retrieved and saved successfully-------")
    return


fill_csvs()


dl_images()




