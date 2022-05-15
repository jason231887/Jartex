from bs4 import BeautifulSoup as bs
import requests
from time import gmtime, strftime
from csv import writer

url = 'https://store.jartexnetwork.com/'

name = []

item = []

count = 0

page = requests.get(url)

soup = bs(page.content, "html.parser")

itemlocator = soup.findAll("div", {"class":"head toggle-tooltip"})

length = len(itemlocator)

f = open('jartex.csv', "a", newline = '')
header = ['Name', "Item", "Time"]
writer = writer(f)
for items in itemlocator:
    temp = str(items)
    nameStr = temp.partition('helmavatar')[2]
    nameStr = nameStr.replace('/','',1)
    nameStr = nameStr.split('/', 1)[0]
    name.append(nameStr)
    print("Name: " + name[count])
    temp = str(items)
    itemStr = temp.partition('small&gt;')[2]
    itemStr = itemStr.split('&', 1)[0]
    itemStr = itemStr.replace('➔','->')
    itemStr = itemStr.replace('·','',1)
    item.append(itemStr)
    print("Item: " + item[count])
    time = (strftime("%Y-%m-%d", gmtime()))
    fullList = [name[count], item[count], time] 
    writer.writerow(fullList) 
    count+=1
f.close()