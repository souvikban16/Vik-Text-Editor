import os 
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import simpledialog

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
		self.textArea = tk.Text(master, font =("Consolas", 18))
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
				self.saveFile()
			elif result == False:
				self.filepath == None
				self.newFile()
		else:
			textAreaContent = self.textArea.get(1.0, tk.END)
			print(len(textAreaContent))
			if len(textAreaContent) > 1:
				result = messagebox.askyesnocancel(title = "Alert!", message = "Save Current File ? ")
				if result == True:
					self.saveFile()
				elif result == False:
					pass
				elif result == None:
					return
				
			self.filepath = None
			self.filename = None
			self.filetype = None
			self.filenameonly = None
			self.master.title("Untitled -- Vik Text Editor")
			self.textArea.delete(1.0, tk.END)
	def saveFile(self):
		if not self.filepath:
			self.saveAsFile()
		else:
			textAreaContent = self.textArea.get(1.0, tk.END)
			with open(self.filepath, "w") as f:
				f.write(textAreaContent)


	def saveAsFile(self):
		self.filepath = filedialog.asksaveasfilename(defaultextension = "*.*")
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

	def openFile(self):
		if self.filepath:
			result = messagebox.askyesnocancel(title = "Alert!", message = "Save Current File ? ")
			if result == True:
				self.saveFile()
			elif result == False:
				pass
			elif result == None:
				return

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
			elif self.filetype == "c":
				temp = 'start cmd /k \"cd '+ self.cwd + ' && gcc ' + self.filename + " -o " + self.filenameonly + "\""
				os.system(temp)
				print(temp)
			elif self.filetype == "java":
				temp = 'start cmd /k \"cd '+ self.cwd + ' && javac ' + self.filename + "\""
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
			elif self.filetype == "c":
				temp  = 'start cmd /k \"cd '+ self.cwd + ' && ' + self.filenameonly +"\""
				os.system(temp)
			elif self.filetype == "java":
				result = simpledialog.askstring("Input", "Enter the class name with the main method")
				temp = 'start cmd /k \"cd '+ self.cwd + ' && java ' + result + "\""
				os.system(temp)
				print(temp)




if __name__ == "__main__":
	master = tk.Tk()
	vik = Vik(master)
	master.mainloop()