#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 10:51:51 2020

@author: yoavfreund
"""
import subprocess
from time import sleep
import argparse

def run_command(command,debug=False):
    if debug:
        print('running ',command)
    p=subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out=p.communicate()
    stdout=out[0].decode()
    stderr=out[1].decode()
    outputs={"stderr":stderr,
             "stdout":stdout}
    if debug:
        print(outputs)
    return outputs
 
class aws_jupyter:
    """
    A python wrapper around the script **aws-jupyter**
    """
    
    def check(self):
        """
        Check on the status of the ec2 instance

        Returns status
        -------
        0 = No instance running under this name 
        
        1 = instance in the process of starting up
        
        2 = instance available        
        
        -1 = Status could not be parsed
        """
        check_cmd = "aws-jupyter check --name %s"%self.name
        self.decoded=run_command(check_cmd)
        stdout=self.decoded['stdout']
        if('The Jupyter Notebook is running on the cluster at the address below.' in stdout):
            print(stdout)
            return 2
        elif("No instance found in the cluster" in stdout):
            return 0
        elif("Cluster is not ready. Please check again later." in stdout):
            return 1
        else:
            print("did not recognize check status")
            print(stdout)
            return -1

    def run(self,scriptname,files=[],credentials="",waitforoutput=True): 
        """
        Run a local script on the remote instance

        Parameters
        ----------
        scriptname : TYPE
            DESCRIPTION.
        files : TYPE, optional
            DESCRIPTION. The default is [].
        credentials : TYPE
            DESCRIPTION.
        waitforoutput : TYPE, optional
            DESCRIPTION. The default is True.

        Returns
        -------
        None.

        """
        return

    def retrieve():
        """ call aws-jupyter retrieve"""
        return
    
    def terminate():
        """ call aws-jupyter terminate"""
        
        
    def __init__(self,name='instance',count=1,_type='t3.large',spot=0):
        """
        Create a cluster of instances on ec2

        Parameters
        ----------
        name : TYPE, optional
            DESCRIPTION. The default is 'instance'.
        count : TYPE, optional
            DESCRIPTION. The default is 1.
        _type : TYPE, optional
            DESCRIPTION. The default is 't3.large'.
        spot : TYPE, optional
            DESCRIPTION. The default is 0.

        Returns
        -------
        None.

        """
        self.name=name
        status=self.check()
        if status==1:
            print("cluster %s not ready yet"%self.name)
            return
        elif status==2:
            print("cluster running")
            return

        create_cmd = "aws-jupyter create -c {count} --name {name} --type {_type}"
        command=create_cmd.format(count=count,name=name,_type=_type)
        if spot>0:
            command.append(" --spot %4.2f"%spot)
        out=run_command(command)
        print("initiated instance:",command)
 
        i=0; wait_period=10
        while True:
            status=self.check()
            if status==2:
                print(stdout)
                break
            print('\r check',i*wait_period,end='')
            i+=1
            sleep(wait_period) 
    
if __name__=="__main__":
    """ Write code that will collect performance data for your analysis """
    instance = aws_jupyter(name="test")
    
 

    
