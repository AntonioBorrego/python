# -*- coding: utf-8 -*-

#from multiprocessing import Process
#from multiprocessing import Queue
from multiprocessing.connection import Client

from tkinter import *
import time, random


def draw_board(canvas, board):
    canvas.delete('all')
    for key,value in board:
       print (key, value)
       (x,y), size, color = value
       canvas.create_oval(x, y, int(x-size), int(y-size), fill=color)

if __name__ == '__main__':    

    root = Tk()
    root.title("MyAgario")
    root.resizable(0, 0)
    
    frame = Frame(root)    
    frame.pack()

    k = 10
    w = 50*k
    h = 25*k
    canvas = Canvas(frame, width=w, height=h, bg="green")
    canvas.pack()

    pointer_x, pointer_y = 0,0
    def move(event):        
        #print ("raton moviendose", event.x, event.y)
        global pointer_x
        global pointer_y 
        pointer_x, pointer_y = event.x, event.y 

    canvas.bind("<Motion>", move)

    print ('trying to connect')
    conn = Client(address=('127.0.0.1', 6000), authkey=b'secret')
    print ('connection accepted')

    try:
        while 1:
            conn.send((pointer_x, pointer_y))
            message = conn.recv()
            draw_board(canvas, message)
            root.update()
    except TclError:
        pass
   

