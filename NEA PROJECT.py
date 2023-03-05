# importing all libraries
from ast import Pass
from curses import window
from distutils import command
from email.mime import image
from fileinput import filename
from genericpath import exists
from logging import root
from pydoc import text
from re import L
from socket import SO_DEBUG
import tkinter as tk
from tkinter import ttk
from tkinter.tix import ROW
from tkinter.ttk import Label
from tkinter import messagebox
import os
from functools import partial
from tkinter import *
from tkinter import filedialog
from tkinter import font
from turtle import ScrolledCanvas, right
from zlib import DEF_BUF_SIZE
from cv2 import COLOR_LUV2BGR
from django.conf import settings
import mysql.connector
import sqlite3
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tkinter as tk
from PIL import Image, ImageTk
import random

#database creation and connections for user accounts
connection = sqlite3.connect("userdata.db")
cursor = connection.cursor()
cursor.execute("create table if not exists userdata (user text, pass text)")

connection.commit() #store all the rows permanently inside "userdata.db", 
                    #otherwise you might have trouble selecting from external files

#select all rows in database and output
for row in cursor.execute("select distinct * from userdata"):
    print(row)

#create a connection to database and cursor to excecute sql queries
connection1 = sqlite3.connect("userdata.db")
cursor1 = connection1.cursor()

# acts as a line break
print ("**********************")

#select all rows for specific user - testing purposes
cursor.execute("select distinct * from userdata where user=:u", {"u": "aviral"} )
userdata_search = cursor.fetchall()
print(userdata_search)

# acts as a line break
print("***********************")

#save all/any modifications
connection.commit()



##### functions and code

       
def exitconfirm():
    new1 = Toplevel(page)
    #creates new window
    new1.geometry("200x50")
    new1.title("New Window")
    #button to exit
    Button(new1, text="CONFIRM EXIT", bg = 'white', fg='black', command = page.quit).pack()

def account_screen():
 
    # create Login Button 
    Button(text="Login", height="6", width="50", command=login, font=("Comic Sans", 30)).pack(pady = 55) 

    # create a register button
    Button(text="Register", height="6", width="50", command=register, font=("Comic Sans", 30)).pack(pady = 15)
    


def login():
    #global variables that are used later
    global userentry
    global user
    global passwordentry
    global password
    # right now incomplete- once database is set up I will cross check login details to it
    new = Toplevel(page)
    # creates new window for it
    user = StringVar()
    #entry box to enter username
    userentry = tk.Entry(new, textvariable= user, show = '')
    password = StringVar()
    #entry box to enter password
    passwordentry = tk.Entry(new, textvariable= password, show = '*')
    #configure entry boxes
    userentry.grid(row=0, column=1)
    passwordentry.grid(row=1, column=1)
    # taking in username and password which is concealed when typed for security reasons
    tk.Label(new, text="Username", width="30").grid(row=0, column = 0)
    tk.Label(new, text="Password", width="30").grid(row=1, column = 0)
    sbmt = Button(new, text="Submit", command= submit2)
    # configuring dimensions of submission button
    sbmt.grid(row = 2, column = 0)


def submit2():
    global allow 
    #create a connection to database and cursor to excecute sql queries
    connection = sqlite3.connect("userdata.db")
    cursor = connection.cursor()
    cursor.execute("create table if not exists userdata (user text, pass text)")
    #select relevant rows where user name and password are of user input
    cursor.execute("select * from userdata where user = ? and pass = ?", (userentry.get(), passwordentry.get()))
    row = cursor.fetchall() #fetches all (or all remaining) rows of a query result set 
    if row:
        #displays a messagebox to show login status
        messagebox.showinfo('info', 'Login Successful')
        allow = '1'
        #valid login so show main menu
        mainmenu()

    else:
        #displays a messagebox to show login status
        messagebox.showinfo('info', 'Incorrect login, please try again')
        allow = '0'



def register():
    new = Toplevel(page)  # creates new window for it
    #global the user inputs 
    global userentry, user, passwordentry, password
    user = StringVar()
    userentry = tk.Entry(new, textvariable= user, show = '')
    password = StringVar()
    passwordentry = tk.Entry(new, textvariable= password, show = '*')
    # taking in username and password which is concealed when typed for security reasons
    userentry.grid(row=0, column=1)
    passwordentry.grid(row=1, column=1)
    # configuring dimensions
    tk.Label(new, text="Username", width="30").grid(row=0, column = 0)
    tk.Label(new, text="Password", width="30").grid(row=1, column = 0)
    sbmt = Button(new, text="Submit", command = submit)
    sbmt.grid(row = 2, column = 0)


def submit():
    #create a connection to database and cursor to excecute sql queries
    connection = sqlite3.connect("userdata.db")
    cursor = connection.cursor()
    cursor.execute("create table if not exists userdata (user text, pass text)")
    #select relevant rows where user name and password are of user input
    cursor.execute("select * from userdata where user = ? and pass = ?", (userentry.get(), passwordentry.get()))
    #fetches all (or all remaining) rows of a query result set 
    row = cursor.fetchall()

    if row:
        #inform user why it did not work
        messagebox.showinfo('info', 'Username already exists, try again')

    else:
        #store the user inputs into a variable
        u = userentry.get()
        p = passwordentry.get()

        #create sql query  
        query = "insert into userdata values(?,?)"
        #creates tuple with two elements which are user inputs of username and password stored as string
        info_list=(str(u), str(p))
        #inserts username and password to database 
        connection.execute(query,info_list)
        #save changes
        connection.commit()

        #output database
        for row in cursor.execute("select distinct * from userdata"):
            print(row)
        
        messagebox.showinfo('info', 'Registered Successfully!') #tell user account registration was successful

        #valid registration of account so show main menu
        mainmenu()


