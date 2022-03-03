import os
import sys
import subprocess
import pwd
import io
import logging
import logging.handlers
import argparse
import shutil

LOG_FILE_NAME="jam.log"
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


def main():
	logger.info("Bootstrapping remote.jam..sh")
	parser = argparse.ArgumentParser(description='Juno remote command center application')
	parser.add_argument('-s','--serverName',
	                action="store",
	                dest="serverName",
	                help="Possible servers(candyman, jamie)",
	                required=False)
	parser.add_argument('-c','--command',
	                action="store",
	                dest="command",
	                help="Possible commands(startcandyman,stopcandyman,healthcheck,buildcandyman, startjamie, stopjamie, buildjamie)",
	                required=False)
	parser.add_argument('-t','--targetfolder',
	                action="store",
	                dest="targetfolder",
	                help="Default deployment folder",
	                required=False)        	
	parser.add_argument('-b','--branch',
	                action="store",
	                dest="branch",
	                help="Branch name",
	                required=False)


	cmdlineConfig=parser.parse_args()        	
	command=cmdlineConfig.command

	if(command=='stopcandyman'):
		serverName=cmdlineConfig.serverName
		targetfolder=cmdlineConfig.targetfolder+"/candyman"
		stopInstance(serverName,targetfolder)
	elif(command=='buildcandyman'):
		url="git@bitbucket.org:junocomm/candyman.git"
		targetfolder=cmdlineConfig.targetfolder
		branch=cmdlineConfig.branch
                removeDirectory(targetfolder+"/candyman")
                removeDirectory(targetfolder+"/handyman")
		buildCandyman(targetfolder,branch,url)
	elif(command=='startcandyman'):
		targetfolder=cmdlineConfig.targetfolder
                serverName=cmdlineConfig.serverName
		stopInstance(serverName,targetfolder+"/candyman")
		startCandyman(targetfolder)        
	elif(command=='stopjamie'):
		targetfolder=cmdlineConfig.targetfolder
		serverName=cmdlineConfig.serverName
		stopJamieInstance(serverName,targetfolder)
	elif(command=='buildjamie'):
		url="git@bitbucket.org:junocomm/jammiddleware.git"
		targetfolder=cmdlineConfig.targetfolder
		branch=cmdlineConfig.branch
                removeDirectory(targetfolder+"/jammiddleware")                                
		buildJamie(targetfolder,branch,url)                		
	elif(command=='startjamie'):
		targetfolder=cmdlineConfig.targetfolder+"/jammiddleware"
                serverName=cmdlineConfig.serverName
		stopJamieInstance(serverName,targetfolder)
		startJamie(targetfolder)           	        		   		
	elif(command=='installcandyman'):
		url="git@bitbucket.org:junocomm/candyman.git"
		targetfolder=cmdlineConfig.targetfolder
		branch=cmdlineConfig.branch
		serverName=cmdlineConfig.serverName
		stopInstance(serverName,targetfolder+"/candyman")
                removeDirectory(targetfolder+"/candyman")
                removeDirectory(targetfolder+"/handyman")
                logger.debug("Installing candyman infra for branch %s",branch)
		buildCandyman(targetfolder,branch,url)
		installfolder=cmdlineConfig.targetfolder+"/candyman"
		#startCandyman(installfolder)        
	elif(command=='installjamie'):
		url="git@bitbucket.org:junocomm/jammiddleware.git"
		targetfolder=cmdlineConfig.targetfolder
		branch=cmdlineConfig.branch
		serverName=cmdlineConfig.serverName
		stopJamieInstance(serverName,targetfolder+"/jammiddleware")
                removeDirectory(targetfolder+"/jammiddleware")
		buildJamie(targetfolder,branch,url)      		
		installfolder=cmdlineConfig.targetfolder+"/jammiddleware"
		#startJamie(installfolder)           	        		   		

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

def makeoscallbg(cmd):
	p = subprocess.Popen(cmd, shell=True, close_fds=True)

def changeDir(dirName):
	# I used the following tutorial to get this snippet
	#http://www.tutorialspoint.com/python/os_chdir.htm
	os.chdir(dirName)
	currentDir = os.getcwd()
	logger.debug("Changing the directory to="+currentDir)
                

def stopInstance(serverName, targetfolder):
    #serverName="scala:run -Dlauncher=spw"
    serverPidCommand="ps -ef |grep java| grep \""+targetfolder+"\""+"| grep \""+serverName+"\" | awk '{print $2}'"
    logger.info("Finding server pid for process with %s", serverPidCommand)
    pid=makeoscall(serverPidCommand)
    logger.info("Retrieved for process  %s, server pid %s", serverName, pid)
    pidlist=pid.splitlines()
    logger.info("Processes listed %s",pidlist)
    #for procid in pidlist:
        #logger.info("Attempting to kill process %s",procid.strip())
        #killCommand="sudo kill -9 "+procid.strip()
        #makeoscall(killCommand)
    for i in range(len(pidlist)):
        logger.info("Attempting to kill process %s",pidlist[i])
        #os.kill(int(pidlist[i]), signal.SIGKILL)
        killCommand="sudo kill -9 "+pidlist[i]
        makeoscall(killCommand)

