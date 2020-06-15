import os 
import tkinter as tk


class Menubar:

	def __init__(self, parent):
		menubar = tk.Menu(parent.master)
		parent.master.config(menu =menubar)
		menubar.add_command(label = "New", command = parent.newFile)
		menubar.add_command(label = "Save", command = parent.saveFile)
		menubar.add_command(label = "Save As", command = parent.saveAsFile)
		menubar.add_command(label = "Open", command = openFile)
		menubar.add_separator()
		menubar.add_command(label = "CMD", command = openCMD)

class Vik:

	def __init__(self, master):
		master.title("Untitled -- Vik Text Editor")
		master.geometry("500x500")

		self.master = master

		self.textArea = tk.Text(master)
		self.scrollBarY = tk.Scrollbar(master, command = self.textArea.yview)
		# self.scrollBarX = tk.Scrollbar(master, command = self.textArea.xview)
		self.textArea.configure(yscrollcommand = self.scrollBarY.set)
		# self.textArea.configure(xscrollcommand = self.scrollBarX.set)
		self.textArea.pack(side = tk.LEFT,  fill = tk.BOTH, expand = True)
		self.scrollBarY.pack(side = tk.RIGHT, fill = tk.Y)
		# self.scrollBarX.pack(side = tk.BOTTOM, fill = tk.X)

		self.menu = Menubar(self)






if __name__ == "__main__":
	master = tk.Tk()
	vik = Vik(master)
	master.mainloop()