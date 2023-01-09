import gspread
from bs4 import BeautifulSoup as bs
import requests
from time import gmtime, strftime

def main():
    #Set up
    sa = gspread.service_account(filename="keys.json")
    sh = sa.open("JartexStore")
    wks = sh.worksheet("jartex")

    #Setup variables
    #rows = the # of rows in the sheet
    rows = wks.row_count
    temp = 0
    count = 0

    #Link of the store page
    url = 'https://store.jartexnetwork.com/'

    # List where the final names/purchases are stored
    name = []
    item = []

    # List of 6 most recent IGN's/purchases are stored
    recentName = []
    recentItem = []

    #Read the last 6 rows to get the most recent purchases
    while temp < 5:
        # temp string for the whole row
        tempString = str(wks.row_values(rows-temp))

        # Seperate the name and purchase from whole row string
        tempName = tempString.partition("'")[2]
        tempName = tempName.partition("'")[0]
        tempItem = tempString.partition(',')[2]
        tempItem = tempItem.partition("'")[2]
        tempItem = tempItem.partition("'")[0]

        # Append the names/purchases to final array
        recentName.append(tempName)
        recentItem.append(tempItem)
        temp += 1

    # Get the page
    page = requests.get(url)

    # Parses the html
    soup = bs(page.content, "html.parser")

    # Find all instances of the specified string
    itemlocator = soup.findAll("div", {"class": "head toggle-tooltip"})

    for items in itemlocator:
        # Create a temporary string to find the name
        temp = str(items)
        # Cut the string to where the IGN starts
        nameStr = temp.partition('helmavatar')[2]
        # Remove the '/' from the string
        nameStr = nameStr.replace('/', '', 1)
        # Remove the text after the IGN
        nameStr = nameStr.split('/', 1)[0]
        # Add the name to the name array
        name.append(nameStr)
        # Create a temporary string to find the purchase item
        temp = str(items)
        # Cut the string to where the purchase item starts
        itemStr = temp.partition('small&gt;')[2]
        # Remove the text after the purchase item
        itemStr = itemStr.split('&', 1)[0]
        # If there is an arrow, replace with an html arrow
        itemStr = itemStr.replace('➔', '->')
        # Remove any dots in the purchase item
        itemStr = itemStr.replace('·', '', 1)
        # Add the purchase item to the array
        item.append(itemStr)
        # Get the time
        time = (strftime("%Y-%m-%d", gmtime()))

    # Compare name to any old names if match, then compare purchase
    # z=new list of names, x=recent 6 names, y=recent 6 items
    for z in (name):
        write = True
        for x in recentName:
            if z == x:
                for y in recentItem:
                    if item[count] == y:
                        write = False

        # If no old names match new names, then write the data to the csv file
        if write == True:
            # Add the IGN, purchase item, and time to the final array
            fullList = [z, item[count], time]
            # Print out purchase to terminal
            print("\t" + z + ': ' + item[count])
            # Write the data to the .csv file
            wks.append_row(fullList, table_range="A1:C1")
        count += 1