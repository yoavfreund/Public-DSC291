import numpy as np
from Tester import *
import re

def map_kmers_correct(text,k):
    # text: an RDD of text lines. Lines contain only lower-case letters and spaces. Spaces should be ignored.
    # k: length of `k`-mers
    def kgram(sentence):
        set=[]
        for i in range(len(sentence)-k+1):
            set.append((tuple(sentence[i:i+k]),1))
        return set
    singles = text.map(lambda x: x.split())\
                .filter(lambda x: x != '').flatMap(kgram)
    return  singles
    # singles: an RDD of pairs of the form (tuple of k words,1)
def count_kmers_correct(singles):
    # singles: as above
    return singles.reduceByKey(lambda x,y: x+y)
    # count: RDD of the form: (tuple of k words, number of occurances)
def sort_counts_correct(count):
    # count: as above
    return count.map(lambda x: (x[1],x[0])).sortByKey(False)
    # sorted_counts: RDD of the form (number of occurances, tuple of k words) sorted in decreasing number of
    
def getkmers(text_file, l,k, map_kmers, count_kmers, sort_counts):
    # text_file: the text_file RDD read above
    # l: will print the l most common 3mers
    
    # Do Not modify this function
    def removePunctuation(text):
        return re.sub("[^0-9a-zA-Z ]", " ", text)
    text = text_file.map(removePunctuation)\
                    .map(lambda x: x.lower())
    singles=map_kmers(text,k)
    count=count_kmers(singles)
    sorted_counts=sort_counts(count)
    return sorted_counts
    
def exercise(pickleFile, map_kmers, count_kmers, sort_counts, sc):
    text_file = sc.textFile(u'../../Data/Moby-Dick.txt')
    for l,k in zip([10,20,7],[3,5,3]):
        func_teacher = lambda RDD: getkmers(RDD, l,k, map_kmers_correct, count_kmers_correct, sort_counts_correct)
        case = func_teacher(text_file)
        func_student = lambda RDD: getkmers(RDD, l,k, map_kmers, count_kmers, sort_counts)
        noError = TestRDDK( data=text_file, func_student=func_student, corAns=case.take(l), corType=type(case), takeK=l, toPrint=False)
        if noError == False: raise AssertionError('Your Answer is Incorrect') 
        print 
    
def gen_exercise(pickleFile, sc):
    text_file = sc.textFile(u'../../Data/Moby-Dick.txt')
    l = 5
    k = 3
    func_teacher = lambda RDD: getkmers(RDD, l,k, map_kmers_correct, count_kmers_correct, sort_counts_correct)
    
    try:
        f = open(pickleFile,'r')
        toPickle = pickle.load(f)
        f.close()
    except:
        toPickle = {}
    exData = []
    tmpAns = func_teacher(text_file)
    exData.append([ tmpAns.take(l)  , 
                      type(tmpAns) ])
    
    toPickle['ex4'] = {'inputs': [''], 'outputs':exData}
    f = open(pickleFile,'w')
    pickle.dump(toPickle,f)
    f.close()
    