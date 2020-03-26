#!/usr/bin/env python3
""" A module for collecting statistics about the performance of the memory Heirarchy
"""
import numpy as np
from time import time
from os.path import isdir
from os import mkdir,chdir,getcwd
import traceback,sys
import shutil, psutil
from numpy.random import rand

def measureRandomAccess(size,filename='',k=1000):
    """Measure the distribution of random accesses in computer memory.

    :param size: size of memory block.
    :param filename: a file that is used as an external buffer. If filename==`` then everything is done in memory.
    :param k: number of times that the experiment is repeated.
    :returns: (mean,std,T):
              mean = the mean of T
              std = the std of T
              T = a list the contains the times of all k experiments
    :rtype: tuple

    """
    # Prepare buffer.
    A=None
    if filename == '':
        inmem=True
        t_alloc_0=time()
        A=np.ones(size,dtype=np.ubyte)
        t_alloc_1 = time()
    else:
        inmem=False
        t_alloc_0=time()
        file=open(filename,'r+')
        t_alloc_1=time()
    dt_alloc = t_alloc_1-t_alloc_0    
    # Read and write k times from/to buffer.
    sum=0; sum2=0
    T=np.zeros(k)

    try:
        for i in range(k):
            if (i%10000==0): print('\r',i, end=' ')
            loc=int(rand()*(size-0.00001))
            if size==0:
                t=time()
                d=time()-t
            elif inmem:
                t=time()
                x=A[loc]
                A[loc]=x+1
                d=time()-t
            else:
                t=time()
                file.seek(loc)
                x=file.read(1)
                file.write('x')
                d=time()-t
            T[i]=d
            sum += d
            sum2 += d*d
        mean=sum/k; var=(sum2/k)-mean**2; std=np.sqrt(var)
    except:
        print('bad loc',size,inmem,loc)
        traceback.print_exc(file=sys.stdout)
    if not inmem:
        file.close()
    return (dt_alloc,mean,std,T)
        
#######

def create_file(n,m,filename='DataBlock'):
    """Create a scratch file of a given size.

    :param n: size of block
    :param m: number of blocks
    :param filename: desired filename
    :returns: time to allocate block of size n, time to write a file of size m*n
    :rtype: tuple

    """
    t1=time()
    A=np.ones(n,dtype=np.ubyte)
    t2=time()
    print(A.shape)
    file=open(filename,'wb')
    for i in range(m):
        file.write(A)
        if i % 100 == 0:
            print('\r',i,",", end=' ')
    file.close()
    t3=time()
    print('\rcreating %d byte block: %f sec, writing %d blocks %f sec' % (n,t2-t1,m,t3-t2))
    return ((t2-t1)/n,(t3-t2)/(n*m))
#######

def create_all_files(sizes):
    """Create all files.

    Parameters
    ----------
    sizes : a list of lists of the form [(filesize,[block_size_1, block_size_2,...])]

    Returns
    -------
    List of file names, a dictionary of measurements

    """
    Stats=[]; files=[]
    try:
        for file_size,block_sizes in sizes:
            for block_size in block_sizes:
                n=block_size
                m=int(file_size/block_size)
                assert n*m==file_size , 'file_size=%d is not a multiple of block_size=%d'%(file_size,n)
                filename='BlockData'+str(file_size)
                (t_mem,t_disk) = create_file(n,m,filename=filename)
                Stats.append({'n':n,
                              'm':m,
                              't_mem':t_mem,
                              't_disk':t_disk})
            files.append(filename)
    except:
        traceback.print_exc(file=sys.stdout)
    return files, Stats


