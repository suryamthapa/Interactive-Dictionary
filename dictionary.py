"""
------------------------------------------------------------
This is the complete walkthough of my dictionary project.
If you want to jump to the code directly, it starts from line 
But, if you are a begineer, i suggest you to go thoroughly.
Learn from my mistakes.
-------------------------------------------------------------

So, this is the project i have started.

> Goals:
 1. To build an interactive dictionary
 2. To make it able to suggest near-to-possible words if user has typo

> Libraries:
As a begineer, i didn't know much more about the work flow of application development.
So, i took the help of the tutorial.
The tutorial was of the same dictionary project, but without GUI.
Additional to the tutorial, i have added the GUI, with the help of TKINTER framework,
which comes built-in python.
------------------------------------------------------------------------------------
> Resources:
I got a json file with large number of words and meanings.
In the tutorial, tutor used JSON library to get a dictionary from json file.
It was quite simple.
Additionally, i thought of other ways to make the job done.
First, let's walk through the tutorial.
-------------------------------------------------------------------------------
"""
import json
from difflib import SequenceMatcher, get_close_matches
# Difflib librery helps to find the best match of the word out of the list

def translate(word):
    f = json.load(open("dict_data.json")) # Conversion of json file to dictionary
    if word.lower() in f.keys():
        return f[f"{word}"]
    else:
        key = get_close_matches(word,f.keys(),n=1,cutoff=0.8) # get the close match (n is the number of matches)
        try:
            key = key[0]
            confirm = input(f"Do you mean {key} instead? Enter Y for Yes and N for No:")
            if confirm.lower()=="y":
                return f[f"{key}"]
            elif confirm.lower() == "n":
                return "The word is not in the dictionary."
        except:
            return "The word is not available."
                

    
## Program Execution
# while True:
#     word = input("Enter the word: ")
#     meaning = translate(word)
#     for i in meaning:
        # print(i)
#     break
"""
So, this is the simple dictionary, which runs in the command line.
Now, lets see how we can make it more interactive.
"""
"""
To get a progress bar: 
"""
# from tqdm import tqdm,trange
# from time import sleep
# # help(tqdm)
# with tqdm(total = 100) as bar:
#     for i in range(100):
#         # sleep(0.1)
#         bar.update(1)

"""
Another approach of the  dictionary:
Let's Use the concepts of the databases(Mysql).
To achieve this, we should be able to import the words and meanings of given json files in the database tables.
So, how can we convert the data inside json into the table in database??

          ---CONVERTING JSON TO DATABASE TABLE---

I found that we can not directly import json file in phpmyadmin.
But i guess it can be achieved with the help of workbench.(It's okay, if you don't know about it.)
But i found that phpmyadmin supports csv files.
and lets do it...

First, let's convert json file to csv file.
Let's do it.
"""

import json
from csv import DictReader, DictWriter,reader, writer
jsdata  = json.load(open("dict_data.json"))

"""
Note:
In JSON files, data are saved in the dictionary format(key value pairs):
And in case of the given json file we have words/expressions as keys & meanings as value.
Values are in list format (You can see the JSON file) and one words/expressions can have different meanings.
So first we have to convert it to plane format...(one word/expression = one meaning)
MAKING THE DICTIONARY PLANE(writing it into the csv file)
"""

def json_to_csv():
    with open("dict_data.csv","w",encoding="utf8",newline="") as data:
        # help(DictWriter)
        #defining the headings of the csv file
        header = ("Expression","Definition") 
        csvwriter = DictWriter(data , fieldnames=header,delimiter='|' )
        csvwriter.writeheader() #writing the headings of the csv file
        for exp,defi in jsdata.items():#looping through the json data
            for definition in defi: #looping through the list of definitions
                #writing the rows by passing the dictionary accordindly
                csvwriter.writerow({"Expression":f"{exp}","Definition":f"{definition}"})
## Run the function
# json_to_csv()
"""
Congratulations!
We successfully got a csv file out of json file.

When i found that the delimeter comma(,) used in the csv file get me into trouble 
then i changed the delimeter to the pipe (|), now it works.
The reason is : 
Meanings are separated by commas(and fields are also separated by comma)
So while loading data from csv into the database table--it will get confused(between the field and meanings)
So will give the warings(more data than the input column)
Now: lets connect to the database using mysql-connector-python and load csv file.
NOTE: If you are not using phpmyadmin for database, it's okay!
      Directly jump to line 
"""
# import mysql.connector as ms
# import time
# from difflib import get_close_matches
# con = ms.connect(user = "root",password = "",host = "localhost",database = "class")
# cursor = con.cursor()

"""
We can have a database file (with .pd extension) and load the data in csv file directly to table.
(You should have some knowledge of sql query.)
After the required table is created.
We can work on our dictionary.
"""

import sqlite3 as sq 
conn = sq.connect("dictionary.pd")
cursor= conn.cursor()

