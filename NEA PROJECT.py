# importing all libraries
from distutils import command
from email.mime import image
from genericpath import exists
from logging import root
from pydoc import text
import tkinter as tk
from tkinter.tix import ROW
from tkinter.ttk import Label
from tkinter import messagebox
from functools import partial
from tkinter import *
from turtle import ScrolledCanvas, right
import mysql.connector
import sqlite3
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd



#database creation

connection = sqlite3.connect("userdata.db")
cursor = connection.cursor()
cursor.execute("create table if not exists userdata (user text, pass text)")


connection.commit() #store all the rows permanently inside "userdata.db", 
                    #otherwise you might have trouble selecting from external files


for row in cursor.execute("select distinct * from userdata"):
    print(row)


connection1 = sqlite3.connect("userdata.db")
cursor1 = connection1.cursor()



print ("**********************")

cursor.execute("select distinct * from userdata where user=:u", {"u": "aviral"} )
userdata_search = cursor.fetchall()
print(userdata_search)

print("***********************")


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
 
    # create a Form label 
    Label(text="You must Login or Register!", bg="maroon", width="300", height="3", font=("Calibri", 13)).pack() 

    # create Login Button 
    Button(text="Login", height="2", width="30", command=login).pack() 
    Label(text="").pack() 

    # create a register button
    Button(text="Register", height="2", width="30", command=register).pack()
    


def login():
    global userentry
    global user
    global passwordentry
    global password
    # right now incomplete- once database is set up I will cross check login details to it
    new = Toplevel(page)
    # creates new window for it
    user = StringVar()
    userentry = tk.Entry(new, textvariable= user, show = '')
    password = StringVar()
    passwordentry = tk.Entry(new, textvariable= password, show = '*')
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
    connection = sqlite3.connect("userdata.db")
    cursor = connection.cursor()
    cursor.execute("create table if not exists userdata (user text, pass text)")
    cursor.execute("select * from userdata where user = ? and pass = ?", (userentry.get(), passwordentry.get()))
    row = cursor.fetchall() #fetches all (or all remaining) rows of a query result set 
    if row:
        #displays a messagebox to show login status
        messagebox.showinfo('info', 'Login Successful')
        allow = '1'
    else:
        #displays a messagebox to show login status

        messagebox.showinfo('info', 'Incorrect login, please try again')
        allow = '0'


def register():
    # right now incomplete as need to submit details to a database
    new = Toplevel(page)
    # creates new window for it
    global userentry
    global user
    global passwordentry
    global password
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

    connection = sqlite3.connect("userdata.db")
    cursor = connection.cursor()
    cursor.execute("create table if not exists userdata (user text, pass text)")

    connection = sqlite3.connect("userdata.db")
    cursor = connection.cursor()
    cursor.execute("create table if not exists userdata (user text, pass text)")
    cursor.execute("select * from userdata where user = ? and pass = ?", (userentry.get(), passwordentry.get()))
    row = cursor.fetchall() #fetches all (or all remaining) rows of a query result set 

    if row:
        messagebox.showinfo('info', 'Username already exists, try again')

    else:
        u = userentry.get()
        p = passwordentry.get()

        query = "insert into userdata values(?,?)"
        info_list=(str(u), str(p))
        connection.execute(query,info_list)
        
        connection.commit()

        for row in cursor.execute("select distinct * from userdata"):
            print(row)



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
    new.title("New Window")
 
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

    g = grade.get()
    u = user.get()
    c = confidence.get()
    a = attempt.get()
    s = score.get()
    pr = predict.get()
    sb = subject.get()

    query = "insert into Trackers (user, score, predict, grade, attempt,confidence,subject) VALUES (?,?,?,?,?,?,?)"
    info_list=(str(u), float(s), str(pr), str(g), int(a), int(c), str(sb))
    cursor.execute(query,info_list)

    connection.commit()

    for row in cursor.execute("select distinct * from Trackers"):
        print(row)

def subjectchoice():
    global sbc
    sbc = sbchoice.get()