def pt():
#globalising all variables to be used later in in database and progress tracker
    global score
    global predict
    global attempt
    global confidence
    global grade
    global subject
    global sbchoice
    new = Toplevel(page)
    new.geometry("750x350")
    new.title("Progress Tracker") #window title
 
    #entering data in the window
    attempt = tk.Entry(new)
    confidence = tk.Entry(new)
    subject = tk.Entry(new)
    subject.grid (row = 7, column = 1)
    attempt.grid(row=4, column=1)
    confidence.grid(row=6, column=1)
    tk.Label(new, text="Attempt / Test Number ", width="30").grid(row=4)
    tk.Label(new, text="My Confidence Level", width="30").grid(row=6)   
    tk.Label(new, text="Subject", width="30").grid(row=7)   

    #entering data in the window
    score = tk.Entry(new)
    predict = tk.Entry(new)
    grade = tk.Entry(new)
    sbchoice = tk.Entry(new)
    sbchoice.grid(row = 9, column = 1)
    score.grid(row=2, column=1)
    grade.grid(row=3, column =1)
    predict.grid(row=5, column=1)
    tk.Label(new, text="Score %", width="30").grid(row=2)
    tk.Label(new, text="My Grade", width="30").grid(row=3)
    tk.Label(new, text="My Predicted Grade", width="30").grid(row=5)
    tk.Label(new, text="Subject I want to display progress of", width="30").grid(row=9)

    #buttons to submit data 
    sbmt = Button(new, text="Submit", command= ptsubmit)
    sbmt.grid(row = 10, column = 0)
    display = Button(new, text="Display", command= ptsubmit)
    show = Button(new, text="Display Score Tracker", command= openpt)
    show.grid(row = 11, column = 0)
    show = Button(new, text="Display Confidence Tracker", command= openpt1)
    show.grid(row = 12, column = 0)
    show = Button(new, text="Show all  Data", command= openpt2)
    show.grid(row = 13, column = 0)
    show = Button(new, text="Confirm", command= subjectchoice)
    show.grid(row = 9, column = 2)

