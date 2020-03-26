import numpy as np

from Tester import *

###   Exercise 1   ###
def func_ex1_1(A):
    return A.map(np.cos)   
def gen_exercise1_1(pickleFile, sc):
    inputs= [range(3), range(4,12), range(-4,0) ]
    GenPickle(sc, func_ex1_1, inputs, pickleFile, "ex1_1" )
def exercise1_1(pickleFile, func_student, sc):    
    inputs= [ [np.pi,0,100000,np.pi*10,np.log(44),-49.4902],  range(39,45) ]
    checkExerciseCorrectAns(inputs, func_ex1_1, func_student, TestRDD, 'ex1_1', sc) 
    
###   Exercise 2   ###
def func_ex1_2(stringRDD):
    return stringRDD.map(lambda x: x.split() )
def gen_exercise1_2(pickleFile, sc):
    inputs = [ ["Spring quarter", "Learning spark basics", "Big data analytics with Spark"],
               ["Do not go gentle", "into that good night", "old age should burn and rave"],
               ["do","I dare disturb","the universe","there will be time there will be","time"] ]
    GenPickle(sc, func_ex1_2, inputs, pickleFile, "ex1_2" )
def exercise1_2(testPath, func_student, sc):    
    inputs = [ ["ah", "ah ah ah", "ha ai ifo aoisdmf"],
               ["asdio", "i", "asdfasd","aasdf"],
               ["do asdnj aksdo adsof aos asod oasdf  mkmasdkf maso asdf okm"] ]
    checkExerciseCorrectAns(inputs, func_ex1_2, func_student, TestRDDStr, 'ex1_2', sc)
        
###   Exercise 3   ###
def func_ex1_3(stringRDD):
    return stringRDD.reduce(max)
def gen_exercise1_3(pickleFile, sc):
    inputs = [ [0,4,2,3,1],[-3.2,-3.233,-3.1,-3.9],[2,2,2,2,2,2] ]
    GenPickle(sc, func_ex1_3, inputs, pickleFile, "ex1_3",  isRDD=False )
def exercise1_3(testPath, func_student, sc):
    inputs = [ [0,3.49,2.4922,5.24,-24], [-3.01,-3.20,-3.001,-3.4], [7] ]
    checkExerciseCorrectAns(inputs, func_ex1_3, func_student, TestNumber, 'ex1_3', sc, isRDD=False)

        
###   Exercise 4   ###
def func_ex1_4(mapwords):
    return mapwords.reduce(lambda x,y: x+" "+y)
def gen_exercise1_4(pickleFile, sc):
    inputs = [["Spring quarter", "Learning spark basics", "Big data analytics with Spark"],
              ["Do not go gentle", "into that good night", "old age should burn and rave"] ,
              ["do","I dare disturb","the universe","there will be time there will be","time"] ]
    GenPickle(sc, func_ex1_4, inputs, pickleFile, "ex1_4",  isRDD=False )
def exercise1_4(testPath, func_student, sc): 
    inputs = [["ah", "ah ah ah", "ha ai ifo aoisdmf"] ,
              ["asdio", "i", "asdfasd","aasdf"] ,
              ["do asdnj aksdo adsof aos asod oasdf  mkmasdkf maso asdf okm"] ]
    checkExerciseCorrectAns(inputs, func_ex1_4, func_student, TestListStr, 'ex1_4', sc, isRDD=False)


###   Exercise 5   ###
def func_ex1_5(x,y):
    return [max(x+y)]

def gen_exercise1_5(pickleFile, sc):
    def func_ex1_5(x,y):
        return [max(x+y)]
    inputs = [ [[15,20],[21,14],[18,4,20]],
               [[3,4,5,-3,19],[19.1],[7,-11]],
               [[-3.2,-3.233,-3.9],[-4],[-3,-5]]  ]
    GenPickle(sc, RddReduce(func_ex1_5), inputs, pickleFile, "ex1_5",  isRDD=False )
def exercise1_5(testPath, func_student, sc):  
    def func_ex1_5(x,y):
        return [max(x+y)]
    inputs = [ [[3,4],[2,1],[7,9]], [[-222],[-10,-33],[0,-5]], [[3.2,3.3,3.1,3.9],[-3.95],[3.4,3.7]]  ]
    checkExerciseCorrectAns(inputs,
                            lambda x: x.reduce(func_ex1_5), lambda y: y.reduce(func_student),
                            TestList, 'ex1_5', sc, isRDD=False)
        