def ptshow():
    try:
        connection = sqlite3.connect('Trackers.db')
        cursor = connection.cursor()

        cursor.execute("select * from Trackers")
        list = cursor.fetchall()
        print("Total rows are:  ", len(list))
        print("Printing each row")

        for row in list:
            print("User: ", row[0])
            print("Score: ", row[1])
            print("Predicted Grade: ", row[2])
            print("Grade: ", row[3])
            print("Attempt: ", row[4])
            print("Confidence: ", row[5])
            print("Subject: ", row[6])

            print("\n")

    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if connection:
            connection.commit()

    mydb = sqlite3.connect('Trackers.db')
    mycursor = mydb.cursor()
    u = user.get()

    # Fecthing Data From mysql to my python progame
    mycursor.execute("SELECT * FROM Trackers WHERE user=:u AND subject=:sb", {"u": u, "sb": sbc})  
    result = mycursor.fetchall()
    print("RESULT",result)
    
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
    mydb = sqlite3.connect('Trackers.db')
    cursor = mydb.cursor()
    u = user.get()
    sbc = sbchoice.get()

    # Fecthing Data From mysql to my python progame
    cursor.execute("SELECT * FROM Trackers WHERE user=:u and subject=:sbc", {"u": u, "sbc": sbc})
    result = cursor.fetchall()
    print("RESULT",result)
    
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

    print("Score = ", score)
    print("Attempts = ", attempt)
    print("Confidence = ", confidence)

    #convert database into pandasdataframe
    df = pd.read_sql(f"select score, attempt, confidence from Trackers where user='{u}' and subject ='{sbc}'", mydb)
    df['attempt']=df['attempt'].astype(int)
    df['score']=df['score'].astype(float)
    df['confidence']=df['confidence'].astype(float)
    print (df.dtypes)
    #plotting graph
    df.plot(x = "attempt" ,y= "confidence" ,kind = "line", ylim=(0,10), ylabel = "Confidence", xlabel = "Attempt")

    plt.show()
   

def allprogressdata():
    u = user.get()
    mydb = sqlite3.connect('Trackers.db')
    mycursor = mydb.cursor()
    w = tk.Tk()
    w.geometry("400x250") 
    w.configure(bg = 'maroon')
    w.title("MY PROGRESS DATA")
    #using tkinter to print labels with database rows
    rows = mycursor.execute("SELECT score, predict, grade, attempt, confidence, subject from Trackers where user=:u", {"u": u})  
    tk.Label(w, text="Score %, Grade, Predicted Grade, Attempt/Test Number, Confidence Level \n", bg = "maroon" , width = 100, font = ("Arial", 30)).pack()

    for row in rows:
        tk.Label(w, text=row, width = 100, bg = "maroon" , font = ("Arial", 30)).pack()

def openpt():
    if allow == '1':
        ptshow()
    else:
        messagebox.showinfo('info', 'Incorrect login, can not access progress tracker')

def openpt1():
    if allow == '1':
        graph1()
    else:
        messagebox.showinfo('info', 'Incorrect login, can not access progress tracker')

def openpt2():
    if allow == '1':
        allprogressdata()
    else:
        messagebox.showinfo('info', 'Incorrect login, can not access progress tracker')





def ut():
    win = tk.Tk()
    win.geometry("400x250") 
    win.configure(bg = 'maroon')
    win.title("USEFUL RESOURCES")
    








##### GUI
# page window
page = tk.Tk()
page.title('MY ECONOMICS PROGRESS TRACKER')


#test scores in file input NEED TO COMPLETE

def file1():
    entry = tk.Entry(page)
    x = entry.get()

#opening windows
def open_window():
   new = Toplevel(page)
   new.geometry("750x250")
   new.title("New Window")
   #Create a Label in New window
   x = Label(new, text = "My Economics Progress Tracker", command = file1)
   x.pack()


# create a menubar
menubar = Menu(page)
page.configure(menu=menubar, bg = 'maroon')


# create a menu
file_menu = Menu(menubar)

# add a menu item to the menu
file_menu.add_command(
    label='Exit',
    command=page.quit
)

# button for logging in
btn=Button(page, text="LOGIN/SIGNUP", bg = 'white', fg='black', command = account_screen() , font=("Comic Sans", 30)).pack


# button for progress tracker
ptbtn=Button(page, text="PROGRESS TRACKER", bg = 'white', fg='black', command = pt , font=("Comic Sans", 30))
ptbtn.place(x=80, y=100)
ptbtn.config(height=4, width=20)
ptbtn.pack() 

# button for useful things
thingsbtn=Button(page, text="USEFUL THINGS", bg = 'white', fg='black', command = ut , font=("Comic Sans", 30))
thingsbtn.place(x=80, y=100)
thingsbtn.config(height=4, width=20)
thingsbtn.pack() 

# button for revision material
materialbtn=Button(page, text="MY REVISION MATERIAL", bg = 'white', fg='black', command = pt , font=("Comic Sans", 30))
materialbtn.place(x=80, y=100)
materialbtn.config(height=4, width=20)
materialbtn.pack() 

# button for exitting
exitbtn=Button(page, text="EXIT", bg = 'white', fg='black', command = exitconfirm , font=("Comic Sans", 30))
exitbtn.place(x=80, y=100)
exitbtn.config(height=4, width=20)
exitbtn.pack() 

# add the File menu to the menubar
menubar.add_cascade(
    label="File",
    menu=file_menu
)
# add a submenu
sub_menu = Menu(file_menu, tearoff=0)
sub_menu.add_command(label='My Progress Tracker', command=pt)
sub_menu.add_command(label='Useful Things', command=pt)
sub_menu.add_command(label='My Revision Material', command=pt)

# add the File menu to the menubar
file_menu.add_cascade(
    label="OPTIONS",
    menu=sub_menu
)




page.geometry("3000x2000+100+100")

page.mainloop()
