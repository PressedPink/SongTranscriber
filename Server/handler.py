# handler.py
from encoding import encode, decode
from socketserver import BaseRequestHandler
class MyTCPHandler(BaseRequestHandler):
    
    def handle(self):
        sock = self.request
        
        the_goods = decode(recv_msg(sock))
        # Do something more interesting here:
        print(f"Here's what we got: {the_goods}")
        send_msg(sock, encode({"msg": "Goods received."}))