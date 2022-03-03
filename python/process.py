import logging
import os
import sys
import subprocess
import pwd
import io
import jamcommons
import spur
import spur.ssh
import time

logger = logging.getLogger("Jam-Commcenter")

class Jamie:
	def __init__(self, configObject):
		self.configObject=configObject
		self.machineList=self.configObject.getMachineList()
		self.destFolder=self.configObject.getCheckoutDirectory()
		self.user=self.configObject.getDeployUser()
		self.archiveFolder=self.configObject.getArchiveFolder()
		self.machineListArr=self.machineList.split(',')
		self.privateKey=self.configObject.getPrivateKeyPath()
		self.buildCommand =self.configObject.getJamieMavenBuildCommand()
		self.startCommand=self.configObject.getJamieMavenStartCommand()
		self.serverName=self.configObject.getJamieServerName()
		self.gitUrl=self.configObject.getJamieGit()
		self.remoteHome=self.configObject.getHomefolder()
		self.branch=self.configObject.getBranch()

	def installjamie(self):
		logger.info("Starting  to perform jamie install sequence using user %s with privateKey %s",self.user, self.privateKey)        		
		for machine in self.machineListArr:
			logger.info("Initiating installation seq(pushcode->stopapp->build->startapp) for %s",machine)
			self.pushstopScript(machine)           			
			logger.info("Completed pushing commands and configuration for %s and initiating install",machine)
			self.install(machine)
		logger.info("Completed  jamie install sequence using user %s with privateKey %s",self.user, self.privateKey)        		

	def pushstopScript(self,machine):
		scpCommand="scp -v python/remote.jam.py ./jam.cfg "+self.user+"@"+machine+":"+self.remoteHome+os.sep
		logger.info("Executing scp command %s for machine %s",scpCommand,machine)
		jamcommons.makeoscall(scpCommand)
		return self            	

	def install(self,machine):
                command=["python2.7","remote.jam.py","--command","installjamie","--serverName","in.juno.bonsaicrm.Application","--branch"," theta","--targetfolder",self.destFolder]
        	logger.info("Install sequence jamie application in machine %s using command %s",machine, command)
                self.executeRemoteCommand(command, machine)
                return self
	
        def stop(self,machine):
      	        command=["python2.7","remote.jam.py","--command","stopjamie","--serverName","in.juno.bonsaicrm.Application","--targetfolder",self.destFolder]
        	logger.info("Stopping jamie application in machine %s using command %s",machine, command)
                self.executeRemoteCommand(command, machine)
                return self
	        	

	def build(self,machine):
	        command=["python2.7", "remote.jam.py", "--command", "buildjamie","--branch",self.branch,"--targetfolder",self.destFolder,"--giturl ",self.gitUrl]   	
                logger.info("Building jamie application in machine %s using command %s",machine,command)	   
	        self.executeRemoteCommand(command, machine)
	        return self	
                  	
	
	def start(self,machine):
        	command=["python2.7", "remote.jam.py", "--command", "startjamie","--targetfolder",self.destFolder]   	
        	logger.info("Starting jamie application in machine %s using command %s",machine,command)	     
        	self.executeRemoteCommand(command, machine)
	        return self	        	        			

        def executeRemoteCommand(self, command, machine):
                logger.info("Executing command %s in machine %s",command,machine)
                try:
                        shell=self.createConnection(machine)
                        with shell:
                                result=shell.run(command,cwd=self.remoteHome,allow_error=True)
                                response=result.output
                                logger.info(response)
                                
                except spur.ssh.ConnectionError as error:
                        print(error.original_traceback)
                        raise
                return self
        
	#this method is duplicated, it cannot be done this way, please refactor it
    	def createConnection(self, machine):
        		rShell = spur.SshShell(hostname=machine,username=self.user,private_key_file=self.privateKey)
        		return rShell            			