def ptsubmit():
# creating progress tracker database
    connection = sqlite3.connect("Trackers.db")
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS Trackers (
        user text, 
        score text, 
        predict text, 
        grade text, 
        attempt text,
        confidence text,
        subject, text)""")

    #get the inputs of user
    g = grade.get()
    u = user.get()
    c = confidence.get()
    a = attempt.get()
    s = score.get()
    pr = predict.get()
    sb = subject.get()

    #if score is greater than 100% disallow it
    if float(s) > 100:
        messagebox.showerror("Error", "Score cannot be greater than 100")
        return

    #if confidence is greater than 10 disallow it
    if int(c) > 10:
        messagebox.showerror("Error", "Confidence cannot be greater than 10")
        return

    #insert all user inputs to database
    query = "insert into Trackers (user, score, predict, grade, attempt,confidence,subject) VALUES (?,?,?,?,?,?,?)"
    info_list=(str(u), float(s), str(pr), str(g), int(a), int(c), str(sb))
    cursor.execute(query,info_list)

    connection.commit() #save modifications

    for row in cursor.execute("select distinct * from Trackers"):
        print(row) #prints rows from database

def subjectchoice():
    global sbc
    sbc = sbchoice.get()

def ptshow():
    try:
        #create a connection to database and cursor to excecute sql queries
        connection = sqlite3.connect('Trackers.db')
        cursor = connection.cursor()
        #select rows from Tracker.db
        cursor.execute("select * from Trackers")
        list = cursor.fetchall()
        print("Total rows are:  ", len(list)) #print total rows
        print("Printing each row")

        #output database but labelled
        for row in list:
            print("User: ", row[0])
            print("Score: ", row[1])
            print("Predicted Grade: ", row[2])
            print("Grade: ", row[3])
            print("Attempt: ", row[4])
            print("Confidence: ", row[5])
            print("Subject: ", row[6])

            print("\n")

    #error handling
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if connection:
            connection.commit()

    mydb = sqlite3.connect('Trackers.db') #create new connection
    mycursor = mydb.cursor()
    u = user.get() #get username input by user

    # Fecthing Data From mysql to my python progame
    mycursor.execute("SELECT * FROM Trackers WHERE user=:u AND subject=:sb", {"u": u, "sb": sbc})  
    result = mycursor.fetchall()
    print("RESULT",result)
    
    #array of score, attempt and confidence
    score = []
    attempt = []
    confidence = []

    #append row items into relevant array
    try:
        for row in result:
            score.append(row[1])
            attempt.append(row[4])
            confidence.append(row[5])
    except TypeError as te:
     print(te)

    #displaying relevant arrays
    print("Score = ", score)
    print("Attempts = ", attempt)
    print("Confidence = ", confidence)

    #using pandas dataframes
    df = pd.read_sql(f"select score, attempt, confidence from Trackers where user='{u}' and subject ='{sbc}'", mydb)
    df['attempt']=df['attempt'].astype(int)
    df['score']=df['score'].astype(float)
    df['confidence']=df['confidence'].astype(float)

    print (df.dtypes)
    #plottinng dataframe and setting ranges for axes
    df.plot(x = "attempt" ,y= "score" ,kind = "line", ylim=(0,100), ylabel = "Score", xlabel = "Attempt")

    #display graph
    plt.show()

def graph1():
    mydb = sqlite3.connect('Trackers.db') #connect to database
    cursor = mydb.cursor() #create cursor
    u = user.get() #get username user input
    sbc = sbchoice.get() #get subject user wants to view from entry box

    # Fecthing Data From mysql to my python progam
    cursor.execute("SELECT * FROM Trackers WHERE user=:u and subject=:sbc", {"u": u, "sbc": sbc})
    result = cursor.fetchall()
    print("RESULT",result)
    
    score = [] #score array
    attempt = [] #attempt array
    confidence = [] #confidence array

    #append row items into relevant array
    try:
        for row in result:
            score.append(row[1])
            attempt.append(row[4])
            confidence.append(row[5])

    except TypeError as te:
     print(te) #if there is an error
    
    #print arrays
    print("Score = ", score)
    print("Attempts = ", attempt)
    print("Confidence = ", confidence)

    #convert database into pandasdataframe
    df = pd.read_sql(f"select score, attempt, confidence from Trackers where user='{u}' and subject ='{sbc}'", mydb)
    df['attempt']=df['attempt'].astype(int) #attempt items are integers
    df['score']=df['score'].astype(float) #score items are float
    df['confidence']=df['confidence'].astype(float)
    print (df.dtypes)
    #plotting graph
    df.plot(x = "attempt" ,y= "confidence" ,kind = "line", ylim=(0,10), ylabel = "Confidence", xlabel = "Attempt")
    #show graph
    plt.show()

def allprogressdata():
    u = user.get()
    mydb = sqlite3.connect('Trackers.db')
    mycursor = mydb.cursor()
    w = tk.Tk()
    w.geometry("400x250") #window dimensions
    w.configure(bg = 'maroon')
    w.title("MY PROGRESS DATA")
    #using tkinter to print labels with database rows
    rows = mycursor.execute("SELECT score, predict, grade, attempt, confidence, subject from Trackers where user=:u", {"u": u})  
    tk.Label(w, text="Score %, Grade, Predicted Grade, Attempt/Test Number, Confidence Level \n", bg = "maroon" , width = 100, font = ("Arial", 30)).pack()

    for row in rows:
        tk.Label(w, text=row, width = 100, bg = "maroon" , font = ("Arial", 30)).pack()


###to open different graphs or tables in progress tracker
def openpt():
    if allow == '1': #if user is logged in
        ptshow()
    else:
        messagebox.showinfo('info', 'Incorrect login, can not access progress tracker')

def openpt1():
    if allow == '1': #if user is logged in
        graph1()
    else:
        messagebox.showinfo('info', 'Incorrect login, can not access progress tracker')

def openpt2():
    if allow == '1': #if user is logged in
        allprogressdata()
    else:
        messagebox.showinfo('info', 'Incorrect login, can not access progress tracker')


def material():
    global status
    global typenew
    #window for the revision material feature
    window = Tk()
    window.title("MY REVISION MATERIAL")
    window.geometry('550x400')
    
    #buttons and their configuration - to access or save files
    #open files button
    openbtn = Button(window, text = 'OPEN FILES' , command = opengui)
    openbtn.place(x=200, y=10)
    #save file button
    savebtn = Button(window, text = 'SAVE FILE' , command = savefile)
    savebtn.place(x=100, y=10)
    #edit file button
    editbtn = Button(window, text = 'EDIT FILES' , command = editfile)
    editbtn.place(x=310, y=10)
    #delete file button
    deletebtn = Button(window, text = 'DELETE FILE' , command = removewhich)
    deletebtn.place(x=413, y=10)
    #allow user to create a new text file
    typenew = Text(window) 
    typenew.place(x=0, y=50)

    #status bar
    status = Label(window, text = 'Ready    ', anchor = E)
    status.pack(fill = X, side = BOTTOM)

    window.mainloop() 




def query_files():
    #get the username
    u = user.get()
    #create connection to database and a cursor to execute queries
    connection = sqlite3.connect('file.db')
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE if not exists file
            (id INTEGER PRIMARY KEY,
            user TEXT,
            filename TEXT,
            data BLOB)''')
    # execute the SELECT statement to retrieve a list of filenames under users account
    cursor.execute("SELECT filename FROM file where user=:u", {"u": u})
    #fetch all results
    files = cursor.fetchall()
    connection.close()
    return files


def opengui():
    # create the GUI
    root = Tk()
    root.title("OPEN FILES")

    # create the listbox widget
    global listbox
    listbox = Listbox(root)
    listbox.pack(expand=YES, fill=BOTH)

    # create the buttons
    frame = Frame(root)
    frame.pack(pady=10)
    Button(frame, text='Display Files', command=display_files).pack()
    Button(frame, text='Open File', command=open_file).pack()

def display_files():
    #get all relevant filenames 
    files = query_files()
    listbox.delete(0, END)
    for file in files:
        # filename is a tuple, so we need to access the first element using file[0]
        listbox.insert(END, file[0])



def open_file():
    #get selected item from listbox
    selected_items = listbox.curselection()
    if selected_items:
        # get the filename and data from the database
        file_id = selected_items[0] + 1
        connection = sqlite3.connect('file.db')
        cursor = connection.cursor()
        cursor.execute('SELECT filename, data FROM file WHERE id = ?', (file_id,))
        result = cursor.fetchone()
        connection.close()
        filename = result[0] #filename
        data = result[1] #data
        
        # decode the data from bytes to string
        text = data.decode()

        # add the text to the text area
        typenew.delete('1.0', END)
        typenew.insert(END, text)
    else:
        messagebox.showwarning('Error', 'Please select a file to open')





def savefile():
    #get username
    u = user.get()
    connection = sqlite3.connect('file.db')
    cursor = connection.cursor()

    # create a table for the files
    cursor.execute('''CREATE TABLE if not exists file
                (id INTEGER PRIMARY KEY,
                user TEXT,
                filename TEXT,
                data BLOB)''')

    filename = filedialog.asksaveasfile(defaultextension=".*")
    
    # check if there is name for file
    if filename:
        with open(filename.name, 'wb') as file:
            # encode() converts string to bytes
            file.write(typenew.get(1.0, END).encode())

        # reopen the file in binary read mode
        with open(filename.name, 'rb') as file:
            data = file.read()

        # convert the filename to a string
        filename_str = str(filename.name)

        # pass a tuple with three values to the execute method
        cursor.execute("INSERT INTO file (user, filename, data) VALUES (?, ?, ?)",
                       (u, filename_str, sqlite3.Binary(data)))

        # commit the changes and close the connection
        connection.commit()
        connection.close()


       
def removewhich():
    # create the GUI
    root = Tk()
    root.title("DELETE FILES")

    # create the listbox widget
    global listbox
    listbox = Listbox(root)
    listbox.pack(expand=YES, fill=BOTH)

    # create the buttons and frame to put buttons into
    frame = Frame(root)
    frame.pack(pady=10)
    Button(frame, text='Display Files', command=display_files).pack()
    Button(frame, text ='Delete', command = deletefile).pack()


def deletefile():
    # get the ID of the file selected in listbox
    selected_items = listbox.curselection()
    if not selected_items:
        # inform user why there is error
        messagebox.showwarning('Error!', 'Please select a file to remove.')
        return

    #add one to get correct file id as indexing in listbox start from 0 but file id starts from 1
    file_id = selected_items[0] + 1

    # create connection
    connection = sqlite3.connect('file.db')
    cursor = connection.cursor()

    # get the filename and data for the selected file
    cursor.execute('SELECT filename, data FROM file WHERE id = ?', (file_id,))
    result = cursor.fetchone()
    filename = result[0]
    data = result[1]

    # remove from database
    cursor.execute("DELETE FROM file WHERE id=?", (file_id,))

    # commit the changes and close the connection
    connection.commit()
    connection.close()

    # check if file exists and if file path exists
    if os.path.exists(filename):
        # remove the file
        os.remove(filename)
        # inform user that file was successfully removed
        messagebox.showwarning('Removed!', 'Successfully removed file: {}'.format(filename))
    else:
        # inform user why there is error
        messagebox.showwarning('Error!', '{} does not exist!'.format(filename))

    # refresh the listbox
    display_files()




def editfile():
    # Creating tkinter window 
    window = Tk()
    window.geometry('1200x300')
    #window title
    window.title("HOW TO EDIT FILES")
    
    # instructions shown in labels
    labelframe = LabelFrame(window, text='How to edit files', font=('Arial', 28))
    labelframe.pack(expand='yes', fill='both')
    
    # instruction 1
    label1 = Label(labelframe, text='1. Click "OPEN FILES"', font=('Arial', 28))
    label1.pack()
    
    # instruction 2
    label2 = Label(labelframe, text='2. Choose the file you would like to edit and click open', font=('Arial', 28))
    label2.pack()
    
    # instruction 3
    label3 = Label(labelframe, text='3. The file should be opened up in the text area for you to edit as you wish', font=('Arial', 28))
    label3.pack()
    
    # instruction 4
    label4 = Label(labelframe, text='4. Once edited click "SAVE FILE" and then choose save', font=('Arial', 28))
    label4.pack()
    
    # instruction 5
    label5 = Label(labelframe, text='5. You will be asked to replace the file by your file manager so all you need to do is accept it', font=('Arial', 28))
    label5.pack()





def ut():
    global econ
    #create new window
    utwin = tk.Tk()
    utwin.geometry("400x250") 
    utwin.title("USEFUL RESOURCES")

    #economics dropdown box and label
    econlabel = tk.Label(utwin, text="Select an economics topic:")
    econlabel.pack()
    econ = StringVar()
    econ.set("Economics")
    drop = OptionMenu(utwin, econ, "Microeconomics", "Macroeconomics")
    drop.pack()

    # add space between buttons
    space = tk.Label(utwin, height=3)
    space.pack()

    #view resources button
    view = Button(utwin, text="View Resources", command=viewresources)
    view.pack()

    #view resources button
    quiz = Button(utwin, text="Test Yourself", command=quizgui)
    quiz.pack()


def quizgui():
    #create words and definitions
    words_and_definitions = [
        ('Macroeconomics is the study of the whole _________', 'economy'),
        ('Theoretically, countries should specialise in producing goods where they have a ____________ advantage', 'comparative advantage'),
        ('Balance of Payments is a records _____________ transactions of a country', 'international'),
        ('Inflation can be measured using the ___________ ______ index', 'consumer price'),
        ('The Principal Agent Problem is essentially a separation of _________ and control', 'ownership'),
        ('X-inefficiency is whe a firms costs are _______ than they should be', 'higher'),
        ('Maximum price is a price set by that government _______ the market equillibrium price level', 'below'),
        ('Ad Valorem Tax is a type of _________ tax', 'indirect'),
        ('In the public sector resources are owned and controlled by a central _________', 'government'),
        ('Game theory helps analyse the relationship between strategic interactions among _________ agents', 'rational')

    ]
    #shuffle the list so it does not output in perfect order
    random.shuffle(words_and_definitions)

    #create the window and call the class
    root = tk.Tk()
    root.title("Test Yourself")
    game(root, words_and_definitions)
    root.mainloop()

class game:
    #define the __init__ method, which initializes the object
    def __init__(self, root, words_and_definitions):
        self.root = root #main window for this function 
        self.words_and_definitions = words_and_definitions #a list of tuples containing sentences and their missing word
        self.score = 0 # set the initial score to 0
        self.score = 0 #sets score initially to 0
        self.current = 0 #sets current question to first in list
        self.wrong_questions = [] #adds questions that were incorrect
        self.wrong_answers = [] #adds answers of incorrect answers

        #title of the game - tells user what to do
        self.title_label = tk.Label(self.root, text='Fill in the Blanks Game', font=('Arial', 18, 'bold'))
        self.title_label.pack()
        
        #adds the text(question) in the first index of the randomly ordered list with questions
        self.card_label = tk.Label(self.root, text=self.words_and_definitions[self.current][0], font=('Arial', 24))
        self.card_label.pack(pady=30) #packs and adds space above and below
        
        #lets the user input
        self.input_box = tk.Entry(self.root, font=('Arial', 16))
        self.input_box.pack(pady=10) #packs and adds space above and below
        #focusses on the input box so user can straight away start typing
        self.input_box.focus()
        
        #allow user to check answer
        self.check_button = tk.Button(self.root, text='Check', command= self.checkanswer , font=('Arial', 16))
        self.check_button.pack(pady=10) #packs and adds space above and below
        
        #gives user live score where their current score is shown relative to the number of questions in list
        self.score_label = tk.Label(self.root, text=f'Score: {self.score}/{len(self.words_and_definitions)}', font=('Arial', 16))
        self.score_label.pack(pady=30) #packs and adds space above and below


    def checkanswer(self):
        user_input = self.input_box.get()
        if user_input == self.words_and_definitions[self.current][1]:
            self.score += 1 #increment score as it was correct
            self.current += 1 #increment question number 
            #show the users current score relative to the amount of questions in the list which is the max score
            self.score_label.config(text=f'Score: {self.score}/{len(self.words_and_definitions)}')
            #there are still questions left to ask then continue
            
            if self.current < len(self.words_and_definitions):
                #delete the text in the input box
                self.input_box.delete(0, 'end')
                #go to next question
                self.card_label.config(text=self.words_and_definitions[self.current][0])
            else:
                #tell user game is over 
                self.card_label.config(text='Game Over')
                self.input_box.config(state='disabled') #disable access to input box
                self.check_button.config(state='disabled') #disable access to check button
                self.exit_button = tk.Button(self.root, text='Exit', command= self.exit_game , font=('Arial', 16)).pack() #exit game
                self.viewwrong_button = tk.Button(self.root, text='View Wrong Questions and Answers', command= self.wrongans , font=('Arial', 16)).pack() #view wrong q and a

        else: #if answer is wrong
            self.score = self.score #score does not change
            self.current += 1 #increment question number 
            if  self.current < len(self.words_and_definitions):
                self.wrong_questions.append(self.words_and_definitions[self.current][0])
                self.wrong_answers.append(self.words_and_definitions[self.current][1])

                #delete the text in the input box
                self.input_box.delete(0, 'end')
                #next question
                self.card_label.config(text=self.words_and_definitions[self.current][0])


    def exit_game(self):
        #destorys the current window
        self.root.destroy()

    def wrongans(self):
        #create a window and set title and dimensions
        root = tk.Tk()
        root.geometry("400x250") 
        root.title("View Wrong Questions and Answers")
        #add labels to window to show what questions were wrong
        Label(root, text = f"You got the following questions wrong: {self.wrong_questions}").pack()
        Label(root, text = f"You got the following answers wrong: {self.wrong_answers}").pack()





def viewresources():
    # check what user chose and output windows accordingly
    if econ.get() == "Microeconomics":
        #create window for microeconomic resources
        global microwin
        microwin = tk.Toplevel()
        microwin.geometry("400x500")
        microwin.title("Microeconomics")
        micro()
    else:
        #create window for macroeconomic resources
        global macrowin
        macrowin = tk.Toplevel()
        macrowin.geometry("400x500")
        macrowin.title("Macroeconomics")
        macro()


def micro():
    #label to act as title 
    econlabel = tk.Label(microwin, text="Vital things to know about Microeconomics", font=("Arial", 16, "bold"))
    econlabel.pack()
    econlabel.pack()

    #buttons that lead to relevant info
    Button(microwin, text='What is Microeconomics?', command=definemicro).pack()
    Button(microwin, text='Types of Market Structures', command=markets).pack()
    Button(microwin, text='Government Intervention', command=govint).pack()
    Button(microwin, text='Principal Agent Problem', command=pap).pack()
    Button(microwin, text='Public vs Private Sector', command=pps).pack()
    Button(microwin, text='Types of Efficiency', command=efficiency).pack()
    Button(microwin, text='Price Discrimination', command=pricediscr).pack()
    Button(microwin, text='Game Theory', command=gametheory).pack()

    #add space   
    space = tk.Label(microwin, height=2)
    space.pack()

    #label to act as title for diagrams section
    diagramlabel = tk.Label(microwin, text="Microeconomics Diagrams", font=("Arial", 16, "bold"))
    econlabel.pack()
    diagramlabel.pack()

    #buttons to show relevant diagrams
    Button(microwin, text='Supply and Demand Diagram', command=sd).pack()
    Button(microwin, text='Cost Revenue Curves (profit maximising firm in monopoly)', command=costcurve).pack()
    Button(microwin, text='Externalities Diagram', command=externalities).pack()
    Button(microwin, text='Third Degree Price Discrimination', command=pricediscr_diagram).pack()

def macro():
    #label to act as title 
    econlabel = tk.Label(macrowin, text="Vital things to know about Macroeconomics", font=("Arial", 16, "bold"))
    econlabel.pack()
    econlabel.pack()

    #buttons that lead to relevant info
    Button(macrowin, text='What is Macroeconomics?', command=definemacro).pack()
    Button(macrowin, text='Aggregate Demand and Supply', command=adas).pack()
    Button(macrowin, text='Economic Growth', command=ecgrowth).pack()
    Button(macrowin, text='Inflation', command=inflation).pack()
    Button(macrowin, text='Macroeconomic Objectives', command=macobj).pack()
    Button(macrowin, text='Fiscal and Monetary Policy', command=fmpolicy).pack()
    Button(macrowin, text='Globalisation', command=globalisation).pack()
    Button(macrowin, text='Absolute and Comparative Advantage', command=adv).pack()
    Button(macrowin, text='Balance of Payments', command=bop).pack()


    #add space   
    space = tk.Label(macrowin, height=2)
    space.pack()

    #label to act as title for diagrams section
    diagramlabel = tk.Label(macrowin, text="Macroeconomics Diagrams", font=("Arial", 16, "bold"))
    econlabel.pack()
    diagramlabel.pack()

    #buttons to show relevant diagrams
    Button(macrowin, text='Aggregate Supply and Demand Diagram', command=adasdiagram).pack()
    Button(macrowin, text='Lorenz Curve', command=lorenz).pack()
    Button(macrowin, text='Laffer Curve', command=laffer).pack()




#functions for all microeconomic vital material
def definemicro():
    #create window
    root = Tk()
    root.title("What is Microeconomics")
    #create the text
    text1 = """What is Microeconomics?:
    Microeconomics is the study of how households make decisions in a particular market.
    It is concerned with the effect of individual decisions by people on society and the economy
    
    """
    #display the text
    econlabel = tk.Label(root, text= text1, font=("Arial", 16, "bold"), justify="left")
    econlabel.pack()  
    tk.mainloop()

def markets():
    #create window
    root = Tk()
    root.title("Types of Market Structures")
    #create the text
    text1 = """Types of Market Structures:
    Monopoly: 
    - Pure monopoly is where one firm is selling a product in a market
    - High barriers to entry 
    - Short run profit maximise
    - Pure monopoly rarely exists in real world
    - Monopoly power is when a firm has >25% market share

    Oligopoly:
    - Few firms dominate market
    - Products are generally differentiated 
    - High barriers to entry
    - High concentration ratio in market
    - Firms are ​interdependent ​so the actions of one firm will affect another

    Natural Monopoly:
    - Economies of scale (Costs reduce when output is increasing) are large so even a single 
      producer can not fully exploit them
    - Very high fixed costs
    - Little to no competition 
    
    Monopsony:
    - Only one buyer in market
    - Rest is same as a basic monopoly

    Contestable Market:
    - Perfect knowledge between firms
    - Very low entry and exit barriers
    - Little to no sunk costs
    
    """
    #display the text
    econlabel = tk.Label(root, text= text1, font=("Arial", 16, "bold"), justify="left")
    econlabel.pack()  
    tk.mainloop()


def govint():
    # create window
    root = Tk()
    root.title("Government Intervention")
    
    # create the text
    text1 = """Why do Governments intervene:
    To correct market failure

    Examples of Forms of Government Intervention
    Taxation: 
    - Indirect Taxes
        * Ad Valorem Tax eg VAT
        * Specific Tax eg fuel duty tax
    - Direct Tax
        * Tax on income, wealth and profit

    Subsidies:
    - Government monetary grant given to producers to lower costs of production and increase
    their production

    Maximum and Minimum Prices:
    - Maximum price below market equilibrium price to encourage consumption
    - Minimum Price above market equilibrium price to discourage consumption

    """
    # display the text
    #justfy - left aligns text
    econlabel = Label(root, text=text1, font=("Arial", 16, "bold"), justify="left")
    econlabel.pack()
    
    root.mainloop()


def pap():
    # create window
    root = Tk()
    root.title("Principal Agent Problem")
    
    # create the text
    text1 = """Principal Agent Problem:
    - Essentially a separation of ownership and control
    - Firms are owned by stakeholders and controlled by CEOs and managers
    - There is a conflict of interest
        * Owners might want to profit maximise to maximise their ROI
        * Managers might want to focus on other things like product innovation

    """
    # display the text
    #justfy - left aligns text
    econlabel = Label(root, text=text1, font=("Arial", 16, "bold"), justify="left")
    econlabel.pack()
    
    root.mainloop()


def pps():
    # create window
    root = Tk()
    root.title("Public vs Private Sector")
    
    # create the text
    text1 = """Public Sector:
    - Part of economy which is owned and controlled by a local or cental government
    - Profit making is not main aim which means some public sector organisations might
      make a loss and this is funded by taxpayers

