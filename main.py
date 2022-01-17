from bs4 import BeautifulSoup
import requests
import re
import csv
import matplotlib.pyplot as plt


def get_data():

    # creating a loop to so that the user can scrape as many products required
    while True:
        # storing the input to create the link of product
        search = input("What product do you want to search for?(Type '0' to quit) \n")

        # condition to stop the loop
        if search == '0':
            break

        else:
            # basic sturture of bs4
            url = f"https://www.newegg.ca/p/pl?d={search}&N=4131"
            page = requests.get(url).text
            doc = BeautifulSoup(page, "html.parser")

            # finding the product page
            page_text = doc.find(class_="list-tool-pagination-text").strong
            # finding the number of pages of the products
            pages = int(str(page_text).split("/")[-2].split(">")[-1][:-1])

            # creating a dict to store the values of products
            items_found = {}

            # looping through all the pages to find all the prices of the products
            for page in range(1, pages + 1):
                url = f"https://www.newegg.ca/p/pl?d={search}&N=4131&page={page}"
                page = requests.get(url).text
                doc = BeautifulSoup(page, "html.parser")
                try:
                    div = doc.find(class_="item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell")
                    items = div.find_all(text=re.compile(search))
                except Exception:
                    print('Product not found')

                # finding all the a tags where all the attributes are present
                for item in items:
                    parent = item.parent
                    if parent.name != "a":
                        continue

                    # getting the link of the product
                    link = parent['href']
                    next_parent = item.find_parent(class_="item-container")
                    try:
                        # getting the price of the product
                        price = next_parent.find(class_="price-current").find("strong").string
                        items_found[item] = {"price": int(price.replace(",", "")), "link": link}
                    except:
                        pass

            # creating a list of the dicts to use it for plotting, creating csv and displaying the output
            sorted_items = sorted(items_found.items(), key=lambda x: x[1]['price'])

            # creating a list to store it as a csv file
            data = []

            # code for displaying the output in the terminal
            for item in sorted_items:
                print(item[0])
                print({item[1]['price']})
                print(item[1]['link'])
                print("-------------------------------")
                data.append([item[0], item[1]['price'], item[1]['link']])

            # creating the csv file using the csv module
            with open(f'{search}-data.csv', 'w', encoding='UTF8') as f:
                writer = csv.writer(f)
                writer.writerow(['Product names', 'price in USD', 'link to the product'])
                writer.writerows(data)

            # creating the coordinates to plot the graph
            x = [int(i) for i in range(1, len(data) + 1)]
            y = [int(j[1]) for j in data]

            # creating a bar graph
            plt.bar(x, y)
            # showing the graph
            plt.show()


if __name__ == '__main__':
    get_data()
