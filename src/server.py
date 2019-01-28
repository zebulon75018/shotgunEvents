from flask import Flask, render_template
from flask import jsonify
from threading import Thread
import time
import datetime
import shotgunEventDaemon as sgED
import logging

import json

# App instance
app = Flask(__name__)

thread = None
running = True

# Debug mode, with auto-reload
app.debug = True
plugcollections = []

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
event = {}

# Initialise the plugin.
plugcollections = [sgED.PluginCollection(
    engine, s) for s in engine.config.getPluginPaths()]

for plugc in plugcollections:
    plugc.load()


def worker_task():
    global running
    
    print("Thread started")
    while running:
        """ Put blocking code that might take longer to execute here """
        time.sleep(5)
        try:
            for plugc in plugcollections:
                plugc.process(event)
        except Exception as e:
            print("Exception %s" % e)
        print("Thread...")
    print("Thread stopped")

# Simple JSON file parser
def get_json(path):
    file = open(path)
    data = json.load(file)
    file.close()
    return data

@app.route("/")
def index():
    data = {}
    return jsonify(data)
    #return render('simple.html', )

if __name__ == "__main__":
    thread = Thread(target = worker_task)
    thread.start()
    app.run()
