import cv2, imutils
import time
import base64
import threading
import queue
import os
import zmq
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

from cipher import AESCipher

class VideoServer:
    WIDTH = 500
    TMP_AUDIO =  'temp.wav'
    q = queue.Queue(maxsize=10)
    host_ip = '0.0.0.0'

    def __init__(self, filename, port, cypher_key = ''):
        self.cypher_key = cypher_key
        context = zmq.Context()
        self.socket = context.socket(zmq.PUB)
        self.socket.bind("tcp://{}:{}".format(self.host_ip, port))
        self.vid = cv2.VideoCapture(filename)
        self.FPS = self.vid.get(cv2.CAP_PROP_FPS)
        self.t1 = threading.Thread(target=self.video_stream_gen, args=())
       
    def do_encrypt(self, message):
        obj = AES.new(self.cypher_key.encode("utf8"), AES.MODE_CBC, 'This is an IV456'.encode("utf8"))
        plaintext_padded = pad(message, AES.block_size)
        ciphertext = obj.encrypt(plaintext_padded)
        return ciphertext
         
    def video_stream_gen(self):
        while(self.vid.isOpened()):
            try:
                _,frame = self.vid.read()
                frame = imutils.resize(frame,width=self.WIDTH)
                self.q.put(frame)
            except:
                os._exit(1)
        print('Player closed')
        self.vid.release()
        
    def video_stream(self):
        self.t1.start()
        TS = (1/self.FPS)
        while True:
                    fps,st,frames_to_count,cnt = (0,0,1,0)
                    frame = self.q.get()
                    _,buffer = cv2.imencode('.jpeg',frame,[cv2.IMWRITE_JPEG_QUALITY,80])
                    message = base64.b64encode(buffer)
                    if len(self.cypher_key) != 0:
                        message = AESCipher(b'8bda7c9b0e97affe14a7691de7e3a977').encrypt(message.decode("utf-8"))
                    self.socket.send(message)
                    frame = cv2.putText(frame,'FPS: '+str(round(fps,1)),(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
                    if cnt == frames_to_count:
                        try:
                            fps = (frames_to_count/(time.time()-st))
                            st=time.time()
                            cnt=0
                            if fps>self.FPS:
                                TS+=0.001
                            elif fps<self.FPS:
                                TS-=0.001
                            else:
                                pass
                        except:
                            pass
                    cnt+=1
            
                    key = cv2.waitKey(int(1000*TS)) & 0xFF    
                    if key == ord('q'):
                        os._exit(1)
