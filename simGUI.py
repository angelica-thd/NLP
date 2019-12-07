from Tkinter import *
import tkMessageBox


simple=Tk()
simple.title("Personality Trait Identification")
simple.geometry("1000x700")
simple.configure(bg="#FFFFFF")
inputxt=StringVar()
forum=StringVar()
user=StringVar()

l1 = Label(simple,bg="#FFFFFF",padx=20,text = "Choose your method to input text: ",font=("Ubuntu",20)).place(x=0,y=150)
personIcon = PhotoImage(file= "/home/angelica-theodorou/Documents/erasmus/NLP/personalitytraits.png")
icon = Label(simple,image=personIcon,bg="#FFFFFF").place(x=0,y=400)


l2 = Label(simple,text = "Enter Raw Text: ",font=("Ubuntu",20),bg="#FFFFFF",highlightbackground="#ba4a00",fg="#000000")
e1 = Entry(simple,font=("Ubuntu",15),textvariable=inputxt,bg="#FFFFFF",highlightbackground="#ba4a00")
l3 = Label(simple,text = "Enter Website Forum: ",font=("Ubuntu",20),bg="#FFFFFF",highlightbackground="#ba4a00")
e2 = Entry(simple, font=("Ubuntu",15),textvariable=forum,bg="#FFFFFF",highlightbackground="#ba4a00")
l4 = Label(simple,text = "Enter Username: ",font=("Ubuntu",20),bg="#FFFFFF",highlightbackground="#ba4a00")
e3 = Entry(simple, font=("Ubuntu",15),textvariable=user,bg="#FFFFFF",highlightbackground="#ba4a00")


def button3():
 	tkMessageBox.askokcancel("Are you sure?")

b3 = Button(simple,text="Submit",font=("Ubuntu",20), command=button3,height=1,bg="#ba4a00",\
	highlightbackground="#ba4a00",fg="#fff",activebackground="#fff",activeforeground="#ba4a00")

def button1():
	b3.place_forget()
	l3.place_forget()
	e2.place_forget()
	l4.place_forget()
	e3.place_forget()
	l2.place(x=500,y=50)
	e1.place(x=500,y=100)
	b3.place(x=500,y=150)


def button2():
	b3.place_forget()
	l2.place_forget()
	e1.place_forget()
	l3.place(x=500,y=400)
	e2.place(x=500,y=450)
	l4.place(x=500,y=500)
	e3.place(x=500,y=550)
	b3.place(x=500,y=600)
	

b1 = Button(simple,text="Raw User Text",font=("Ubuntu",20),command=button1,width= 20, height=1,bg="#ba4a00",\
	highlightbackground="#ba4a00",fg="#fff",activebackground="#fff",activeforeground="#ba4a00")
b1.place(x=500,y=3)
b2 = Button(simple,text="Text from a Website Forum User",font=("Ubuntu",20),command=button2,width=30,height=1,bg="#ba4a00",\
	highlightbackground="#ba4a00",fg="#fff",activebackground="#fff",activeforeground="#ba4a00")
b2.place(x=500,y=350)



simple.mainloop()
