import socket
import threading
import tkinter
import time


class PyChat:
	host = "127.0.0.1"
	port = 5000
	thisMessage = ""

	clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def recieve(self):
		currentMessage = ""
		while True:
			time.sleep(0.1)
			lastMessage = currentMessage
			currentMessage = str(self.clientSocket.recv(1024), "utf-8")
			if not lastMessage == currentMessage:
				self.thisMessage = currentMessage
			else:
				continue

	def message(self, text, name):
		if text:
			self.clientSocket.send(bytes(name + ": " + text, "utf-8"))

	def __init__(self):
		try:
			self.clientSocket.connect((self.host, self.port))
			print("[*] Connected")
		except socket.error:
			print("[!] Socket Error")
			quit(0)

		receiver = threading.Thread(target=self.recieve)
		receiver.start()


class GUI:
	def __init__(self, root):
		name = tkinter.Label(root, text="Name: ")
		message = tkinter.Label(root, text="Message: ")

		self.nameEntry = tkinter.Entry(root)
		self.messageEntry = tkinter.Entry(root)

		self.messageField = tkinter.Text(root, state="disabled", width=50, height=30)

		quitButton = tkinter.Button(root, text="Quit", command=root.destroy)
		clearButton = tkinter.Button(root, text="Clear", command=lambda a=0, b="end": self.messageField.delete(a, b))

		name.grid(row=0)
		message.grid(row=1)
		quitButton.grid(row=0, column=3)
		clearButton.grid(row=1, column=3)
		self.nameEntry.grid(row=0, column=1)
		self.messageEntry.grid(row=1, column=1)
		self.messageField.grid(row=2, columnspan=2)


		self.messageEntry.bind("<Return>", self.sendMessage)

		displayThread = threading.Thread(target=self.displayMessage)
		displayThread.setDaemon(True)
		displayThread.start()

	def sendMessage(self, event):
		chat.message(self.messageEntry.get(), self.nameEntry.get())
		self.messageEntry.delete(0, "end")

	def displayMessage(self):
		newMessage = ""
		while True:
			time.sleep(0.1)
			lastMessage = newMessage
			newMessage = chat.thisMessage
			if not lastMessage == newMessage:
				self.messageField.configure(state="normal")
				self.messageField.insert("1.0", newMessage + "\n")
				self.messageField.configure(state="disabled")
				print("Inserted " + newMessage)

root = tkinter.Tk()

chat = PyChat()
gui = GUI(root)

root.mainloop()

print("Done")
exit(0)