import click
import logging
import shotgunEventDaemon as sgED

class EngineCli(sgED.Engine):
    def __init__(self, configPath):
        super(EngineCli,self).__init__(configPath)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(levelname)s:%(name)s:%(message)s"))
        logging.getLogger().addHandler(handler)
        self.setLogger(logging.getLogger())

@click.group()
def cli1():
    pass

@click.group()
def cli2():
    pass

@cli1.command()
def listplugin():
    engine = EngineCli('shotgunEventDaemon.conf') 
    #print("%s " % engine.config.getPluginPaths())

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

@cli2.command()
def info():
    engine = EngineCli('shotgunEventDaemon.conf') 
    conf = engine.config
    print("shotgun url : %s " % conf.getShotgunURL())
    print("plugin path : %s " % conf.getPluginPaths())
    
    #conf.set("shotgun","titi","toto")
    #with open('shotgunEventDaemon.cfg', 'w') as configfile:
    #    conf.write(configfile)

cli = click.CommandCollection(sources=[cli1,cli2])

if __name__ == '__main__':
    cli()