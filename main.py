import http.server
from urllib.parse import urlparse,parse_qs
import socketserver
import webbrowser
import json
import os
import re
import random
url="http://localhost:8080/www/"
PORT=8080

Handler=http.server.SimpleHTTPRequestHandler

class CustomHandler(Handler):
        wordlist=[]
        req=0;
        def readDict(self):
                wf=open("words.txt",'r');
                for word in wf:
                        word=word.strip()
                        self.wordlist.append(word)
               
                
                
        def do_GET(self):
                CustomHandler.req=CustomHandler.req+1
                if(len(self.wordlist)==0):
                        self.readDict()
                qp=urlparse(self.path).query
                q=parse_qs(qp).get('q',None)
                if q!=None:
                        self.send_response(200)
                        self.send_header('Content-type','text/html')
                        self.end_headers()
                        wl=self.get_random_word()
                        print(q[0])
                        self.wfile.write(bytes("<h1>"+wl+"</h1><br><p1>"+str(round(CustomHandler.req/1000,1))+"k request served.</p>",encoding='utf-8'))
                else:
                        f = self.send_head()
                        if f:
                            try:
                                self.copyfile(f, self.wfile)
                            finally:
                                f.close()
        def get_words(self,term):
                wordlist=[]
                count=0
                for word in self.wordlist:
                        if count>=10:
                                break
                        elif re.match(term,word):
                                wordlist.append(word)
                                count+=1
                return wordlist
        def get_random_word(self):
        
                return str(self.wordlist[random.randint(0,len(self.wordlist))])
                

# ip can be 0.0.0.0 or 127.0.0.1
# for lan access and get the ip from dhcp of router 0.0.0.0
with socketserver.TCPServer(("0.0.0.0",PORT),CustomHandler) as httpd:
    print("Http Server running at Port",PORT)
    webbrowser.open_new_tab(url)
    httpd.serve_forever()
