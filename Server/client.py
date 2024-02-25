# client.py
import time
import socket
from send_rcv import send_msg, recv_msg
from encoding import encode, decode
class MySynchronousTCPClient:
    def __init__(self, host, port, timeout=10, wait=10):
        self.addr = (host, port)
        self.timeout = timeout
        self.wait = wait
    def send_request(self, the_goods):
        t0 = time.time()
        sock = socket.create_connection(
                   self.addr, 
                   timeout=self.timeout
               )                  
        
        send_msg(encode(the_goods))
        t0 = time.time()
        msg = None
        while not msg:
            msg = decode(recv_msg(sock))
            if time.time() - t0 > self.wait:
                raise TimeoutError('Timed out waiting for resp.')
    
        sock.close()
        return msg