Private Sector:
    - Part of economy where everything is privately owned and ran
    - these organisations tend to have profit making as a priority compared to public
      sector organisations

    """
    # display the text
    #justfy - left aligns text
    econlabel = Label(root, text=text1, font=("Arial", 16, "bold"), justify="left")
    econlabel.pack()
    
    root.mainloop() 


def efficiency():
    # create window
    root = Tk()
    root.title("Types of Efficiency")
    
    # create the text
    text1 = """Allocative efficiency:
    - Maximises utility and social welfare
    - Resources are distrubuted effectively 

Productive efficiency Sector:
    - Firms produce at lowest average cost

Dynamic efficiency:
    - resources allocated efficiently over time and rate of innovation 
      is optimal
    - related to rate of innvation which leads to lower costs in future
      or better quality products

X-inefficiency:
    - When a firms costs are higher than they should

    """
    # display the text
    #justfy - left aligns text
    econlabel = Label(root, text=text1, font=("Arial", 16, "bold"), justify="left")
    econlabel.pack()
    
    root.mainloop()     

def pricediscr():
    # create window
    root = Tk()
    root.title("Price Discrimination")
    
    # create the text
    text1 = """Price Discrimination:
    - When a firm charges different groups of consumers different prices
      for the same good or service 
    - For example in Football matches- kids tickets are cheaper and there 
      are family tickets at discounted prices
    - Off and on peak times for trains have different prices

    """
    # display the text
    #justfy - left aligns text
    econlabel = Label(root, text=text1, font=("Arial", 16, "bold"), justify="left")
    econlabel.pack()
    
    root.mainloop()    

def gametheory():
    # create window
    root = Tk()
    root.title("Game Theory")
    
    # create the text
    text1 = """Game Theory:
    - A theoretical concept that is concerned with the relationship between strategic interationcs among rational agents
    - Rational agent is an entity that always aims to carry out optimal actions by fully utilising the information it has
    - It can be used to analyse an oligopoly when firms collude, as firms take actions based off what they predict or see 
      other firms do

    """
    # display the text
    #justfy - left aligns text
    econlabel = Label(root, text=text1, font=("Arial", 16, "bold"), justify="left")
    econlabel.pack()
    
    root.mainloop()    


# functions for all the microeconomics diagrams
def sd():
    root = tk.Toplevel()
    root.title("Supply and Demand Diagram")

    #open the image using PIL
    image = Image.open("/Users/aviral/Downloads/supplyanddemand.png")

    #convert the image to a PhotoImage object
    photo = ImageTk.PhotoImage(image)

    #create a label to display the image
    label = tk.Label(root, image=photo)
    label.image = photo
    label.pack()
    #tell user where diagram was taken from
    creditlabel = Label(root, text="Taken from https://www.economicshelp.org", font=("Arial", 10, "bold"), justify="left")
    creditlabel.pack()

    # Start the main event loop
    root.mainloop()

def costcurve():
    root = tk.Toplevel()
    root.title("Cost Revenue Curve")

    #open the image using PIL
    image = Image.open("/Users/aviral/Downloads/monopoly.png")

    #resize the image to half its original size
    new_width = int(image.width/2)
    new_height = int(image.height/2)
    resized_image = image.resize((new_width, new_height))

    #resize image as it was too big 
    #Create a PhotoImage object from the resized image
    photo = ImageTk.PhotoImage(resized_image)

    #create a label to display the image
    label = tk.Label(root, image=photo)
    label.image = photo 
    label.pack()
    #tell user where diagram was taken from
    creditlabel = Label(root, text="Taken from https://www.physicsandmathstutor.com", font=("Arial", 10, "bold"), justify="left")
    creditlabel.pack()

    # Start the main event loop
    root.mainloop()

def externalities():
    root = tk.Toplevel()
    root.title("Externalities Diagram")

    #open the image using PIL
    image = Image.open("/Users/aviral/Downloads/Externalities")

    #Create a PhotoImage object for the image
    photo = ImageTk.PhotoImage(image)

    #create a label to display the image
    label = tk.Label(root, image=photo)
    label.image = photo 
    label.pack()
    #tell user where diagram was taken from
    creditlabel = Label(root, text="Taken from https://www.economicsonline.co.uk/market_failures/externalities.html/", font=("Arial", 10, "bold"), justify="left")
    creditlabel.pack()

    # Start the main event loop
    root.mainloop()

def pricediscr_diagram():
    root = tk.Toplevel()
    root.title("3rd Degree Price Discrimination Diagram")

    #open the image using PIL
    image = Image.open("/Users/aviral/Downloads/Price-discrimination-SNP3.webp")

    #Create a PhotoImage object for the image
    photo = ImageTk.PhotoImage(image)

    #create a label to display the image
    label = tk.Label(root, image=photo)
    label.image = photo 
    label.pack()
    #tell user where diagram was taken from
    creditlabel = Label(root, text="Taken from https://www.economicsonline.co.uk/business_economics/price_discrimination.html/", font=("Arial", 10, "bold"), justify="left")
    creditlabel.pack()

    # Start the main event loop
    root.mainloop()


#functions for all macroeconomic vital material
def definemacro():
    #create window
    root = Tk()
    root.title("What is Macroeconomics")
    #create the text
    text1 = """What is Macroeconomics?:
    Macroeconomics is the study of the whole economy. It is concerned with the issues such as 
    unemployment, inflation and economic growth.
    
    """
    #display the text
    econlabel = tk.Label(root, text= text1, font=("Arial", 16, "bold"), justify="left")
    econlabel.pack()  
    tk.mainloop()


def adas():
    #create window
    root = Tk()
    root.title("Aggregate Demand and Supply")
    #create the text
    text1 = """Aggregate Demand:
    - Total demand for goods and services within a particular market
    - C + I + G + (X-M)
        * C (consumption)
        * I (investment)
        * G (government spending)
        * X-M (net Export / Import)

