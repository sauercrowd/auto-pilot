import display
import socket
from PIL import Image

def loop(s, size):
	buffer_size= size[0] * size[1] * 3
	data = s.recv(buffer_size)
	return Image.frombytes(mode='RGB', size=size, data=data)

def finish_fn(s):
	s.close()

def main():
	TARGET_IP = "192.168.2.95"

	size=(1024,768)
	x = display.Display('Desktop Capture')

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((TARGET_IP, 7654))

	x.set_poll_function(loop, s, size)
	x.set_finish_function(finish_fn, s)

	x.show()

if __name__ == "__main__":
	main()
