import time
from time import sleep

string = open('shared_output.txt','r')
data = string.read().split(" ")[1]


while True:
	counter += 1
	print("I am now {}".format(counter))
	sleep(0.5)