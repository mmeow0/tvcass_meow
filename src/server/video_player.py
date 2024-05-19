import tkinter as tk
import cv2, imutils
from PIL import Image, ImageTk

class VideoPlayer:
    WIDTH = 550
    HEIGHT = 400
    
    def __init__(self, video_file, master=None):
        self.cap = cv2.VideoCapture(video_file)
        self.master = master
        self.canvas = tk.Canvas(master, width=self.WIDTH, height=self.HEIGHT, background='grey')
        self.canvas.grid(row=1,pady=(0, 20))
        self.delay = int(1000/self.cap.get(cv2.CAP_PROP_FPS))

    def update(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = imutils.resize(frame,width=self.WIDTH, height=self.HEIGHT)
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
            self.master.after(self.delay, self.update)
        else:
            self.cap.release()
            
    def run(self):
        self.update()