Aggregate Supply:
    - Total supply of goods and services in a particular market from producers
    - Affected by quantity and productivity of labour and capital

    """
    #display the text
    econlabel = tk.Label(root, text= text1, font=("Arial", 16, "bold"), justify="left")
    econlabel.pack()  
    tk.mainloop()   

def ecgrowth():
    #create window
    root = Tk()
    root.title("Economic Growth")
    #create the text
    text1 = """Economic Growth:
    - The increase in real GDP or real output
    - During periods of economic growth...
        * Unemployment is low
        * Incomes are higher
        * Consumer and business confidence is high
        * Reduced poverty
        * Better education 
        * Better healthcare
    
    """
    #display the text
    econlabel = tk.Label(root, text= text1, font=("Arial", 16, "bold"), justify="left")
    econlabel.pack()  
    tk.mainloop()  


def inflation():
    #create window
    root = Tk()
    root.title("Inflation")
    #create the text
    text1 = """Inflation:
    - The increase in the average price level
    - The UK aims for 2 percent inflation
    - Measured using the Consumer Price Index (CPI), which
      measures the percentage change in prices of a basket of 
      a basket of goods and services bought by most households
    
    """
    #display the text
    econlabel = tk.Label(root, text= text1, font=("Arial", 16, "bold"), justify="left")
    econlabel.pack()  
    tk.mainloop()     


def macobj():
    #create window
    root = Tk()
    root.title("Macroeconomic Objectives")
    #create the text
    text1 = """Macroeconomic Objectives:
    - Sustainable economic growth
    - Low and stable inflation (in UK 2 percent)
    - Low unemployment (in UK <3 percent)
    - Avoid large trade deficit 
    - Low government borrowing to avoid debt 
    - Stable exchange rate
    - Low inequality
    - Protection of environment
    
    """
    #display the text
    econlabel = tk.Label(root, text= text1, font=("Arial", 16, "bold"), justify="left")
    econlabel.pack()  
    tk.mainloop()   


def fmpolicy():
    #create window
    root = Tk()
    root.title("Fiscal and Monetary Policy")
    #create the text
    text1 = """Fiscal Policy:
    - Involves government changing taxation and spending levels to influence AD and
      economic growth
    - Expansionary fiscal policy
        * Increasing AD and achieving economic growth
        * Cutting tax rates to encoruage spending
        * Increasing spending to increase AD but this can cause budget deficit
        * Can lead to demand pull inflation
    - Contractionary fiscal policy
        * Decreasing AD which lowers inflation but leads to negative economic growth
        * Cutting government spending and increasing tax rates which lowers consumer
          spending
        * Can improve government budget deficit
    
