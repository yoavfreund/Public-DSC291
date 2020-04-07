#!/usr/bin/env python3

import multiprocessing 
from numpy import *
import numpy as np
from time import time
from os.path import isfile,isdir
from os import mkdir,chdir,getcwd

def multiprocessing_compute(x):
    s=0
    for i in range(10**7):
        s+=i*i
    print('process %d: %d iterations'%(x,i))

def multiprocessing_read(i):
    with open('GB%d'%i,'rb') as file:
        A=file.read()
    print('read copy%d len=%d'%(i,len(A)))

def multi_process(F=multiprocessing_read,max_par=4):
    Times=[0.]
    for j in range(1,max_par):
        starttime = time()
        processes = []
        print('number of processes=%d'%j)
        for i in range(0,j):
            p = multiprocessing.Process(target=F, args=(i,))
            processes.append(p)
            p.start()

        for process in processes:
            process.join()
        DT = time() - starttime
        Times.append(DT)
        print('That took {} seconds'.format(DT))
    return Times

if __name__=="__main__":
    #prepare 2GB files to read
    exec_dir=getcwd()
    scratch_dir='scratch'
    #scratch_dir='/home/ubuntu/spda'
    log_dir=scratch_dir+'/measurement_logs/'
    if not isdir(log_dir):
        mkdir(log_dir)
    chdir(log_dir)

    GB=random.rand(2**27)
    for i in range(2):
        with open('GB%d'%i,'wb') as file:
            file.write(GB)

    stats={}
    stats['Times_compute'] = multi_process(F=multiprocessing_compute,max_par=10)
    stats['Times_read'] = multi_process(F=multiprocessing_read,max_par=10)
    import pickle as pk
    chdir(exec_dir)
    with open('multi_processing_stats.pkl','wb') as stats_pkl:
        pk.dump(stats,stats_pkl,protocol=pk.HIGHEST_PROTOCOL)
