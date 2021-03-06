from tkinter import *
from multiprocessing import Process, Manager
#import tkMessageBox
import scraper
import os
import wordnet_sim as ws

simple=Tk()
simple.title("Personality Trait Identification")
simple.geometry("1000x700")
simple.configure(bg="#FFFFFF")
simple.resizable(True,True)
keyword=StringVar()
subreddit=StringVar()
user=StringVar()
searchUrl =StringVar()
SITE_URL = 'https://old.reddit.com/'
postNum = 0
path = os.path.abspath(os.getcwd())

l1 = Label(simple,bg="#FFFFFF",padx=20,text = "Enter the information required: ",font=("Ubuntu",20)).place(x=0,y=150)
personIcon = PhotoImage(file= path+"/personalityTraits.png")
icon = Label(simple,image=personIcon,bg="#FFFFFF").place(x=0,y=400)


l2 = Label(simple,text = "Reddit Forum Subject: ",font=("Ubuntu",20),bg="#FFFFFF",highlightbackground="#ba4a00",fg="#000000")
e1 = Entry(simple,font=("Ubuntu",15),textvariable=subreddit,bg="#FFFFFF",highlightbackground="#ba4a00")
l3 = Label(simple,text = "Keyword for Search: ",font=("Ubuntu",20),bg="#FFFFFF",highlightbackground="#ba4a00")
e2 = Entry(simple, font=("Ubuntu",15),textvariable=keyword,bg="#FFFFFF",highlightbackground="#ba4a00")
l4 = Label(simple,text = "Username: ",font=("Ubuntu",20),bg="#FFFFFF",highlightbackground="#ba4a00")
e3 = Entry(simple, font=("Ubuntu",15),textvariable=user,bg="#FFFFFF",highlightbackground="#ba4a00")

def createWindow(score_list):
	window = Toplevel(simple)
	window.geometry("1000x700")
	window.configure(bg="#FFFFFF")
	#this doesnt work perfectly, will fix later
	subjectLabel = Label(window,font=("Ubuntu",20),bg="#FFFFFF",highlightbackground="#ba4a00",fg="#000000")
	if subreddit.get()!=0:
		subjectLabel.configure(text = 'Subject: "'+ subreddit.get() +'"')
	else: subjectLabel.configure(text = "Subject: None")
	subjectLabel.place(x=0,y=50)
	keywordLabel = Label(window,font=("Ubuntu",20),bg="#FFFFFF",highlightbackground="#ba4a00",fg="#000000")
	if keyword.get()!=0:
		keywordLabel.configure(text = 'Keyword: "'+ keyword.get() +'"')
	else: keywordLabel.configure(text = 'Keyword: None')
	keywordLabel.place(x = 0,y =100)
	userLabel = Label(window,font=("Ubuntu",20),bg="#FFFFFF",highlightbackground="#ba4a00",fg="#000000")
	if user.get()!=0:
		userLabel.configure(text = 'Username: "'+ user.get() +'"')
	else: userLabel.configure(text = 'Username: None')
	userLabel.place(x=0,y=150)
	scoreLabel = Label(window,font=("Ubuntu",20),bg="#FFFFFF",highlightbackground="#ba4a00",fg="#000000")
	scoreLabel.configure(text = "Similarity score: \n          Openness: " + str(score_list[0]) + "% \n                   Conscientiousness: "+ str(score_list[1]) + "% \n              Extraversion: "+ str(score_list[2]) + "% \n               Agreeableness: "+ str(score_list[3]) + "% \n            Neuroticism: "+ str(score_list[4]) +"%" )
	scoreLabel.place(x =0, y =200)
	#postLabel = Label(window,font=("Ubuntu",20),bg="#FFFFFF",highlightbackground="#ba4a00",fg="#000000")
	#postLabel.configure(text = "Scraping...%s posts." % postNum)
	#postLabel.place(x=0,y=100)
	
	

def submitKey():
	username = None
	if len(keyword.get()) == 0:
		#for python3
		tkmessagebox.showerror("WARNING","No keyword detected:\nPlease enter a keyword if you want to get results.")		
		#tkMessageBox.showerror("WARNING","No keyword detected:\nPlease enter a keyword if you want to get results.")
	else:
		keyword.set(keyword.get().replace(' ','-'))
		key = keyword.get()
		if len(subreddit.get()) == 0:
	 		searchUrl = SITE_URL + 'search?q="'+ keyword.get() + '"'
	 		sub = None
		else:
			subreddit.set(subreddit.get().replace(' ',''))
			sub = subreddit.get()
			searchUrl = SITE_URL + 'r/' + sub +'/search?q="'+ key +'&restrict_sr=on'	
	postlist = scraper.returnResults(searchUrl,key,sub,username)
	temp = ws.preprocess(postlist)
	score_list = ws.similarity(temp)
	print(score_list)
	#postNum = str(len(postlist)) 
	createWindow(score_list)
	
		
def submitUser():
	if len(subreddit.get()) == 0:
		#for python3
		tkmessagebox.showerror("WARNING","No reddit Forum detected:\nPlease enter a reddit forum(subject) if you want to get results.")
		#tkMessageBox.showerror("WARNING","No reddit Forum detected:\nPlease enter a reddit forum(subject) if you want to get results.")
	else:
		subreddit.set(subreddit.get().replace(' ','-'))
		sub = None
		key = subreddit.get()
		searchUrl = SITE_URL + 'search?q="' + key +'"'
	username = user.get()
	postlist = scraper.returnResults(searchUrl,key,sub,username)
	#postNum = str(len(postlist))
	temp = ws.preprocess(postlist)
	score_list = ws.similarity(temp)
	print(score_list)
	createWindow(score_list)

		


b3 = Button(simple,text="Submit",font=("Ubuntu",20), command=submitKey,height=1,bg="#ba4a00",\
	highlightbackground="#ba4a00",fg="#fff",activebackground="#fff",activeforeground="#ba4a00")
b4 = Button(simple,text="Submit",font=("Ubuntu",20), command=submitUser,height=1,bg="#ba4a00",\
	highlightbackground="#ba4a00",fg="#fff",activebackground="#fff",activeforeground="#ba4a00")


def button1():
	b3.place_forget()
	l4.place_forget()
	e3.place_forget()
	b4.place_forget()
	l2.place(x=500,y=50)
	e1.place(x=500,y=100)
	l3.place(x=500,y=150)
	e2.place(x=500,y=200)
	b3.place(x=500,y=250)


def button2():
	b3.place_forget()
	l2.place_forget()
	e1.place_forget()
	l3.place_forget()
	e2.place_forget()
	l2.place(x=500,y=400)
	e1.place(x=500,y=450)
	l4.place(x=500,y=500)
	e3.place(x=500,y=550)
	b4.place(x=500,y=600)
	

b1 = Button(simple,text="Reddit Forum and Keyword",font=("Ubuntu",20),command=button1,width= 30, height=1,bg="#ba4a00",\
	highlightbackground="#ba4a00",fg="#fff",activebackground="#fff",activeforeground="#ba4a00")
b1.place(x=500,y=3)
b2 = Button(simple,text="Reddit Forum and User",font=("Ubuntu",20),command=button2,width=30,height=1,bg="#ba4a00",\
	highlightbackground="#ba4a00",fg="#fff",activebackground="#fff",activeforeground="#ba4a00")
b2.place(x=500,y=350)

simple.mainloop()