# To search for the word in the dictionary
# And returning the list of result
def search(word):
    list_of_result = []
    if len(word)>0:
        l_word = word.lower().rstrip()
        cap_word = word.capitalize().rstrip()
        # print(l_word)
        # print(cap_word)
        cursor.execute(f"SELECT Definition FROM dictionary WHERE Expression = '{l_word}' or Expression = '{cap_word}';")
        result = cursor.fetchall()
        # print(len(result))
        if len(result)!=0:
            for meanings in result:
                for mean in meanings:
                    list_of_result.append(mean.rstrip())
            return list_of_result
        else:
            check_close_match2(word)
            return 1
    else:
        return 0

# To get the close matches of the given word in the database table
# And returning the final result
def check_close_match1(word):
    global window
    cursor.execute("SELECT Expression from dictionary;")#query for selecting the expressionss
    raw_list_of_exp = cursor.fetchall() #fetching the list of the expressionss
    list_of_exp = []
    for tup in raw_list_of_exp:
        for exp in tup:
            list_of_exp.append(exp.rstrip())
    close_match = get_close_matches(word,list_of_exp,n=1,cutoff=0.8)#getting the close match
    if close_match:
        new_word = close_match[0]
        # without gui
        confirm = input(f"Do you mean {new_word} instead? Enter Y for Yes and N for No:")
        if confirm.lower()=="y":
            list_of_result = search(new_word)
            return list_of_result
        elif confirm.lower()=="n":
             return ["There is not such word in the dictionary."]
    else:            
        return ["There is not such word in the dictionary."]

#Running the programme 
# word = input("Enter the word: ")
# result = search(word)
# if result:
#     # print(result)
#     for i in result:
        # print(i)
"""
So, we successfully used the concept of database in our dictionary.

Learnings:
Difflib library: get_close_matches(), SequenceMatcher()
Mysql general approach.
This was funn.

But i thought, i should add some gui here.
So, i had just watched some tutorials about tkinter.
And i am going to apply some ideas here.
Let's make it user friendly.

We already have search function!
So, we don't need to rewrite.
"""

# Defining the function again
def check_close_match2(word):
    global window
    cursor.execute("SELECT Expression from dictionary;")#query for selecting the expressionss
    raw_list_of_exp = cursor.fetchall() #fetching the list of the expressionss
    list_of_exp = []
    for tup in raw_list_of_exp:
        for exp in tup:
            if exp!=None:
                list_of_exp.append(exp.rstrip())
    close_match = get_close_matches(word,list_of_exp,n=5,cutoff=0.8)#getting the close match
    if len(close_match) != 0:
        new_word = close_match[0]
        # for tkinter
        text.delete("1.0",END)
        text.insert(END,f"Do you mean '{new_word}' instead?")
        new_btn1 = Button(window,text="Yes",command=lambda: proceed("Y",new_word))
        new_btn1.grid(row=3,column=0,padx = 10)
        new_btn2 = Button(window,text="No",command=lambda:  proceed("N",new_word))
        new_btn2.grid(row=3,column=1,padx=10)
        pass
    else:            
        show_result(["There is not such word in the dictionary."])
        pass

# To proceed after finding the new word list
def proceed(confirm,new_word):
    confirm = confirm
    if confirm.lower()=="y": # If user press "Yes"
        entry.delete(0,END)
        entry.insert(END,f"{new_word}")
        list_of_result = search(new_word)
        result = list_of_result
        # print(result)
        show_result(result)
        yn_destroy() # To destroy the yes/no button
        pass
    elif confirm.lower()=="n": #If user press "No"
        result = ["There is not such word in the dictionary."]
        show_result(result)
        yn_destroy() # To destroy the yes/no button
        pass

# To destroy the yes/no button
def yn_destroy():        
    yn_child = window.winfo_children()
    for i in yn_child[-2:]:
        i.destroy()

# To find the meaning
def find_meaning():
    word = word_var.get()
    result = search(word)
    show_result(result) 
    pass

# To show the result
def show_result(result):
    if result != 0 and result != 1:
        text.delete("1.0",END)
        for i in result:
            if len(i)!=0:
                # print(i)
                text.insert(END,f"{i}\n")
    elif result == 1:
        a = 1
    else:
        text.delete("1.0",END)
        text.insert(END,"Please type a word!")


# About the dictionary
def about_dict():
    information = """
    Interactive dictionary!
    Version 2.0
    By Suryam Thapa Kshetri
    
    Additioanal Features:
    > Interactive interface
    > Get the word suggestions if typing mistake.
    """
    messagebox.showinfo("Information",information)


# Tkinter GUI
from tkinter import *
from tkinter import PhotoImage
from tkinter import messagebox
# Gui window
window = Tk()
window.title("Dictionary")
window.geometry('1000x250')
window.configure(bg="blue")
window.resizable(0,0)
# Entry
word_var = StringVar()
entry = Entry(window,textvariable=word_var,font="Courier")
entry.grid(row=0,column=0)

# Search button
search_btn = Button(window,text="Search",command=find_meaning, font="Courier")
search_btn.grid(row=0, column=1,pady=10)

# About button
image = PhotoImage(file="ico2.png")
about_btn = Button(window, command=about_dict,image=image, height=30,width=30)
about_btn.grid(row=0, column=5)

# Text Button
text = Text(window,height=10, width=100,font="Courier")
text.grid(row=2,column=0,columnspan=6,rowspan=6)

# Mainloop
window.mainloop()            \

# So now this is the end of the dictionary
# OFFICIALLY