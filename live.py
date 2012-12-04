import gevent
from gevent.http import HTTPServer
from gevent.event import Event
from gevent.queue import Queue 
import json

e = Event()
global_counter = 0
stuff = []

def handle(request):
    global global_counter, stuff
    if request.uri == '/guess':
        text = request.input_buffer.read()
        stuff.append(text)
        if len(stuff) > 100:
            stuff.pop(0)
            global_counter += 1
        request.send_reply(200,"OK","")
        e.set()
    elif request.uri.startswith('/wait/'):
        counter = int(request.uri[6:])
        if counter > (global_counter + len(stuff)):
            e.clear()
            e.wait()
        i = counter - global_counter
        if i < 0:
            i = 0
        counter = global_counter + len(stuff)
        request.send_reply(200,"OK",
                '{"counter":'+str(counter)+', "guesses":['+','.join(stuff[i:])+']}')

server = HTTPServer(('127.0.0.1', 65300), handle)
server.serve_forever()
