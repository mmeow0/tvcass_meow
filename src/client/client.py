import cv2
import numpy as np
import time, os
import base64
import zmq

BUFF_SIZE = 65536

BREAK = False
host_ip = '192.168.0.105'
print(host_ip)
port = 5555

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://{}:{}".format(host_ip, port))

socket.setsockopt_string(zmq.SUBSCRIBE, '')

cv2.namedWindow('RECEIVING VIDEO')        
cv2.moveWindow('RECEIVING VIDEO', 10,360) 
fps,st,frames_to_count,cnt = (0,0,20,0)
         
while True:
    jpg_as_text = socket.recv()
    jpg_original = base64.b64decode(jpg_as_text)
    jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
        
    frame = cv2.imdecode(jpg_as_np,1)
    frame = cv2.putText(frame,'FPS: '+str(fps),(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
    cv2.imshow("RECEIVING VIDEO",frame)
    key = cv2.waitKey(1) & 0xFF
    
    if key == ord('q'):
        socket.close()
        os._exit(1)

    if cnt == frames_to_count:
        try:
            fps = round(frames_to_count/(time.time()-st),1)
            st=time.time()
            cnt=0
        except:
            pass
    cnt+=1

