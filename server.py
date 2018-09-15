import socket
import threading

host = "127.0.0.1"
port = 5000

connections = []

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((host, port))
serverSocket.listen(1)


def handler(c, a):
	while True:
		try:
			data = c.recv(1024)
		except socket.error:
			print("user left")
			connections.remove(c)
			c.close()
			break
		message = data
		for connection in connections:
			connection.send(message)


def Main():
	while True:
		c, a = serverSocket.accept()

		messageThread = threading.Thread(target=handler, args=(c, a))
		messageThread.setDaemon(True)
		messageThread.start()

		connections.append(c)

if __name__ == "__main__":
	Main()
