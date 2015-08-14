# Kicking the tires on MongoDB

"""
Your task is to sucessfully run the exercise to see how pymongo works
and how easy it is to start using it.
You don't actually have to change anything in this exercise,
but you can change the city name in the add_city function if you like.

Your code will be run against a MongoDB instance that we have provided.
If you want to run this code locally on your machine,
you have to install MongoDB (see Instructor comments for link to installation information)
and uncomment the get_db function.
"""

def add_city(db):
    # Changes to this function will be reflected in the output. 
    # All other functions are for local use only.
    # Try changing the name of the city to be inserted
    db.cities.insert({"name" : "Chicago"})
    
def get_city(db):
    return db.cities.find_one()

def get_db():
    # For local use
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    # 'examples' here is the database name. It will be created if it does not exist.
    db = client.examples
    return db

if __name__ == "__main__":
    # For local use
    # db = get_db() # uncomment this line if you want to run this locally
    add_city(db)
    print get_city(db)
    

# 	Finding Porsche

#!/usr/bin/env python
"""
Your task is to complete the 'porsche_query' function and in particular the query
to find all autos where the manufacturer field matches "Porsche".
Please modify only 'porsche_query' function, as only that will be taken into account.

Your code will be run against a MongoDB instance that we have provided.
If you want to run this code locally on your machine,
you have to install MongoDB and download and insert the dataset.
For instructions related to MongoDB setup and datasets please see Course Materials at
the following link:
https://www.udacity.com/wiki/ud032
"""

def porsche_query():
    # Please fill in the query to find all autos manuafactured by Porsche.
    query = {"manufacturer" : "Porsche"}
    return query


# Do not edit code below this line in the online code editor.
# Code here is for local use on your own computer.
def get_db(db_name):
    # For local use
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client[db_name]
    return db

def find_porsche(db, query):
    # For local use
    return db.autos.find(query)


if __name__ == "__main__":
    # For local use
    db = get_db('examples')
    query = porsche_query()
    p = find_porsche(db, query)


# Inserting Multiple Documents

#!/usr/bin/env python
""" 
Add a single line of code to the insert_autos function that will insert the
automobile data into the 'autos' collection. The data variable that is
returned from the process_file function is a list of dictionaries, as in the
example in the previous video.
"""

from autos import process_file


def insert_autos(infile, db):
    data = process_file(infile)
    # Add your code here. Insert the data in one command.
    for a in data:
        db.autos.insert(a)
  
if __name__ == "__main__":
    # Code here is for local use on your own computer.
    from pymongo import MongoClient
    client = MongoClient("mongodb://localhost:27017")
    db = client.examples

    insert_autos('autos-small.csv', db)
    print db.autos.find_one()


# 	Range Queries

#!/usr/bin/env python
"""
Your task is to write a query that will return all cities
that are founded in 21st century.
Please modify only 'range_query' function, as only that will be taken into account.

Your code will be run against a MongoDB instance that we have provided.
If you want to run this code locally on your machine,
you have to install MongoDB, download and insert the dataset.
For instructions related to MongoDB setup and datasets please see Course Materials.
"""

from datetime import datetime
    
def range_query():
    # Modify the below line with your query.
    # You can use datetime(year, month, day) to specify date in the query
    query = {'foundingDate': {"$gt" : datetime(2000, 12, 31)}}
    return query

# Do not edit code below this line in the online code editor.
# Code here is for local use on your own computer.
def get_db():
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client.examples
    return db

if __name__ == "__main__":
    # For local use
    db = get_db()
    query = range_query()
    cities = db.cities.find(query)

    print "Found cities:", cities.count()
    import pprint
    pprint.pprint(cities[0])


# 	Using $in Operator

#!/usr/bin/env python
"""
Your task is to write a query that will return all cars manufactured by
"Ford Motor Company" that are assembled in Germany, United Kingdom, or Japan.
Please modify only 'in_query' function, as only that will be taken into account.

Your code will be run against a MongoDB instance that we have provided.
If you want to run this code locally on your machine,
you have to install MongoDB, download and insert the dataset.
For instructions related to MongoDB setup and datasets please see Course Materials.
"""


def in_query():
    # Modify the below line with your query; try to use the $in operator.
    query = {"manufacturer" : "Ford Motor Company", "assembly": {"$in": [
		"United Kingdom",
		"Germany",
		"Japan"
	]}}
    
    return query


# Do not edit code below this line in the online code editor.
# Code here is for local use on your own computer.
def get_db():
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client.examples
    return db


if __name__ == "__main__":

    db = get_db()
    query = in_query()
    autos = db.autos.find(query, {"name":1, "manufacturer":1, "assembly": 1, "_id":0})

    print "Found autos:", autos.count()
    import pprint
    for a in autos:
        pprint.pprint(a)


# Dot Notation

#!/usr/bin/env python
"""
Your task is to write a query that will return all cars with width dimension
greater than 2.5. Please modify only the 'dot_query' function, as only that
will be taken into account.

Your code will be run against a MongoDB instance that we have provided.
If you want to run this code locally on your machine, you will need to install
MongoDB, download and insert the dataset. For instructions related to MongoDB
setup and datasets, please see the Course Materials.
"""


def dot_query():
    # Edit the line below with your query - try to use dot notation.
    # You can check out example_auto.txt for an example of the document
    # structure in the collection.
    query = {"dimensions.width" : {"$gt": 2.5}}
    return query


# Do not edit code below this line in the online code editor.
# Code here is for local use on your own computer.
def get_db():
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client.examples
    return db


if __name__ == "__main__":
    db = get_db()
    query = dot_query()
    cars = db.cars.find(query)

    print "Found cars:", cars.count()
    import pprint
    pprint.pprint(cars[0])

