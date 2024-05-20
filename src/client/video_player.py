import base64
import os
import time
import tkinter as tk
import cv2, imutils
import numpy as np
from PIL import Image, ImageTk
import zmq

class VideoPlayer:
    WIDTH = 550
    HEIGHT = 400
    
    def __init__(self, master=None):
        host_ip = '192.168.0.105'
        print(host_ip)
        port = 5555

        context = zmq.Context()
        self.socket = context.socket(zmq.SUB)
        self.socket.connect("tcp://{}:{}".format(host_ip, port))
        self.socket.setsockopt_string(zmq.SUBSCRIBE, '')
        
        self.master = master
        self.canvas = tk.Canvas(master, width=self.WIDTH, height=self.HEIGHT, background='grey')
        self.canvas.grid(row=6,pady=(0, 20))
            
    def run(self):
        fps,st,frames_to_count,cnt = (0,0,20,0)
        
        while True:
            jpg_as_text = self.socket.recv()
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