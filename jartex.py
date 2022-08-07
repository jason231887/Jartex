from audioop import reverse
from pickle import TRUE
from bs4 import BeautifulSoup as bs
import requests
from time import gmtime, strftime
import csv

def main():
    #URL of the store page
    url = 'https://store.jartexnetwork.com/'

    name = []

    item = []

    count = 0

    #List of 6 most recent IGN's
    recentName = []

    #List of 6 most recent item names
    recentItem = []

    #Open .csv file for reading
    with open ('jartex.csv') as csvFile:
        temp = 0
        reader = csv.reader(csvFile)
        #Read the csv file from the bottom to get most reccent purchases
        for row in reversed(list(reader)):
            tempString = str(row)
            tempName = tempString.partition("'") [2]
            tempName = tempName.partition("'") [0]
            tempItem = tempString.partition(',') [2]
            tempItem = tempItem.partition("'") [2]
            tempItem = tempItem.partition("'") [0]
            #print(str(tempName) + '\n' + str(tempItem))
            recentName.append(tempName)
            recentItem.append(tempItem)
            temp+=1
            if temp > 5:
                break

    #Get the page
    page = requests.get(url)

    #Parses the html
    soup = bs(page.content, "html.parser")

    #Find all instances of the specified string
    itemlocator = soup.findAll("div", {"class":"head toggle-tooltip"})

    #Open a .csv file with the according header names
    f = open('jartex.csv', "a", newline = '')
    header = ['Name', "Item", "Time"]
    #Create a writer to write the data into the .csv file
    writer = csv.writer(f)

    #Loop through each iteration where we found the needed string
    for items in itemlocator:
        write = True
        #Create a temporary string to find the name
        temp = str(items)
        #Cut the string to where the IGN starts
        nameStr = temp.partition('helmavatar')[2]
        #Remove the '/' from the string 
        nameStr = nameStr.replace('/','',1)
        #Remove the text after the IGN
        nameStr = nameStr.split('/', 1)[0]
        #Add the name to the name array
        name.append(nameStr)
        #Create a temporary string to find the purchase item
        temp = str(items)
        #Cut the string to where the purchase item starts
        itemStr = temp.partition('small&gt;')[2]
        #Remove the text after the purchase item
        itemStr = itemStr.split('&', 1)[0]
        #If there is an arrow, replace with an html arrow
        itemStr = itemStr.replace('➔','->')
        #Remove any dots in the purchase item
        itemStr = itemStr.replace('·','',1)
        #Add the purchase item to the array
        item.append(itemStr)
        #Get the time 
        time = (strftime("%Y-%m-%d", gmtime()))

    count = 0
    #Reverse the order of the lists to start at the oldest
    item.reverse()
    name.reverse()

    #Compare name to any old names if match, then compare purchase
    #z=new list of names, x=recent 6 names, y=recent 6 items
    for z in (name):
        write = True
        for x in recentName:
            if z == x:
                for y in recentItem:
                    if item[count] == y:
                        write = False

        #If no old names match new names, then write the data to the csv file
        if write == True:
            #Add the IGN, purchase item, and time to the final array
            fullList = [z, item[count], time] 
            #Print out purchase to terminal
            print(z + ': ' + item[count])
            #Write the data to the .csv file
            writer.writerow(fullList) 
        count+=1

    f.close() 