Monetary Policy:
    - Involves using interest rates and monetary tools such as quantative easing to
      influence AD levels and economic growth
    - Quantative easing involves the central bank buying governemnt bonds in order to 
      increase the money supply in banks to increase lending activities
    - Expansionary monetary policy
        * Cutting interest rates and therefore encouraging investment and consumer 
          spending in the economy and increase AD
        * Increasing quantative easing which menas more lending activity so more there
          is more investment in economy and increase AD
        * Leads to inflation
    - Contractionary monetary policy
        * Increasing interest rates to discourage spending and investment and therefore
          reduce AD but lower inflation
        * Quantative tightening to reduce money supply and lower economic activity and
          reduce AD but lower inflation

    
    """
    #display the text
    econlabel = tk.Label(root, text= text1, font=("Arial", 16, "bold"), justify="left")
    econlabel.pack()  
    tk.mainloop()  


def globalisation():
    #create window
    root = Tk()
    root.title("Globalisation")
    #create the text
    text1 = """Globalisation:
    - Integration of markets in the global economy
    - Increased interconnectedness of national economies
    - Increasing trade is liberalised and industries expand and 
      develop internationally

    """
    #display the text
    econlabel = tk.Label(root, text= text1, font=("Arial", 16, "bold"), justify="left")
    econlabel.pack()  
    tk.mainloop()     

  


def adv():
    #create window
    root = Tk()
    root.title("Absolute and Comparative Advantage")
    #create the text
    text1 = """Absolute Advantage:
    - Where one country can produce more goods with the same quantity of
      inputs compared to other economies
    - Fewer resources are needed to produce the same amount of goods and 
      there will be lower costs than other economies
    
