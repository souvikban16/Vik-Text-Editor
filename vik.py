import os 
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import simpledialog
import re

class Menubar:

	def __init__(self, parent):
		menubar = tk.Menu(parent.master)
		parent.master.config(menu =menubar)
		menubar.add_command(label = "New", command = parent.newFile)
		menubar.add_command(label = "Save", command = parent.saveFile)
		menubar.add_command(label = "Save As", command = parent.saveAsFile)
		menubar.add_command(label = "Open", command = parent.openFile)
		menubar.add_command(label = "About", command = parent.showAbout)
		menubar.add_command(label = "Change Font size", command = parent.changeFontSize)
		menubar.add_separator()
		menubar.add_separator()
		menubar.add_separator()
		menubar.add_command(label = "CMD", command = parent.openCMD)
		menubar.add_command(label = "Build", command = parent.buildFile)
		menubar.add_command(label = "Run", command = parent.runFile)

class Vik:

	def __init__(self, master):
		master.title("Untitled -- Vik Text Editor")
		master.geometry("500x500")

		self.master = master
		self.filepath = None
		self.filename = None
		self.filenameonly = None
		self.cwd = None
		self.filetype = None
		self.fontsize = 18
		self.current_indent = 0
		self.textArea = tk.Text(master, font =("Consolas", self.fontsize), bg = "black", fg = "grey", insertbackground = "yellow", padx = "20", pady = "20", spacing1 = self.fontsize * 0.60+ 2)
		self.scrollBarY = tk.Scrollbar(master, command = self.textArea.yview)
		# self.scrollBarX = tk.Scrollbar(master, command = self.textArea.xview)
		self.textArea.configure(yscrollcommand = self.scrollBarY.set)
		# self.textArea.configure(xscrollcommand = self.scrollBarX.set)
		self.textArea.pack(side = tk.LEFT,  fill = tk.BOTH, expand = True)
		self.scrollBarY.pack(side = tk.RIGHT, fill = tk.Y)
		# self.scrollBarX.pack(side = tk.BOTTOM, fill = tk.X)

		self.menu = Menubar(self)

		#keyboard binds
		self.textArea.bind("<KeyRelease-BackSpace>",self.counttabs)
		self.textArea.bind("<Return>", self.indent)
		self.textArea.bind("<Tab>",self.counttabsTab)
		self.textArea.bind("<Control-s>", self.saveFileShortcut)


	def newFile(self):

		if self.filepath:
			original = ""
			with open(self.filepath, "r") as file:
				original = file.read()
			current = self.textArea.get(1.0, tk.END) 
			if original == current:
				print("They are the same")
				self.filepath = None
				self.filename = None
				self.filetype = None
				self.filenameonly = None
				self.master.title("Untitled -- Vik Text Editor")
				self.textArea.delete(1.0, tk.END)
				return
			result = messagebox.askyesnocancel(title = "Alert!", message = "Save File first ? ")
			print(result)
			if result == None:
				return
			elif result == True:
				self.saveFile()
				self.filepath = None
				self.filename = None
				self.filetype = None
				self.filenameonly = None
				self.master.title("Untitled -- Vik Text Editor")
				self.textArea.delete(1.0, tk.END)
			elif result == False:
				self.filepath = None
				self.filename = None
				self.filetype = None
				self.filenameonly = None
				self.master.title("Untitled -- Vik Text Editor")
				self.textArea.delete(1.0, tk.END)
		else:
			textAreaContent = self.textArea.get(1.0, tk.END)
			print(len(textAreaContent))
			if len(textAreaContent) > 1:
				result = messagebox.askyesnocancel(title = "Alert!", message = "Save Current File ? ")
				if result == True:
					self.saveFile()
					self.filepath = None
					self.filename = None
					self.filetype = None
					self.filenameonly = None
					self.master.title("Untitled -- Vik Text Editor")
					self.textArea.delete(1.0, tk.END)
				elif result == False:
					self.filepath = None
					self.filename = None
					self.filetype = None
					self.filenameonly = None
					self.master.title("Untitled -- Vik Text Editor")
					self.textArea.delete(1.0, tk.END)
				elif result == None:
					return
				
			self.filepath = None
			self.filename = None
			self.filetype = None
			self.filenameonly = None
			self.master.title("Untitled -- Vik Text Editor")
			self.textArea.delete(1.0, tk.END)
	def saveFileShortcut(self, event):
		self.saveFile()
                
	def saveFile(self):
		if not self.filepath:
			self.saveAsFile()
		else:
			textAreaContent = self.textArea.get(1.0, tk.END)
			with open(self.filepath, "w") as f:
				f.write(textAreaContent)
			messagebox.showinfo("Alert!", message = "File Saved Successfully")


	def saveAsFile(self):
		self.filepath = filedialog.asksaveasfilename(defaultextension = "*.*")
		if self.filepath:
			textAreaContent = self.textArea.get(1.0, tk.END)
			with open(self.filepath, "w") as f:
				f.write(textAreaContent)
			self.master.title(self.filepath + " -- Vik Text Editor")
			index = self.filepath.rfind("/")
			self.filename = self.filepath[index + 1 :]
			self.cwd = self.filepath[:index]
			dotindex = self.filepath.rfind(".")
			self.filetype = self.filepath[dotindex + 1 :]
			self.filenameonly = self.filepath[index + 1:dotindex]
			messagebox.showinfo("Alert!", message = "File Saved Successfully")

	def openFile(self):
		if self.filepath:
			result = messagebox.askyesnocancel(title = "Alert!", message = "Save Current File ? ")
			if result == True:
				self.saveFile()
				self.filepath = filedialog.askopenfilename(defaultextension = "*.*")
				print(self.filepath)
				if self.filepath:
					self.textArea.delete(1.0, tk.END)
					with open(self.filepath, "r") as file:
						self.textArea.insert(1.0, file.read())
					self.master.title(self.filepath + " -- Vik Text Editor")
					index = self.filepath.rfind("/")
					self.filename = self.filepath[index + 1 :]
					self.cwd = self.filepath[:index]
					dotindex = self.filepath.rfind(".")
					self.filetype = self.filepath[dotindex + 1 :]
					self.filenameonly = self.filepath[index + 1:dotindex]
					print(self.filepath)
					print(self.cwd)
					print(self.filename)
					print(self.filetype)

			elif result == False:
				self.filepath = filedialog.askopenfilename(defaultextension = "*.*")
				print(self.filepath)
				if self.filepath:
					self.textArea.delete(1.0, tk.END)
					with open(self.filepath, "r") as file:
						self.textArea.insert(1.0, file.read())
					self.master.title(self.filepath + " -- Vik Text Editor")
					index = self.filepath.rfind("/")
					self.filename = self.filepath[index + 1 :]
					self.cwd = self.filepath[:index]
					dotindex = self.filepath.rfind(".")
					self.filetype = self.filepath[dotindex + 1 :]
					self.filenameonly = self.filepath[index + 1:dotindex]
					print(self.filepath)
					print(self.cwd)
					print(self.filename)
					print(self.filetype)
			elif result == None:
				return
		else:

			self.filepath = filedialog.askopenfilename(defaultextension = "*.*")
			print(self.filepath)
			if self.filepath:
				self.textArea.delete(1.0, tk.END)
				with open(self.filepath, "r") as file:
					self.textArea.insert(1.0, file.read())
				self.master.title(self.filepath + " -- Vik Text Editor")
				index = self.filepath.rfind("/")
				self.filename = self.filepath[index + 1 :]
				self.cwd = self.filepath[:index]
				dotindex = self.filepath.rfind(".")
				self.filetype = self.filepath[dotindex + 1 :]
				self.filenameonly = self.filepath[index + 1:dotindex]
				print(self.filepath)
				print(self.cwd)
				print(self.filename)
				print(self.filetype)


	def showAbout(self):
		messagebox.showinfo(title = "About Vik Text Editor", message = "I am Souvik Banerjee and I have made this editor for fun!")
		
	def openCMD(self):
		if not self.filepath:
			messagebox.showerror(title = "Alert!", message = "Save file first!")
		else:
			os.system("start cmd /k cd /d " + self.cwd)
	def buildFile(self):
		if not self.filepath:
			messagebox.showerror(title = "Alert!", message = "Save file first!")
		else:
			if self.filetype == "py":
				temp = 'start cmd /k \"cd /d '+ self.cwd + ' && python ' + self.filename +"\""
				os.system(temp)
			elif self.filetype == "cpp":
				temp = 'start cmd /k \"cd /d '+ self.cwd + ' && g++ ' + self.filename + " -o " + self.filenameonly + "\""
				os.system(temp)
				print(temp)
			elif self.filetype == "c":
				temp = 'start cmd /k \"cd /d '+ self.cwd + ' && gcc ' + self.filename + " -o " + self.filenameonly + "\""
				os.system(temp)
				print(temp)
			elif self.filetype == "java":
				temp = 'start cmd /k \"cd /d '+ self.cwd + ' && javac ' + self.filename + "\""
				os.system(temp)
				print(temp)

	def runFile(self):
		if not self.filepath:
			messagebox.showerror(title = "Alert!", message = "Save file first!")
		else:
			if self.filetype == "py":
				temp = 'start cmd /k \"cd /d '+ self.cwd + ' && python ' + self.filename +" \""
				os.system(temp)
			elif self.filetype == "cpp":
				temp  = 'start cmd /k \"cd /d '+ self.cwd + ' && ' + self.filenameonly +"\""
				os.system(temp)
			elif self.filetype == "c":
				temp  = 'start cmd /k \"cd /d '+ self.cwd + ' && ' + self.filenameonly +"\""
				os.system(temp)
			elif self.filetype == "java":
				result = simpledialog.askstring("Input", "Enter the class name with the main method")
				temp = 'start cmd /k \"cd /d '+ self.cwd + ' && java ' + result + "\""
				os.system(temp)
				print(temp)
	def changeFontSize(self):
		self.fontsize = simpledialog.askinteger("Input", "Enter font size")
		self.textArea.config(font = ("Consolas",self.fontsize), spacing1 = self.fontsize * 0.60 + 2)


	def counttabs(event, self):
	    # the text widget that received the event
	    # widget = event.widget

	    # get current line
	    line = event.textArea.get("insert linestart", "insert lineend")

	    # compute the indentation of the current line
	    match = re.match(r'^(\s+)', line)
	    # global current_indent
	    event.current_indent = len(match.group(0)) if match else 0
	    print(event.current_indent,1)

	def counttabsTab(event, self):
	    
	    #first inserting a tab
	    event.textArea.insert(tk.INSERT, "\t")
	    # the text widget that received the event
	    # widget = event.widget

	    # get current line
	    line = event.textArea.get("insert linestart", "insert lineend")

	    # compute the indentation of the current line
	    match = re.match(r'^(\s+)', line)
	    # global current_indent
	    event.current_indent = len(match.group(0)) if match else 0
	    print(event.current_indent,1)
	    return 'break'

	def indent(event, self ):
	    print (event.current_indent,1)
	    event.textArea.insert(tk.INSERT, "\n")
	    event.textArea.insert(tk.INSERT, event.current_indent * "\t")
	    return 'break'





if __name__ == "__main__":
	master = tk.Tk()
	#master.iconbitmap('v.ico')
	vik = Vik(master)
	master.mainloop()

