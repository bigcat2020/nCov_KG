from tkhtml import MainFrame
from cefpython3 import cefpython as cef
import tkinter as tk
import tkinter.messagebox
import sys

class GUI(tk.Tk):
	def __init__(self,url):
		self.url = url
		self.window = tk.Tk()
		self.var_situation = tk.StringVar()
		self.var_start_time = tk.StringVar()
		self.var_end_time = tk.StringVar()
		self.on_hit = False
		self.set_window()
		self.set_menubar()
		self.set_searchbar()
		self.set_display()
		self.window.mainloop()


	def set_display(self):
		frame = tk.Frame(self.window)
		frame.pack(anchor='nw', padx=20,pady=80,side='top', fill='both', expand=True)
		app = MainFrame(frame,self.url)
		app.pack(anchor='nw',side='top', fill='both', expand=True)
		frm = tk.Frame(self.window)
		frm.pack()
		foot = tk.Label(frame,text='Update:2020/02/29\t knowledgeGraph count: xxxxthins,xxxxrelations,xxxxattribute')
		foot.pack()

	def Search(self):
		if not self.on_hit:
			self.no_hit = True
			tk.messagebox.showinfo(title='Search',
				message='Search about '+str(self.var_situation.get())\
				+' in '+str(self.var_start_time.get())\
				+' to '+str(self.var_end_time.get()))
		else:
			on_hit = False

	def set_searchbar(self):
		l1 = tk.Label(self.window,text='Keywords')
		l1.place(x=20,y=20,anchor='nw')
		l2 = tk.Label(self.window,text='knowledgeGraph about "situation",time start to time end')
		l2.place(x=20,y=50,anchor='nw')
		e1 = tk.Entry(self.window,textvariable=self.var_situation)
		e1.place(x=90,y=20,anchor='nw')
		l3 = tk.Label(self.window,text='Search Time')
		l3.place(x=260,y=20,anchor='nw')
		e2 = tk.Entry(self.window,textvariable=self.var_start_time,width=10)
		e2.place(x=340,y=20,anchor='nw')
		l4 = tk.Label(self.window,text='-')
		l4.place(x=420,y=20,anchor='nw')
		e3 = tk.Entry(self.window,textvariable=self.var_end_time,width=10)
		e3.place(x=440,y=20,anchor='nw')
		b1 = tk.Button(self.window,text='Search',font=('Arial',7),command=self.Search)
		b1.place(x=530,y=20,anchor='nw')

	def set_menubar(self):
		menubar = tk.Menu(self.window)
		filemenu = tk.Menu(menubar,tearoff=0)
		menubar.add_cascade(label='File',menu=filemenu)
		filemenu.add_command(label='New',command='')
		filemenu.add_command(label='Open',command='')
		filemenu.add_command(label='Save',command='')
		chose = tk.Menu(filemenu,tearoff=0)
		filemenu.add_cascade(label='Chose',menu=chose)
		chose.add_command(label='Chose1',command='')
		chose.add_command(label='Chose2',command='')
		filemenu.add_separator()
		filemenu.add_command(label='Exit',command=self.window.quit)
		editfile = tk.Menu(menubar,tearoff=0)
		menubar.add_cascade(label='Edit',menu=editfile)
		editfile.add_command(label='Cut',command='')
		editfile.add_command(label='Copy',command='')
		editfile.add_command(label='Paste',command='')
		self.window.config(menu = menubar)

	def set_window(self):
		self.window.title('2019nCov')
		self.window.geometry('800x450')
		self.window.config(background = '#DADADA')

	def tkhtml(self):
		sys.excepthook = cef.ExceptHook
		cef.Initalize()


if __name__ == '__main__':
	cef.Initialize()
	GUI("world.html")
	cef.Shutdown()

