import subprocess
import ConfigParser
import os
import platform


def createDirectories(config):
    if os.path.isdir(os.path.join(os.getcwd(), 'COTS'))==False:
        subprocess.call(['mkdir','COTS'])

    for section in config.sections():
        if os.path.isdir(os.path.join(os.getcwd(), '/COTS/'+section))==False:
            subprocess.call(['mkdir','COTS/'+section])

def downloadDependencies(config, plat):

    if plat == 'centos':
        for section in config.sections():
            for (name, version) in config.items(section):
                subprocess.call(['yum','install','--downloadonly', '--downloaddir='+os.path.join(os.getcwd(), 'COTS/'+section)+'/',name, version])
        
    if plat == 'Ubuntu':
        startdir = os.getcwd()
        for section in config.sections():
            os.chdir(os.path.join(os.getcwd(), 'COTS/'+section))

            for (name, version) in config.items(section):
                if version =='':
                    subprocess.call(['apt-get','download', name])
                
                else:
                    subprocess.call(['apt-get','download', name, version])
            
            print(os.getcwd())
            os.chdir(startdir)

if __name__=='__main__':
    config = ConfigParser.ConfigParser()
    config.read('dependencies.ini')
    
    createDirectories(config)

    plat = platform.dist()[0]
    downloadDependencies(config, plat)

