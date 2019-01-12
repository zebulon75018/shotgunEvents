import click
import logging
import shotgunEventDaemon as sgED

engine = sgED.Engine('shotgunEventDaemon.conf') 
#print("%s " % engine.config.getPluginPaths())
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(levelname)s:%(name)s:%(message)s"))
logging.getLogger().addHandler(handler)
engine.setLogger(logging.getLogger())

plugcollections = [sgED.PluginCollection(engine, s) for s in engine.config.getPluginPaths()]
for plugc in plugcollections:
    plugc.load()
    for plug in  plugc:
        
        print("%s:" % plug.getName())
        print("\tPATH:\t\t%s" % plug._path)
        for call in plug._callbacks:
            print("\tMATCHEVENT:\t%s" % call._matchEvents)
            print("\tARGS:\t\t%s" % call._args)
            print("\tStop On Error:\t%s"  % call._stopOnError)