def stopJamieInstance(serverName, targetfolder):
	#jps -lv | grep "in.handyman.server.HandymanServer" | awk '{print $1}'
	#ps -ef | grep /home/jpvel/autodeploy/jammiddleware | grep in.juno.bonsaicrm.Application
	serverPidCommand="sudo ps -ef | grep java |grep \""+targetfolder+"\""+"| grep \""+serverName+"\" | awk '{print $2}'"
	logger.info("Finding server pid for process with %s", serverPidCommand)
	pid=makeoscall(serverPidCommand)
	logger.info("Retrieved server pid %s, for process with %s", pid, serverName)
	killCommand="sudo kill -9 "+pid
	makeoscall(killCommand)

def buildCandyman(targetfolder,branch,giturl):
	checkoutCandyManSource(targetfolder,branch,giturl)
	runMavenForCandymanBuild(targetfolder+"/handyman/handyman.parent")
	runDefaultMavenBuild(targetfolder+"/candyman")

def startCandyman(targetfolder):
	changeDir(targetfolder+"/candyman")
	launchCommand="./starthandyman.sh"
	logger.info("Starting candy man using command %s",launchCommand)
	makeoscallbg(launchCommand)

def buildJamie(targetfolder,branch,giturl):
	checkoutJamieSource(targetfolder,branch,giturl)
	runSudoDefaultMavenBuild(targetfolder+"/jammiddleware")

def startJamie(targetfolder):
	stopApacheCommand="sudo /etc/init.d/apache2 stop"
	logger.info("Stopping apache2 using command %s",stopApacheCommand)
	makeoscall(stopApacheCommand)
	changeDir(targetfolder)
	logger.info("Starting Juno middle ware server using command %s", targetfolder+"/jammiddleware")
	launchCommand="sudo mvn spring-boot:run>output.log&"
	makeoscallbg(launchCommand)

def gitClone(targetfolder, url, project,branch):
	logger.info("Changing to directory to %s ", targetfolder)	
	changeDir(targetfolder)
	cloneCommand="git clone "+ url
	logger.info("Executing clone command for %s using %s",project, cloneCommand)
	makeoscall(cloneCommand)
	changeDir(targetfolder+"/"+project)
	branchCommand="git checkout "+ branch
	logger.info("Executing branch command for %s using %s",project, branchCommand)
	makeoscall(branchCommand)

def gitPull(targetfolder, branch):
	logger.info("Changing to directory to %s ", targetfolder)	
	changeDir(targetfolder)
	stashCommand="git stash"
	logger.info("Executing stash command for candyman using %s", stashCommand)
	makeoscall(stashCommand)
	pullCommand="git pull origin "+branch
	logger.info("Executing pull command for candyman using %s", pullCommand)
	makeoscall(pullCommand)

def checkoutCandyManSource(targetfolder,branch,giturl):
    logger.info("Creating the checkout directory="+targetfolder)
    createDirectory(targetfolder)
    gitClone(targetfolder, giturl,"candyman",branch)
    handyManUrl="git@github.com:jpvelsamy/handyman.git"
    gitClone(targetfolder,handyManUrl,"handyman",branch)

def checkoutJamieSource(targetfolder,branch,giturl):
    createDirectory(targetfolder)
    gitClone(targetfolder, giturl,"jammiddleware",branch)

def runMavenForCandymanBuild(targetfolder)	:
	logger.info("Changing to directory %s to run maven", targetfolder)	
	changeDir(targetfolder)
	mavenCommand="mvn clean compile net.alchim31.maven:scala-maven-plugin:compile install -Dmaven.test.skip=true"
	logger.info("Executing maven command  %s", mavenCommand)
	makeoscall(mavenCommand)

def runDefaultMavenBuild(targetfolder)	:
	logger.info("Changing to directory %s to run maven", targetfolder)	
	changeDir(targetfolder)
	mavenCommand="mvn clean compile install -Dmaven.test.skip=true"
	logger.info("Executing maven command  %s", mavenCommand)
	makeoscall(mavenCommand)

def runSudoDefaultMavenBuild(targetfolder)	:
	logger.info("Changing to directory %s to run maven", targetfolder)	
	changeDir(targetfolder)
	mavenCommand="sudo mvn clean compile install -Dmaven.test.skip=true"
	logger.info("Executing maven command  %s", mavenCommand)
	makeoscall(mavenCommand)	


def removeDirectory(directoryName):
    logger.info("Removing the directory="+directoryName)
    try:
        shutil.rmtree(directoryName, ignore_errors=True)
        removeCommand="sudo rm -rf "+directoryName
        logger.info("Executing  command  %s", removeCommand)
	makeoscall(removeCommand)	
    except OSError:
        logger.fatal("Directory="+directoryName+" cannot be removed")
        raise RuntimeError("Directory ="+directoryName+" cannot be removed even after force removal")
    
def createDirectory(directoryName):    
    try:
        os.makedirs(directoryName)
    except OSError:
        if os.path.exists(directoryName):
            # We are nearly safe
            logger.fatal("Directory="+directoryName+" already exists, leaving it as is")
                #raise RuntimeError("Directory already exists, you may not want clone, check and rerun")        

main()	
