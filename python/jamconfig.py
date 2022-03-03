import os
from os.path import expanduser
class Configuration:
    def __init__(self, commandLineArgument, sysCfg):
        self.commandName=commandLineArgument.command        
        self.checkoutDirectory=sysCfg.get("build","checkout-dir")
        self.environment=sysCfg.get("build","environment")
        self.skipTest=sysCfg.get("build","should-skip-unit-test")
        self.archive=sysCfg.get("common","archive-folder")        
        self.pkeyPath=sysCfg.get("common","private-key-path")
        self.javaHome=sysCfg.get("common","java-home")
        self.machineList=sysCfg.get("common","machine-list")
        self.deploymentUser=sysCfg.get("common","user")        
        self.homeFolder=sysCfg.get("common","home-folder")
        self.branch=sysCfg.get("common","branch")
        self.archiveFolder=sysCfg.get("common","archive-folder")
        self.candymanVersion=sysCfg.get("release","candyman-version")
        self.candymanMavenBuild=sysCfg.get("candyman","maven-build-command")
        self.candymanMavenStart=sysCfg.get("candyman","maven-start-command")
        self.candyServerFqn=sysCfg.get("candyman","server-fqn")
        self.candymanGit=sysCfg.get("candyman","git-url")
        self.jamieMavenBuild=sysCfg.get("jamie","maven-build-command")
        self.jamieMavenStart=sysCfg.get("jamie","maven-start-command")
        self.jamieServerFqn=sysCfg.get("jamie","server-fqn")
        self.jamieGit=sysCfg.get("jamie","git-url")       

        self.sysConfigObject=sysCfg

    def getJamieServerName(self):
        return self.jamieServerFqn

    def getBranch(self):
        return self.branch

    def getPrivateKeyPath(self):
        return self.pkeyPath

    def getCommand(self):
        return self.pkeyPath        

    def shouldSkipTest(self):
        return self.skipTest
    
    def getCheckoutDirectory(self):
        return self.checkoutDirectory

    def getMachineList(self):
        return self.machineList

    def getDestLocation(self):        
        return self.target

    def getDeployUser(self):
        return self.deploymentUser

    def getPrivateKeyPath(self):
        return self.pkeyPath

    def getArchiveFolder(self):
        return self.archiveFolder

    def getJavaHome(self):
        return self.javaHome

    def getUserHome(self):
        home = expanduser("~")
        return home

    def getHomefolder(self):
        return self.homeFolder        

    def getCandymanGit(self):
        return self.candymanGit

    def getCandymanMavenBuildCommand(self):
        return self.candymanMavenBuild

    def getCandymanMavenStartCommand(self):
        return self.candymanMavenStart

    def getCandyServerName(self):
        return self.candyServerFqn        

    def getJamieGit(self):
            return self.jamieGit

    def getJamieMavenBuildCommand(self):
        return self.jamieMavenBuild

    def getJamieMavenStartCommand(self):
        return self.jamieMavenStart        

