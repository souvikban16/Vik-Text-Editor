import os 
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

class Menubar:

	def __init__(self, parent):
		menubar = tk.Menu(parent.master)
		parent.master.config(menu =menubar)
		menubar.add_command(label = "New", command = parent.newFile)
		menubar.add_command(label = "Save", command = parent.saveFile)
		menubar.add_command(label = "Save As", command = parent.saveAsFile)
		menubar.add_command(label = "Open", command = parent.openFile)
		menubar.add_command(label = "About", command = parent.showAbout)
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
		self.textArea = tk.Text(master)
		self.scrollBarY = tk.Scrollbar(master, command = self.textArea.yview)
		# self.scrollBarX = tk.Scrollbar(master, command = self.textArea.xview)
		self.textArea.configure(yscrollcommand = self.scrollBarY.set)
		# self.textArea.configure(xscrollcommand = self.scrollBarX.set)
		self.textArea.pack(side = tk.LEFT,  fill = tk.BOTH, expand = True)
		self.scrollBarY.pack(side = tk.RIGHT, fill = tk.Y)
		# self.scrollBarX.pack(side = tk.BOTTOM, fill = tk.X)

		self.menu = Menubar(self)

	def newFile(self):

		if self.filepath:
			result = messagebox.askyesnocancel(title = "Alert!", message = "Save File first ? ")
			print(result)
			if result == None:
				return
			elif result == True:
				print("saved")
		self.filepath = None
		self.filename = None
		self.filetype = None
		self.filenameonly = None
		self.master.title("Untitled -- Vik Text Editor")
		self.textArea.delete(1.0, tk.END)
	def saveFile(self):
		pass
	def saveAsFile(self):
		pass
	def openFile(self):
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
			os.system("start cmd /k cd " + self.cwd)
	def buildFile(self):
		if not self.filepath:
			messagebox.showerror(title = "Alert!", message = "Save file first!")
		else:
			if self.filetype == "py":
				temp = 'start cmd /k \"cd '+ self.cwd + ' && python ' + self.filename +"\""
				os.system(temp)
			elif self.filetype == "cpp":
				temp = 'start cmd /k \"cd '+ self.cwd + ' && g++ ' + self.filename + " -o " + self.filenameonly + "\""
				os.system(temp)
				print(temp)
	def runFile(self):
		if not self.filepath:
			messagebox.showerror(title = "Alert!", message = "Save file first!")
		else:
			if self.filetype == "py":
				temp = 'start cmd /k \"cd '+ self.cwd + ' && python ' + self.filename +" \""
				os.system(temp)
			elif self.filetype == "cpp":
				temp  = 'start cmd /k \"cd '+ self.cwd + ' && ' + self.filenameonly +"\""
				os.system(temp)




if __name__ == "__main__":
	master = tk.Tk()
	vik = Vik(master)
	master.mainloop()