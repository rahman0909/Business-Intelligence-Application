
from tkinter import *
import tkinter
import socket 
from threading import Thread 
from socketserver import ThreadingMixIn
from os import path
import pickle
import sys
import numpy as np


mainGUI = tkinter.Tk()
mainGUI.title("Cloud Server") #designing main screen
mainGUI.geometry("900x700")
running = True




def startDistributedCore():
    class CoreThread(Thread): 
 
        def __init__(self,ip,port): 
            Thread.__init__(self) 
            self.ip = ip 
            self.port = port 
            text.insert(END,'Request received from Client IP : '+ip+' with port no : '+str(port)+"\n") 
 
        def run(self):
            text.delete('1.0', END)
            global details
            data = conn.recv(100) #receive encrypted data
            dataset = pickle.loads(data) #convert binary data into enecrypted data
            request_type = dataset[0]
            if request_type == "download":
                fname = dataset[1]
                fout = open('Dataset/'+fname, 'rb')
                data = fout.read()
                fout.close()
                text.insert(END,fname+" sent dataset to client for processing\n\n")
                output = []
                output.append(data)
                output = pickle.dumps(output)
                conn.send(output)             
            
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
    server.bind(('localhost', 2222))
    threads = []
    text.insert(END,"Cloud Server Started\n\n")
    while running:
        server.listen(4)
        (conn, (ip,port)) = server.accept()
        newthread = CoreThread(ip,port) 
        newthread.start() 
        threads.append(newthread) 
    for t in threads:
        t.join()

def startCore():
    Thread(target=startDistributedCore).start()


gfont = ('times', 16, 'bold')
gtitle = Label(mainGUI, text='Cloud Server')
gtitle.config(bg='darkviolet', fg='gold')    
gtitle.config(font=gfont)           
gtitle.config(height=3, width=120)       
gtitle.place(x=0,y=5)

gfont1 = ('times', 12, 'bold')

text=Text(mainGUI,height=28,width=130)
scroll=Scrollbar(text)
text.configure(yscrollcommand=scroll.set)
text.place(x=10,y=100)
text.config(font=gfont1)

startCore()

mainGUI.config(bg='sea green')
mainGUI.mainloop()