Comparative Advantage:
    - Where one country can produce a goods at a lower oppurtunity cost
      than another country
    - Theoretically, countries should specialise in producing goods where
      they have a comparative advantage



    """
    #display the text
    econlabel = tk.Label(root, text= text1, font=("Arial", 16, "bold"), justify="left")
    econlabel.pack()  
    tk.mainloop()     



def bop():
    #create window
    root = Tk()
    root.title("Balance of Payments")
    #create the text
    text1 = """Balance of Payments:
    - Record of a country's international transactions
    - There are different accounts

Current Account:
    - Records balance of trade is goods and services
    - Records net primary and secondary income flows
 
Financial Account:
    - Records transactions for financial investment
    - Includes Direct and portfolio investment
    - Incldues short term monetary flows

Capital Account
    - Refers to transfer of funds related to buying fixed
      assets such as land

    """
    #display the text
    econlabel = tk.Label(root, text= text1, font=("Arial", 16, "bold"), justify="left")
    econlabel.pack()  
    tk.mainloop()  


#functions for the macroeconomics diagrams
def adasdiagram():
    root = tk.Toplevel()
    root.title("Aggregate Demand and Supply Diagram")

    #open the image using PIL
    image = Image.open("/Users/aviral/Downloads/adasdiagram.png")

    #resize the image to double its original size
    new_width = int(image.width*2)
    new_height = int(image.height*2)
    resized_image = image.resize((new_width, new_height))

    #resize image as it was too big 
    #Create a PhotoImage object from the resized image
    photo = ImageTk.PhotoImage(resized_image)

    #create a label to display the image
    label = tk.Label(root, image=photo)
    label.image = photo 
    label.pack()
    #tell user where diagram was taken from
    creditlabel = Label(root, text="Taken from https://www.economicshelp.org/blog/486/uncategorized/ad-as-diagrams/", font=("Arial", 10, "bold"), justify="left")
    creditlabel.pack()

    # Start the main event loop
    root.mainloop()


def lorenz():
    root = tk.Toplevel()
    root.title("Lorenz Curve")

    #open the image using PIL
    image = Image.open("/Users/aviral/Downloads/lorenz.png")

    #resize the image to double its original size
    new_width = int(image.width/2)
    new_height = int(image.height/2)
    resized_image = image.resize((new_width, new_height))

    #resize image as it was too big 
    #Create a PhotoImage object from the resized image
    photo = ImageTk.PhotoImage(resized_image)

    #create a label to display the image
    label = tk.Label(root, image=photo)
    label.image = photo 
    label.pack()
    #tell user where diagram was taken from
    creditlabel = Label(root, text="Taken from https://www.intelligenteconomist.com/gini-coefficient/", font=("Arial", 10, "bold"), justify="left")
    creditlabel.pack()

    # Start the main event loop
    root.mainloop()


def laffer():
    root = tk.Toplevel()
    root.title("Laffer Curve")

    #open the image using PIL
    image = Image.open("/Users/aviral/Downloads/laffer.png")

    #resize the image to double its original size
    new_width = int(image.width*2)
    new_height = int(image.height*2)
    resized_image = image.resize((new_width, new_height))

    #resize image as it was too big 
    #Create a PhotoImage object from the resized image
    photo = ImageTk.PhotoImage(resized_image)

    #create a label to display the image
    label = tk.Label(root, image=photo)
    label.image = photo 
    label.pack()

    #tell user where diagram was taken from
    creditlabel = Label(root, text="Taken from https://en.wikipedia.org/wiki/Laffer_curve", font=("Arial", 10, "bold"), justify="left")
    creditlabel.pack()

    # Start the main event loop
    root.mainloop()

#settings menu
def settings():
    # Create a list of color names to display in the dropdown box
    colors = ['maroon', 'green', 'blue', 'black', 'purple', 'orange']
    # Create a new Toplevel window
    root = tk.Toplevel(page)
    root.title("Settings")
    root.geometry("500x250")
    # Add a label to the window
    label = tk.Label(root, text="Change background color:")
    label.pack()
    #globalise the user choice variable
    global combobox
    # Create a dropdown box with the list of colors as options and add it to the window
    combobox = ttk.Combobox(root, values=colors)
    combobox.pack()
    #confirm choice button
    setbg=Button(root, text="SET", bg='white', fg='black', command=updatebg, font=("Comic Sans", 16))
    setbg.pack()
    #delete account button
    deleteacc=Button(root, text="Delete Account", bg='white', fg='black', command=deleteaccount, font=("Comic Sans", 16))
    deleteacc.pack()

def updatebg():
    # Update the background color of the main window
    page.configure(bg=combobox.get()) #update background colour of login/register page
    menuroot.configure(bg=combobox.get()) #update background colour of main menu page
    accountlabel.configure(background=combobox.get()) #update background colour of label on login/register page
    
def deleteaccount():
    #globalise user entries
    global ud_entry
    global user
    global pd_entry
    global password
    # creates new window for it
    new = Toplevel(page)
    user = StringVar()
    password = StringVar()
    #entry box to enter username
    ud_entry = tk.Entry(new, textvariable= user, show = '')
    pd_entry = StringVar()
    #entry box to enter password
    pd_entry = tk.Entry(new, textvariable= password, show = '*')
    #configure entry boxes
    ud_entry.grid(row=0, column=1)
    pd_entry.grid(row=1, column=1)
    # taking in username and password which is concealed when typed for security reasons
    tk.Label(new, text="Username", width="30").grid(row=0, column = 0)
    tk.Label(new, text="Password", width="30").grid(row=1, column = 0)
    sbmt = Button(new, text="Submit", command= confirmaccountdelete)
    # configuring dimensions of submission button
    sbmt.grid(row = 2, column = 0)

def confirmaccountdelete():
    global allow 
    #create a connection to database and cursor to excecute sql queries
    connection = sqlite3.connect("userdata.db")
    cursor = connection.cursor()
    cursor.execute("create table if not exists userdata (user text, pass text)")
    #select relevant rows where user name and password are of user input
    cursor.execute("delete from userdata where user = ? and pass = ?", (ud_entry.get(), pd_entry.get()))
    #commit the changes to the database
    connection.commit() 
    #get the number of rows affected
    rowsaffected = cursor.rowcount 
    if rowsaffected > 0: #if there are affected rows
        #displays a messagebox to show delete status
        messagebox.showinfo('info', 'Account deleted successfully')
    else:
        #displays a messagebox to show delete status
        messagebox.showinfo('info', 'Account entered invalid, please try again')
     


##### MAIN GUI
# main page window and add title
page = tk.Tk()
page.title('MY ACADEMIC PROGRESS TRACKER')
#choose background
colour = 'maroon'
page.configure(bg = colour)



# create a menubar
menubar = Menu(page)
page.configure(menu=menubar)


# create a menu
file_menu = Menu(menubar)


# add a exit to the menu
file_menu.add_command(
    label='Exit',
    command=page.quit
)


# button and labels for logging in
text = """ Welcome to your Academic Progress Tracker!

