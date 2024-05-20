import re
import threading
import tkinter as tk

from video_player import VideoPlayer
            
class App:
    BUFF_SIZE = 65536
    host_ip = '192.168.0.105'
    port = 5555
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('800x800')
        self.root.grid_columnconfigure(0, weight=1)
        self.root.title('Клиент системы условного доступа')

        self.frame = tk.Frame(self.root)
        self.frame.grid()
        
        self.errmsg = tk.StringVar()  
        
        check = (self.root.register(self.is_valid), "%P")
         
        self.label = tk.Label(self.frame, text="Введите адрес").grid(row=0, pady=(20,5))
        self.entry = tk.Entry(self.frame, validate="key", validatecommand=check)
        self.entry.grid(row=1, pady=(0,20))
        
        self.label_2 = tk.Label(self.frame, text="Введите порт").grid(row=2, pady=(0,5))
        self.entry_2 = tk.Entry(self.frame, validate="key", validatecommand=check)
        self.entry_2.grid(row=3, pady=(0,10))

        self.error_label = tk.Label(self.frame, textvariable=self.errmsg, foreground="red").grid(row=4, pady=(0,10))

        self.player = VideoPlayer(master=self.root)
        self.but = tk.Button(self.frame, text="Подключиться", command=self.btn_click, state=tk.DISABLED)
        self.but.grid(row=5, pady=(0,10))

        self.root.mainloop()
        
    def schedule_check(self, t):
        self.root.after(1000, self.check_if_done, t)

    def check_if_done(self, t):
        if t.is_alive():
            self.schedule_check(t)
                
    def btn_click(self):   
        self.but['state'] = tk.DISABLED
        
        t = threading.Thread(target=self.player.run)
        t.start()
        self.schedule_check(t)
            
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