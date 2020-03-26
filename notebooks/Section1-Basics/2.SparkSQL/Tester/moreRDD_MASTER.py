import numpy as np
import urllib

from Tester import *




###   Import Dataset  ###
def getData(sc):
    f = urllib.urlretrieve ("http://kdd.ics.uci.edu/databases/kddcup99/kddcup.data_10_percent.gz", "kddcup.data_10_percent.gz")
    data_file = "./kddcup.data_10_percent.gz"
    return sc.textFile(data_file).filter(lambda x: np.random.uniform()<.5  ).cache()


###   Exercise 1   ###
def func_ex1(raw_data):
    return raw_data.map(lambda x: (x.split(",")[-1], x.split(",")) )
def gen_exercise1(pickleFile, data, sc):
    GenPickle_RDD(sc, func_ex1, data, pickleFile, 'ex1', takes=3 )
def exercise1(pickleFile, func_student, data, sc):  
    noError= TestRDDK(data=data, func_student=func_student, corAns=func_ex1(data).take(3), corType=type(func_ex1(data)), takeK=3)
    if noError == False: raise AssertionError('Your Answer is Incorrect') 
        
        
###   Exercise 2   ###
def func_ex2(data):
    return func_ex1(data) \
            .mapValues(lambda x: int(x[0]) ) \
            .reduceByKey(lambda x,y: x+y)  \
            .map(lambda x: (x[1],x[0]) ) \
            .sortByKey(False) \
            .map(lambda x: (x[1],x[0])) 
def gen_exercise2(pickleFile, data, sc):
    #RDD = func_ex1(data)
    GenPickle_RDD(sc, func_ex2, data, pickleFile, 'ex2', takes=5 )
def exercise2(pickleFile, func_student, data, sc):  
    #RDD = func_ex1(data)
    noError= TestRDDK(data=data, func_student=func_student, corAns=func_ex2(data).take(5), corType=type(func_ex2(data)), takeK=5)
    if noError == False: raise AssertionError('Your Answer is Incorrect')         
            
            

###   Exercise 3   ###      
def func_ex3(data):
    return func_ex1(data) \
        .mapValues(lambda x: int(x[0]) ) \
        .combineByKey(
            (lambda x: (x, 1)),
            (lambda acc, value: (acc[0]+value, acc[1]+1)),
            (lambda acc1, acc2: (acc1[0]+acc2[0], acc1[1]+acc2[1])) ) \
        .sortByKey() \
        .mapValues(lambda value: value[0]*1.0/value[1]) 
def gen_exercise3(pickleFile, data, sc):
    GenPickle_RDD(sc, func_ex3, data, pickleFile, 'ex3', takes=9 )

def exercise3(pickleFile, func_student, data, sc): 
    corAns=func_ex3(data).take(9)
    corType=type(func_ex3(data))
    takeK=9
    
    initDebugStr = data.toDebugString() 
    studentRDD = func_student(data)
    print "Input: "+ str(type(data)) 
    print "Correct Output: " + str(corAns)
    
    newDebugStr  = studentRDD.toDebugString()
    initDebugStr = '|'.join(initDebugStr.split('|')[-1:])[3:50]

    try: assert( initDebugStr.replace(' ','') in newDebugStr.replace(' ','') )
    except AssertionError as e:
        print "\nError: Did you use only Spark commands? Original RDD is not found in execution path."
        return False

    try:
        studentAns = studentRDD.take(takeK)
        for i in range(9):
            assert studentAns[i][0] == corAns[i][0]
            assert  abs(studentAns[i][1]-corAns[i][1]) < 0.0005
    except AssertionError as e:
        print "\nError: Function returned incorrect output"
        print "Your Output: ",studentRDD.take(takeK)
        return False
    
    print "Great Job!"
    return True


        
        
        
        
        