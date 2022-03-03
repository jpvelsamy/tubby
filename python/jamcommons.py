import logging
import os
import sys
import subprocess
import pwd
import io

logger = logging.getLogger("Jam-Commcenter")

def createDirectory(directoryName):
        logger.info("Creating the checkout directory="+directoryName)
        try:
            os.makedirs(directoryName)
        except OSError:
            if os.path.exists(directoryName):
                # We are nearly safe
                logger.fatal("Directory="+directoryName+" already exists, leaving it as is")
                raise RuntimeError("Directory already exists, you may not want clone, check and rerun")	

#took this method from - http://www.saltycrane.com/blog/2009/10/how-capture-stdout-in-real-time-python/

def makeoscall(cmd):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout = []
    while True:
        line = p.stdout.readline()
        stdout.append(line)
        logger.fatal(line),
        if line == '' and p.poll() != None:
            break
    return ''.join(stdout)


def changeDir(dirName):
    # I used the following tutorial to get this snippet
    #http://www.tutorialspoint.com/python/os_chdir.htm
    os.chdir(dirName)
    currentDir = os.getcwd()
    logger.debug("Changing the directory to="+currentDir)