def pokes(size_list,k):
    
    L=len(size_list)
    print(L)
    
    _mean=np.zeros([2,L])   #0: using disk, 1: using memory
    _std=np.zeros([2,L])
    T=np.zeros([2,L,k])

    Random_pokes=[]
    try:
        for m_i in range(len(size_list)):
            print(m_i)
            file_size,_list = size_list[m_i]   
            
            (dt_alloc,_mean[0,m_i],_std[0,m_i],T[0,m_i]) = measureRandomAccess(file_size,filename='BlockData'+str(file_size),k=k)
            T[0,m_i]=sorted(T[0,m_i])
            print('\rFile pokes _mean='+str(_mean[0,m_i])+', file _std='+str(_std[0,m_i]))

            (dt_alloc,_mean[1,m_i],_std[1,m_i],T[1,m_i]) = measureRandomAccess(file_size,filename='',k=k)
            T[1,m_i]=sorted(T[1,m_i])
            print('\rMemory pokes _mean='+str(_mean[1,m_i])+', Memory _std='+str(_std[1,m_i]))

            Random_pokes.append({'size':file_size,
                                 'dt_alloc':dt_alloc,
                                 'memory__mean': _mean[1,m_i],
                                 'memory__std': _std[1,m_i],
                                 'file__mean': _mean[0,m_i],
                                 'file__std': _std[0,m_i],
            })
    except:
        Random_pokes.append({'m_i':m_i,
                             'file_size':file_size,
                             'failed':'failed' # It would be neat to log
                                               # the error mesage here
            })
        traceback.print_exc(file=sys.stdout)

    print('='*50)
    return Random_pokes,files

def find_available_space(path):
    
    DU = shutil.disk_usage(path)
    MU = psutil.virtual_memory()
    return {'Disk':DU,\
            'Mem':MU}


def consec_disk_reads(files):
    consec_read=[]
    try:
        ### Computing could be made faster and more memory efficient using streaming 
        for file in files:
            t0 = time()
            M=np.fromfile(file,dtype=np.byte,count=-1)
            t1=time()
            np.sum(M)
            t2=time()
            read_time= t1-t0
            calc_time= t2-t1
            L=max(1,M.shape[0])
            Vars={'file':file,'L':L,'read_time':read_time,'read_time_per_byte':read_time/L,\
                  'calc_time':calc_time,'calc_time_per_byte':calc_time/L}
            consec_read.append(Vars)
    except:
        print('fail in consec_disk_reads')
        traceback.print_exc(file=sys.stdout)
        consec_read.append((file,'fail'))
    return consec_read

if __name__=='__main__':
    exec_dir=getcwd()
    scratch_dir='scratch'
    available = find_available_space(scratch_dir)       
    #max_size is 80% of the mximal size between memory and disk
    max_size = int(0.8*min(available['Disk'].free,available['Mem'].available))
    log_dir=scratch_dir+'/measurement_logs/'
    if not isdir(log_dir):
        mkdir(log_dir)
    chdir(log_dir)
        
    stats={} # dict that contains all of the statistics

    PP = [10**i for i in range(11)]
    size_list=[(PP[3],[PP[1],PP[2],PP[3]]),\
               (PP[6],[PP[4],PP[5],PP[6]]),\
               (PP[9],[PP[6],PP[9]]),\
               (int(PP[10]/2),[PP[6],PP[9]])]
        
    # remove from size_list elements whose total size is larger than max_size for this machine
    trimmed_size_list=[]
    for element in size_list:
        if element[0]<=max_size:
            trimmed_size_list.append(element)
            
    size_list=trimmed_size_list
    
    print('size_list=',size_list)
    print('maximal_size(GB)=%3.3f'%(max_size*1.0e-9))
          
#%%
    files,creation_stats=create_all_files(size_list)
    stats['creation_stats']=creation_stats
    print('done creating files')

#%%    
    stats['consec_disk_reads']=consec_disk_reads(files)
#%%   
    stats['Random_pokes'], files = pokes(size_list,k=1000)
#%%    
#%%   
   
    import pickle as pk
    chdir(exec_dir)
    with open('stats.pkl','wb') as stats_pkl:
        pk.dump(stats,stats_pkl,protocol=pk.HIGHEST_PROTOCOL)
