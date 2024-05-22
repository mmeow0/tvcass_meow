import base64
import os
import time
import tkinter as tk
import cv2, imutils
import numpy as np
from PIL import Image, ImageTk
import zmq
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

from cipher import AESCipher

class VideoPlayer:
    WIDTH = 550
    HEIGHT = 400
    
    def __init__(self, master=None):
        self.master = master
        self.canvas = tk.Canvas(master, width=self.WIDTH, height=self.HEIGHT, background='grey')
        self.canvas.grid(row=9,pady=(0, 5)) 
        self.errmsg = tk.StringVar()  
        self.error_label = tk.Label(master, textvariable=self.errmsg, foreground="red").grid(row=10, pady=(0,10))

    def run(self, host, port, cipher = None):
        context = zmq.Context()
        self.socket = context.socket(zmq.SUB)
        self.socket.connect("tcp://{}:{}".format(host, port))
        self.socket.setsockopt_string(zmq.SUBSCRIBE, '')
        
        fps,st,frames_to_count,cnt = (0,0,20,0)
        
        while True:
            jpg_as_text = self.socket.recv()
            if cipher != None:
                try:
                    jpg_as_text = AESCipher(cipher.encode()).decrypt(jpg_as_text)
                except:
                    self.errmsg.set("Не получилось расшифровать видеопоток! Неверный ключ")
            jpg_original = base64.b64decode(jpg_as_text)
            jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
                
            frame = cv2.imdecode(jpg_as_np,1)
            frame = cv2.putText(frame,'FPS: '+str(fps),(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = imutils.resize(frame,width=self.WIDTH, height=self.HEIGHT)
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):
                self.socket.close()
                os._exit(1)

            if cnt == frames_to_count:
                try:
                    fps = round(frames_to_count/(time.time()-st),1)
                    st=time.time()
                    cnt=0
                except:
                    pass
            cnt+=1