Please login to your account or create a new account by clicking register...

    """ #text for label 
accountlabel = tk.Label(page, text= text, bg=colour, font=("Arial", 24, "bold"))
accountlabel.pack()
btn=Button(page, text="LOGIN/SIGNUP", command = account_screen() , font=("Comic Sans", 30)).pack

#function the main menu gui
def mainmenu():
    #create a new window for menu
    global menuroot
    menuroot = Toplevel(page)
    menuroot.configure(bg = colour)

    # button for progress tracker
    ptbtn=Button(menuroot, text="PROGRESS TRACKER", bg = 'white', fg='black', command = pt , font=("Comic Sans", 30))
    ptbtn.place(x=80, y=100)
    ptbtn.config(height=4, width=20)
    ptbtn.pack(pady = 10) 

    # button for useful resources
    thingsbtn=Button(menuroot, text="USEFUL RESOURCES", bg = 'white', fg='black', command = ut , font=("Comic Sans", 30))
    thingsbtn.place(x=80, y=100)
    thingsbtn.config(height=4, width=20)
    thingsbtn.pack(pady = 10) 

    # button for revision material
    materialbtn=Button(menuroot, text="MY REVISION MATERIAL", bg = 'white', fg='black', command = material , font=("Comic Sans", 30))
    materialbtn.place(x=80, y=100)
    materialbtn.config(height=4, width=20)
    materialbtn.pack(pady = 10) 

    # button for exitting
    exitbtn=Button(menuroot, text="EXIT", bg = 'white', fg='black', command = exitconfirm , font=("Comic Sans", 30))
    exitbtn.place(x=80, y=100)
    exitbtn.config(height=4, width=20)
    exitbtn.pack(pady = 10) 

    # button for settings
    settingsbtn=Button(menuroot, text="Settings", bg = 'white', fg='black', command = settings , font=("Comic Sans", 30))
    settingsbtn.place(x=0)
    


# add the File menu to the menubar
menubar.add_cascade(
    label="File",
    menu=file_menu
)

# add a submenu
sub_menu = Menu(file_menu, tearoff=0)
sub_menu.add_command(label='My Progress Tracker', command=pt) #option to go to progress tracker
sub_menu.add_command(label='Useful Resources', command=ut) #option to go to useful resources
sub_menu.add_command(label='My Revision Material', command=material) #option to go to revision material
sub_menu.add_command(label='Settings', command= settings) #option to go to settings


# add the File menu to the menubar
file_menu.add_cascade(
    label="OPTIONS",
    menu=sub_menu
)


page.geometry("3000x2000+100+100")

page.mainloop()
