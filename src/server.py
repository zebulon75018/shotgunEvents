from flask import Flask, render_template
from flask import jsonify
from threading import Thread
import threading

import time
import datetime
import shotgunEventDaemon as sgED
import logging
import Queue
import json

# App instance
app = Flask(__name__)

thread = None
running = True

# Debug mode, with auto-reload
app.debug = True
plugcollections = []

counter = 0
class EngineCli(sgED.Engine):
    def __init__(self, configPath):
        super(EngineCli,self).__init__(configPath)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(levelname)s:%(name)s:%(message)s"))
        logging.getLogger().addHandler(handler)
        self.setLogger(logging.getLogger())

engine = EngineCli("shotgunEventDaemon.conf") 

# Get The EventLogEntry ID
#global sg
"""
sgConnection = sg.Shotgun(engine.config.getShotgunURL(),
                             engine.config.getEngineScriptName(),
                             engine.config.getEngineScriptKey(),
                         http_proxy=engine.config.getEngineProxyServer())
  
event = sgConnection.find_one("EventLogEntry", [["id", "is", int(id)]], fields=[
                                'id', 'event_type', 'attribute_name', 'meta', 'entity', 'user', 'project', 'session_uuid', 'created_at'])
"""
event = {'id':7806,'event_type':'Shotgun_Entity_Change','attribute_name':'sg_status_list'}

# Initialise the plugin.

plugcollections = [sgED.PluginCollection(
    engine, s) for s in engine.config.getPluginPaths()]

for plugc in plugcollections:
    plugc.load()

q = Queue.LifoQueue()

class MyThread(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}):
        super(MyThread, self).__init__(group, target, name, args, kwargs)
        self.counter = 0
        print("Create Thread")


def worker_task():
    global running
    global thread
    global event
    global plugcollections
    
    print("Thread started")
    while running:
        """ Put blocking code that might take longer to execute here """
        time.sleep(1)
        #try:
        """
        for plugc in plugcollections:
            plugc.process(event)
        """
        thread.counter = thread.counter + 1

        print(event)     
        for plugc in plugcollections:
            print(plugc)
            plugc.process(event)

        q.put(thread.counter)
        #t = threading.currentThread()
        #print(thread.counter)
        #print(t.counter)
            
        #except Exception as e:
        #    print("Exception %s" % e)

        print("Thread...")
    print("Thread stopped")

@app.route("/")
def index():
    return render_template('simple.html',name=q.get())

if __name__ == "__main__":
    thread = MyThread(target = worker_task)
    thread.start()
    app.run()
