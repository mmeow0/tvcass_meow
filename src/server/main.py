import os
import threading
import tkinter as tk

from src.server.video_player import VideoPlayer
from src.server.video_server import VideoServer
            
class App:
    filename =  'astley.avi'
    TMP_AUDIO =  'temp.wav'
    
    def __init__(self):
        # command = "ffmpeg -y -i {} -ab 160k -ac 2 -ar 44100 -vn {}".format(self.filename, self.TMP_AUDIO)
        # os.system(command)
        
        self.root = tk.Tk()
        self.root.geometry('700x500')
        self.root.grid_columnconfigure(0, weight=1)
        self.root.title('Система условного доступа')

        self.frame = tk.Frame(self.root)
        self.frame.grid()
        
        self.player = VideoPlayer(self.filename, master=self.root)
        self.but = tk.Button(self.frame, text="Транслировать", command=self.btn_click)
        self.but.grid(row=0, pady=20)

        self.root.mainloop()
        
    def schedule_check(self, t):
     self.root.after(1000, self.check_if_done, t)

    def check_if_done(self, t):
        if t.is_alive():
            self.schedule_check(t)
            
    def btn_click(self):
        video_server = VideoServer(self.filename, 5555)
        t = threading.Thread(target=video_server.video_stream)
        t.start()
        
        self.but['state'] = tk.DISABLED
        
        self.player.run()
        self.schedule_check(t)
        

app=App()