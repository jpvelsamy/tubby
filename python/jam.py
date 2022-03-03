import os
import sys
import subprocess
import pwd
import ConfigParser
import io
import logging
import logging.handlers
import ConfigParser
import argparse
from jamconfig import Configuration
from jamprompt import JamPrompt


LOG_FILE_NAME="jam.log"
CFG_FILE_NAME="jam.cfg"

logger = logging.getLogger("Jam-Commcenter")
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger.setLevel(logging.DEBUG)

fileHandler = logging.handlers.RotatingFileHandler(LOG_FILE_NAME,
                                               maxBytes=1000000,
                                               backupCount=5
                                           )
fileHandler.setLevel(logging.INFO)
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.DEBUG)
consoleHandler.setFormatter(formatter)

logger.addHandler(consoleHandler)



#Refered this link - http://pymotw.com/2/argparse/
def readConfig(configFile):
        config = ConfigParser.ConfigParser()
        if(configFile and not configFile.isspace()):
                if os.path.exists(configFile):
                        config.read(configFile)
                else:
                        raise RuntimeError("If you intend to use your own config file"+
                        "(by default commcenter has its own config file),"+
                        "then ensure the path is correct."+
                        "The config file path you gave is absent="+configFile)
        else:
                config.read(CFG_FILE_NAME)
        return config
    
def loadParsedArgs():
        parser = argparse.ArgumentParser(description='Humingo Command center application')
        parser.add_argument('-c','--command',
                            action="store",
                            dest="command",
                            help="Possible commands(installcandyman,pushcandymanpatch,startcandyman,stopcandyman,healthcheck,stopjamie,startjamie)",
                            required=False)
        parser.add_argument('-m','--machine',
                            action="store",
                            dest="machineList",
                            help="If you want to specifically target a machine(s),"+
                            "then use this to key in the ip address",
                            required=False)
        parser.add_argument('-f','--config-file', 
                            action="store", 
                            dest="configFilePath", 
                            help ="Provide the configuration file path,"+
                            "by default it is not required as it will be present along "+
                            "with the commandcenter module itself", 
                            required=True)
        return parser
    
def initialize(commandLineConfig):
        configFile = commandLineConfig.configFilePath
        config = readConfig(configFile)
        configObj=Configuration(commandLineConfig,config)
        return configObj
    
def main():
    logger.info("Booting Comm center ")
    parser = loadParsedArgs()
    inputConfig=parser.parse_args()
    configObj = initialize(inputConfig)
    logger.info("Initialized configuration object %s",configObj)
    logger.info("Starting the repl for %s", configObj.getMachineList())
    prompt = JamPrompt()
    prompt.configObj=configObj
    prompt.prompt = '> '
    prompt.cmdloop('Starting prompt...')
    

main()    
