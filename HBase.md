# HBase
- A type of Nosql DB
- HBase is row oriented
- zookkeeper > HMaster servers > Region Servers > HDFS
- row = uniqueid  column family> columns > cell> versions with timestamp

# Importing Movie ratings into HBase
Python client> restService > HBase > HDFS

# HBase start
- go to Hbase & service_actions > start
- go to virtual box >right click >settings>network>port forwarding> create a new port for HBase REST 
- I created at 8002 port on localhost
- Now ssh into sandbox then change to super user root
``` su root ``` & a****
```usr/hdp/current/hbase-master/bin/hbase-daemon.sh start rest -p 8002 --infoport 8003```
- open canopy & write a python client to get the data from local into HBASE
- pip install starbase which is used to connect to hbase
- To install a pip module- !pip install git+https://github.com/barseghyanartur/starbase@stable#egg=starbase --upgrade
- To list all installed pip modules- !pip list
- To run python file in canopy- %run "~/Documents/ULTIMATE HADOOP/Untitled.py"

``` python
from starbase import Connection

c = Connection("127.0.0.1", "8002")

ratings = c.table('ratings')

if(ratings.exists()):
    print("Dropping existing ratings table \n")
    ratings.drop()
    
ratings.create('rating')

print("Parsing the ml-100 ratings data... \n")
ratingFile = open("~/Documents/ULTIMATE HADOOP/ml-100k/u.data","r")
batch = ratings.batch()

for line in ratingFile:
    (userID,movieID,rating,timestamp) = line.split()
    batch.update(userID, {'rating': {movieID:rating}})
    
ratingFile.close()

print("committing ratings data to HBase via REST service \n")
batch.commit(finalize=True)

print("Get back ratings for some users..\n")
print("Ratings for user ID 1:\n")
print(ratings.fetch("1"))
print("ratings for user ID 2:\n")
print (ratings.fetch("33")) 
    ```

