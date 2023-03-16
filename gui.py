import gspread
from tkinter import *
from tkinter.ttk import *
from tkinter.scrolledtext import ScrolledText

root = Tk()
root.title('JartexStore')
root.geometry("1000x1000")

#Set up
sa = gspread.service_account(filename="keys.json")
sh = sa.open("JartexStore")
wks = sh.worksheet("jartex")

#Get user input for username to check
input_text = Entry(root, width=80)
input_text.pack(pady=20)
input_text.focus_set()

names = wks.col_values(1)
items = wks.col_values(2)

#Get the purchases made by the input username
def get_purchases():
    global input_text
    name = input_text.get()
    purchases.delete(1.0,"end")
    #Set name to lowercase to match in the list
    name = name.lower()
    list = ''
    #look through both columns and turn to tuple
    for cella, cellb in zip(names, items):
        #Set the names to lowercase to match the input username
        match = str(cella)
        match = match.lower()
        #If match, then add the purchase to list
        if match == name:
            list = f'{list + str(cellb)}\n'
    #Set label to the list of purchases
    purchases.insert(1.0, list)

def get_names():
    global input_text
    name = input_text.get()
    purchases.delete(1.0,"end")
    #Set text to lowercase to match in the list
    name = name.lower()
    list = ''
    #look through both columns and turn to tuple
    for cella, cellb in zip(items, names):
        #Set the items to lowercase to match the input
        match = str(cella)
        match = match.lower()
        #If match, then add the name to list
        if match == name:
            list = f'{list + str(cellb)}\n'
    #Set label to the list of names
    purchases.insert(1.0, list)

button_frame = Frame(root)
button_frame.pack()

name_button = Button(button_frame, text="Get Purchases", command= get_purchases)
name_button.grid(row=0, column=0, padx=10)

purchase_button = Button(button_frame, text="Get Names", command= get_names)
purchase_button.grid(row=0, column=1, padx=10)

purchases = Text(root, height=200)
purchases.pack(pady=20)

root.mainloop()