from basic_tester import *
from pyspark.sql.functions import *

def checkExerciseCorrectAns(sqlContext, inputs, func_teacher, func_student, TestFunction, exerciseNumber,
                           multiInputs=False):
    outputs = []
    for input in inputs:
        if multiInputs == True:
            tmpAns = func_teacher(input[0], input[1], sqlContext)
        else:
            tmpAns = func_teacher(input[0], sqlContext)

        outputs.append([tmpAns, type(tmpAns)])
    checkExercise(sqlContext, inputs, outputs, func_student, TestFunction, exerciseNumber , multiInputs=multiInputs)
    
    
def func_ex_3(csv_filepath, sqlContext):
    city_df = sqlContext.read.csv(csv_filepath, header = True)
    city_df.printSchema()
    count = city_df.filter(city_df.name.like("%city%")).count()
    return count

def exercise_3(sqlContext, pickleFile, func_student):
    input_file = '../../Data/city_master.csv'
    inputs = [ [input_file] ]
    checkExerciseCorrectAns(sqlContext, inputs, func_ex_3, func_student, TestNumber, 'ex_3' , multiInputs=False)
    
def gen_exercise_3(pickleFile, sqlContext):
    inputs = [["../../Data/city_student.csv"]]
    GenPickle(sqlContext, func_ex_3, inputs, pickleFile, "ex_3", multiInputs=False)

    
def func_ex_2(parquet_path, n, sqlContext):
    makes_df = sqlContext.read.parquet(parquet_path)
    makes_df.printSchema()
    makes_table = makes_df.createOrReplaceTempView("makes_table")
    query='SELECT make_country, count(*) as count  FROM makes_table group by make_country'
    query_result_df = sqlContext.sql(query).sort(desc("count"))
    result = query_result_df.rdd.map(lambda x:(str(x["make_country"]), x["count"])).take(n)
    return result

def exercise_2(sqlContext, pickleFile, func_student):
    input_file = '../../Data/makes_master.parquet'
    inputs = [ [input_file,5] ]
    checkExerciseCorrectAns(sqlContext, inputs, func_ex_2, func_student, TestList, 'ex_2' , multiInputs=True)
    
def gen_exercise_2(pickleFile, sqlContext):
    inputs = [["../../Data/makes.parquet", 3]]
    GenPickle(sqlContext, func_ex_2, inputs, pickleFile, "ex_2", multiInputs=True)
    
def func_ex_1(json_filepath, n, sqlContext):
    makes_df = sqlContext.read.json(json_filepath)
    makes_df.printSchema()
    group_by_country_df = makes_df.filter("make_is_common == 1").groupby("make_country").count()
    df = group_by_country_df.rdd.filter(lambda x: x["count"] > n)
    return df.map(lambda x: str(x["make_country"])).collect()

def exercise_1(sqlContext, pickleFile, func_student):
    input_file = '../../Data/makes_master.json'
    inputs = [ [input_file,5] ]
    checkExerciseCorrectAns(sqlContext, inputs, func_ex_1, func_student, TestList, 'ex_1' , multiInputs=True)
    
def gen_exercise_1(pickleFile, sqlContext):
    inputs = [["../../Data/makes.json", 3]]
    GenPickle(sqlContext, func_ex_1, inputs, pickleFile, "ex_1", multiInputs=True)
    
