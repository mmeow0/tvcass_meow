import re
import threading
import tkinter as tk

from video_player import VideoPlayer
from video_server import VideoServer
            
class App:
    filename =  'astley.avi'
    TMP_AUDIO =  'temp.wav'
    
    def __init__(self):
        # command = "ffmpeg -y -i {} -ab 160k -ac 2 -ar 44100 -vn {}".format(self.filename, self.TMP_AUDIO)
        # os.system(command)
        
        self.root = tk.Tk()
        self.root.geometry('800x800')
        self.root.grid_columnconfigure(0, weight=1)
        self.root.title('Система условного доступа')

        self.frame = tk.Frame(self.root)
        self.frame.grid()
      
        self.errmsg = tk.StringVar()  
        
        check = (self.root.register(self.is_valid), "%P")
         
        self.label = tk.Label(self.frame, text="Введите порт для трансляции незашифрованного сигнала: ").grid(row=0, pady=(20,5))
        self.entry = tk.Entry(self.frame, validate="key", validatecommand=check)
        self.entry.grid(row=1, pady=(0,20))
        
        self.label_2 = tk.Label(self.frame, text="Введите порт для трансляции зашифрованного сигнала: ").grid(row=2, pady=(0,5))
        self.entry_2 = tk.Entry(self.frame, validate="key", validatecommand=check)
        self.entry_2.grid(row=3, pady=(0,10))

        self.error_label = tk.Label(self.frame, textvariable=self.errmsg, foreground="red").grid(row=4, pady=(0,10))
 
        self.player = VideoPlayer(self.filename, master=self.root)
        self.but = tk.Button(self.frame, text="Транслировать", command=self.btn_click, state=tk.DISABLED)
        self.but.grid(row=5, pady=(0,10))

        self.root.mainloop()
        
    def schedule_check(self, t):
     self.root.after(1000, self.check_if_done, t)

    def check_if_done(self, t):
        if t.is_alive():
            self.schedule_check(t)
            
    def btn_click(self):
        video_server = VideoServer(self.filename, self.entry.get())
        t = threading.Thread(target=video_server.video_stream)
        t.start()
        
        video_server_enc = VideoServer(self.filename, self.entry_2.get(), 'This is a key123')
        t_2 = threading.Thread(target=video_server_enc.video_stream)
        t_2.start()
            
        self.but['state'] = tk.DISABLED
            
        self.player.run()
        self.schedule_check(t)
        # self.schedule_check(t_2)
            
    def is_valid(self, newval):
        result=re.match(r'\d+', newval) is not None
        if not result:
            self.errmsg.set("Некорректные данные!")
            self.but.config(state=tk.DISABLED)
        else:
            self.errmsg.set("")
            self.but.config(state=tk.ACTIVE)
        return result
            
        

app=App()