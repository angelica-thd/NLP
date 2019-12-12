from Tkinter import *
from multiprocessing import Process, Manager
import tkMessageBox
import scraper


simple=Tk()
simple.title("Personality Trait Identification")
simple.geometry("1000x700")
simple.configure(bg="#FFFFFF")
keyword=StringVar()
subreddit=StringVar()
user=StringVar()

l1 = Label(simple,bg="#FFFFFF",padx=20,text = "Enter the information required: ",font=("Ubuntu",20)).place(x=0,y=150)
personIcon = PhotoImage(file= "/home/angelica-theodorou/Documents/erasmus/NLP/personalitytraits.png")
icon = Label(simple,image=personIcon,bg="#FFFFFF").place(x=0,y=400)


l2 = Label(simple,text = "Reddit Forum Subject: ",font=("Ubuntu",20),bg="#FFFFFF",highlightbackground="#ba4a00",fg="#000000")
e1 = Entry(simple,font=("Ubuntu",15),textvariable=subreddit,bg="#FFFFFF",highlightbackground="#ba4a00")
l3 = Label(simple,text = "Keyword for Search: ",font=("Ubuntu",20),bg="#FFFFFF",highlightbackground="#ba4a00")
e2 = Entry(simple, font=("Ubuntu",15),textvariable=keyword,bg="#FFFFFF",highlightbackground="#ba4a00")
l4 = Label(simple,text = "Username: ",font=("Ubuntu",20),bg="#FFFFFF",highlightbackground="#ba4a00")
e3 = Entry(simple, font=("Ubuntu",15),textvariable=user,bg="#FFFFFF",highlightbackground="#ba4a00")

def button3():

	if len(keyword.get()) == 0:
		tkMessageBox.showerror("WARNING","No keyword detected:\nPlease enter a keyword if you want to get results.")
	else:
		keyword.set(keyword.get().replace(' ','-'))
	 	if len(subreddit.get()) == 0:
	 		searchUrl = scraper.SITE_URL + 'search?q="'+ keyword.get() + '"'
	 	else:
	 		searchUrl = scraper.SITE_URL + 'r/' + subreddit.get() +'/search?q="'+ keyword.get() +'&restrict_sr=on'

	 	window = Toplevel(simple)
	 	window.geometry("1000x700")
		window.configure(bg="#FFFFFF")
		URLabel = Label(window,font=("Ubuntu",20),bg="#FFFFFF",highlightbackground="#ba4a00",fg="#000000")
		postLabel = Label(window,font=("Ubuntu",15),bg="#FFFFFF",highlightbackground="#ba4a00",fg="#000000")
		resultsLabel = Label(window,font=("Ubuntu",11),bg="#FFFFFF",highlightbackground="#ba4a00",fg="#000000")
	 	
	 	product= {}
	 	URLabel.configure(text = "Search URL: "+ searchUrl)
	 	URLabel.place(x=0,y=50)
	 	posts = scraper.getSearchResults(searchUrl)
	 	postLabel.configure(text = "Scraping "+str(len(posts))+" posts.")
	 	postLabel.place(x=0,y=100)
	 	
	 	product[keyword.get()] = {}
	 	product[keyword.get()]['subreddit'] ='all' if len(subreddit.get()) == 0 else subreddit.get()
	 	results = Manager().list()
	 	opers = []
	 	for post in posts:
	 		oper = Process(target = scraper.parsePost, args=(post,results))
	 		opers.append(oper)
	 		oper.start()
	 	for oper in opers:
	 		oper.join()
	 	product[keyword.get()]['posts'] = list(results)
	 	postList = product[keyword.get()]['posts']
	 	for i in range(0,9):
	 		resultsLabel.configure(text = str(postList[i])+ "\n")
	 	resultsLabel.place(x=0, y=150)
	 	#resultsLabel.configure( text =  "RESULTS:\n" + product[keyword.get()]['posts'])



b3 = Button(simple,text="Submit",font=("Ubuntu",20), command=button3,height=1,bg="#ba4a00",\
	highlightbackground="#ba4a00",fg="#fff",activebackground="#fff",activeforeground="#ba4a00")

def button1():
	b3.place_forget()
	l4.place_forget()
	e3.place_forget()
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
	b3.place(x=500,y=600)
	

b1 = Button(simple,text="Reddit Forum and Keyword",font=("Ubuntu",20),command=button1,width= 30, height=1,bg="#ba4a00",\
	highlightbackground="#ba4a00",fg="#fff",activebackground="#fff",activeforeground="#ba4a00")
b1.place(x=500,y=3)
b2 = Button(simple,text="Reddit Forum and User",font=("Ubuntu",20),command=button2,width=30,height=1,bg="#ba4a00",\
	highlightbackground="#ba4a00",fg="#fff",activebackground="#fff",activeforeground="#ba4a00")
b2.place(x=500,y=350)

simple.mainloop()



