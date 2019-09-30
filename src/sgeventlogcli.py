import click
import logging
import shotgunEventDaemon as sgED
import shotgun_api3 as sg

sgED.startHttpServer = False

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

@click.group()
def cli3():
    pass

@click.group()
def cli4():
    pass


@cli1.command(help=" option --conf filename ")
@click.option('--conf',default='shotgunEventDaemon.conf', help='config file.')
def listplugin(conf):
    engine = EngineCli(conf) 
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


@cli2.command(help=" option --conf filename ")
@click.option('--conf',default='shotgunEventDaemon.conf', help='config file.')
def info(conf):
    engine = EngineCli(conf) 
    conf = engine.config
    print("shotgun url : %s " % conf.getShotgunURL())
    print("plugin path : %s " % conf.getPluginPaths())
    
    #conf.set("shotgun","titi","toto")
    #with open(conf, 'w') as configfile:
    #    conf.write(configfile)

@cli3.command(help=" option --id eventlogid --name nameplugin")
@click.option('--id', help='id.')
@click.option('--name',default=None,help='id.')
@click.option('--conf',default='shotgunEventDaemon.conf', help='config file.')
def process(id,name,conf):   
   engine = EngineCli("shotgunEventDaemon.conf")

   # Get The EventLogEntry ID
   sgConnection = sg.Shotgun(engine.config.getShotgunURL(),
                             engine.config.getEngineScriptName(),
                             engine.config.getEngineScriptKey())
  
   event = sgConnection.find_one("EventLogEntry", [["id", "is", int(id)]], fields=[
                                  'id', 'event_type', 'attribute_name', 'meta', 'entity', 'user', 'project', 'session_uuid', 'created_at'])
  
   # Initialise the plugin.
   plugcollections = [sgED.PluginCollection(
       engine, s) for s in engine.config.getPluginPaths()]

   for plugc in plugcollections:
       plugc.load()
  
   for plugc in plugcollections:
       plugc.process(event)


@cli4.command(help=" option --id eventlogid --name nameplugin")
@click.option('--id', help='id.')
@click.option('--name', help='name.')
def generate(id,name):
    pass



cli = click.CommandCollection(sources=[cli1,cli2,cli3,cli4])

if __name__ == '__main__':
    cli()