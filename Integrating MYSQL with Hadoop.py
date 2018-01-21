 - popular free relational database 
 - Generally monolithic in nature
 - But, can be used for OLTP - so exporting data into MYSQL can be useful
 - Existing data may exist in MYSQL that you want to import to Hadoop to execute more complex queries --- THIS CAN BE DONE BY SQOOP ---
 
 
 SQOOP (SQL + HADOOP)
 It can handle large datasets and import/export them to Hadoop
 It kicks off Mapreduce job to handle import/export of data
 
 
 SQOOP: IMPORT DATA FROM MYSQL TO HDFS
 # this command sucks out movies from mysql table and copies it on hdfs cluster
 
 sqoop import --connect jdbc:mysql://localhost/movielens --driver
 com.mysql.jdbc.Driver --table movies
 
 #INCREMENTAL IMPORTS
 
 --we can keep our relational databsase and Hadoop in sync
 -- --check-coloum and --last-value
 
 SQOOP: EXPORT DATA FROM HIVE TO MYSQL
 # this command sucks out movies from mysql table and copies it on hdfs cluster
 
 sqoop export --connect jdbc:mysql://localhost/movielens -m 1 --driver
 com.mysql.jdbc.Driver --table exported_movies --export-dir
 /apps/hive/warehouse/movies --input-fields-terminated-by '\0001'
 (target table must already exist in MYSQL,with columns in expected order)
 
 # EXAMPLES
 
 #IMPORT MOVIELENS DATA INTO A MYSQL DATABASE
 
 
 #IMPORT THE MOVIES TO HDFS
 
 #IMPORT THE MOVIES INTO HIVE
 
 #EXPORT THE MOVIES BACK INTO MYSQL
 
   
    
 
