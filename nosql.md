### 
### Student ID:22018083


# NoSQL Data Modeling for Bristol Air Quality Data

For the purpose of this assignment, I decide to choose MogoDB platform for my nosql modelling of the data.

MongoDB is an open-source database developed by MongoDB, Inc. MongoDB stores data in JSON-like documents that may have different structures. Related information is stored together and you can quickly access your queries via the MongoDB query language. MongoDB uses a dynamic schema. That is, you can create a record without first defining a structure such as the type of field or its value. You can change the structure of a record (called a document) simply by adding new fields or deleting existing fields [1]. MongoDB is used  to represent hierarchical relationships and easily store arrays and other more complex structures. Documents in a collection do not have to have the same set of fields, and data denormalization  is common. MongoDB is built with high availability and scalability in mind and includes out-of-the-box replication and automatic sharding.

Below are reasons for my selection.

 * Easy to install.
 * Supports both embedding and referencing of the data.
 * Provide a flexible document schema.


### Definition of Keywords in report
* Collection: A collection is a grouping of MongoDB documents. Documents within a collection can have different fields. A collection is the equivalent of a table in a relational database system. 
* Document: A document is synonymous to rows in relational database.


### Approach for modelling the station data in MongoDB

Mongodb presents different approaches in modelling data. The embedded approach and the referencing or normalized approach. 
I will make use of the embedded approach for modeling the data.
The data from the readings are historical data, there will be no action regarding data update and deletion.
Due to the form of the data and the data will be left in its original form with no referencing or use of foreign keys in modelling the data.


Below is a representation of how the data will be modelled.

The station entity and the reading entity is merged. This represents a document in the station collection

```json
{
   "station_name": "Fishponds Road",
   "station_id": 463,
   "geo_point_2d": "51.4780449714, -2.53523027459",
   "readings": 
       [
          {
             "date_time": "2014-08-22T06:00:00+00:00",
             "station_id": 463,
             "nox": 249.5,
             "no2": 26.75,
             "no": 145.0,
             "pm10": 0,
             "nvpm10": 0,
             "vpm10": 0,
             "nvpm2.5": 0,
             "pm25": 0,
             "vpm2.5": 0,
             "co": 0,
             "o3": 0,
             "so2":0,
             "temperature":0,
             "date_start":"2003-01-01T00:00:00+00:00",
             "date_end": "2015-12-31T00:00:00+00:00",
             "current": false,
             "instrument_type_ref": "Continuous (Refrence)"
          }
    
       ]
}

```

### Implementation of data in MongoDB

### 1. Starting Mongodb service
   After successfully installing mongodb, I started the mongodb service in my terminal by running.
   ``` cmd
   sudo service mongod start
   ```
   
   To start the mongodb session . I used the command below. This grants me access to run mongodb database session.

   ```cmd
      mongosh
   ```


### 2. Monitoring collection 
Collections in nosql are synonymous to tables in relational databases.

```javascript
      // The code below creates a collection with name station. 
      db.createCollection('monitoring_data')
```

### 3. Copy Station Data to Json
Using the python script below I copied the data from Fishponds Road station to a json file by using the modelled structure
The output of the data will be used to insert into the mongodb database.

```python
from sqlalchemy import create_engine
import pandas


engine = create_engine("mysql+pymysql://root:@localhost/pollution-db2")
dbcon = engine.connect()

# Read the first  100 records of the reading table with station id  of 463 and join with the station table
df = pandas.read_sql_query("select * from reading r inner join station s on r.station_id = s.id where r.station_id = 463 limit 100", dbcon)

# Create a dictionary
data = {}
# Add the SiteID, Location and geo_point_2d
data["station_id"] = df["station_id"][0]
data["name"] = df["name"][0]
data["geo_point_2d"] = df["geo_point_2d"][0]

# Create a list of readings
readings = []
# Loop through the data frame and generate a dictionary for each row
for index, row in df.iterrows():
    # Create a dictionary for each row
    reading = {}
    # Add the columns to the dictionary
    reading["Date Time"] = row["Date Time"]
    reading["NOx"] = row["NOx"] or 0
    reading["NO2"] = row["NO2"] or 0
    reading["NO"] = row["NO"] or 0
    reading["PM10"] = row["PM10"] or 0
    reading["NVPM10"] = row["NVPM10"] or 0
    reading["VPM10"] = row["VPM10"] or 0
    reading["NVPM2.5"] = row["NVPM2.5"] or 0
    reading["PM2.5"] = row["PM2.5"] or 0
    reading["VPM2.5"] = row["VPM2.5"] or 0
    reading["CO"] = row["CO"] or 0
    reading["O3"] = row["O3"] or 0
    reading["SO2"] = row["SO2"] or 0
    reading["Temperature"] = row["Temperature"] or 0
    reading["RH"] = row["RH"] or 0
    reading["Air Pressure"] = row["Air Pressure"] or 0
    reading["DateStart"] = row["DateStart"] or ""
    reading["DateEnd"] = row["DateEnd"] or ""
    reading["Current"] = row["Current"]
    reading["Instrument Type"] = row["Instrument Type"]
    # Add the dictionary to the list
    readings.append(reading)

# Add the list of readings to the dictionary
data["readings"] = readings

print(data)


# Close the connection

dbcon.close()

# Write the dictionary to a json file
import json
with open("readings.json", "w") as outfile:
    json.dump(data, outfile)


```


### 4. Bulk Import Reading Data into MongoDB
To import the data from the file into mongodb.  I used the **mongoimport** command from mongodb. This  helper function helps to import bulk data from a json file, csv files.
The syntax for mongoimport:
```cmd
      mongoimport --db dbName --collection collectionName --file fileName.json --jsonArray
```
* dbName  - The name of the database
* collectionName  - The name of the collection
* --file - The absolute path of the file to be imported

To import bulk data from a json file . I used the code below
```zsh
      $ mongoimport --db pllution_db --collection monitoring_data --file readings.json --jsonArray
 ```
Output

```console
      2023-01-15T21:29:19.352+0100    connected to: mongodb://localhost/
      2023-01-15T21:29:22.354+0100    [###################.....] pllution_db.monitoring_data 17.5MB/21.2MB (82.3%)
      2023-01-15T21:29:23.042+0100    [########################] pollution_db.monitoring_data 21.2MB/21.2MB (100.0%)
      2023-01-15T21:29:23.042+0100    52584 document(s) imported successfully. 0 document(s) failed to import.

```
      

### 4. Retrieving Data from Database
Mongodb provides several read operations for  retrieving data. Because the data is inserted as a document, the retrival will be done using the find fuction.  The code below retrieves all the data from the monitoring_data collection.

```js 
db.monitoring_data.find().pretty();
```
    
 The output data is from running the code is seen below
 ``` js
      [
        {
         _id: ObjectId("63c466e8d4577054b79e4a3a"),
         station_id: 463,
         name: 'Fishponds Road',
         geo_point_2d: '51.4780449714, -2.53523027459',
         readings: [
      {
        'Date Time': '2019-07-01T08:00:00+00:00',
        NOx: 75.8784,
        NO2: 43.3181,
        NO: 21.2614,
        PM10: 0,
        NVPM10: 0,
        VPM10: 0,
        'NVPM2.5': 0,
        'PM2.5': 0,
        'VPM2.5': 0,
        CO: 0,
        O3: 0,
        SO2: 0,
        Temperature: 0,
        RH: 0,
        'Air Pressure': 0,
        DateStart: '2009-03-13T00:00:00+00:00',
        DateEnd: '',
        Current: 1,
        'Instrument Type': 'Continuous (Reference)'
      },
      {
        'Date Time': '2019-07-02T07:00:00+00:00',
        NOx: 72.4838,
        NO2: 28.305,
        NO: 28.8057,
        PM10: 0,
        NVPM10: 0,
        VPM10: 0,
        'NVPM2.5': 0,
        'PM2.5': 0,
        'VPM2.5': 0,
        CO: 0,
        O3: 0,
        SO2: 0,
        Temperature: 0,
        RH: 0,
        'Air Pressure': 0,
        DateStart: '2009-03-13T00:00:00+00:00',
        DateEnd: '',
        Current: 1,
        'Instrument Type': 'Continuous (Reference)'
      },
      {
        'Date Time': '2019-07-03T00:00:00+00:00',
        NOx: 24.7191,
        NO2: 16.4475,
        NO: 5.3621,
        PM10: 0,
        NVPM10: 0,
        VPM10: 0,
        'NVPM2.5': 0,
        'PM2.5': 0,
        'VPM2.5': 0,
        CO: 0,
        O3: 0,
        SO2: 0,
        Temperature: 0,
        RH: 0,
        'Air Pressure': 0,
        DateStart: '2009-03-13T00:00:00+00:00',
        DateEnd: '',
        Current: 1,
        'Instrument Type': 'Continuous (Reference)'
      },
      {
        'Date Time': '2019-07-03T07:00:00+00:00',
        NOx: 64.7859,
        NO2: 28.7353,
        NO: 23.5059,
        PM10: 0,
        NVPM10: 0,
        VPM10: 0,
        'NVPM2.5': 0,
        'PM2.5': 0,
        'VPM2.5': 0,
        CO: 0,
        O3: 0,
        SO2: 0,
        Temperature: 0,
        RH: 0,
        'Air Pressure': 0,
        DateStart: '2009-03-13T00:00:00+00:00',
        DateEnd: '',
        Current: 1,
        'Instrument Type': 'Continuous (Reference)'
      },
      {
        'Date Time': '2019-07-03T14:00:00+00:00',
        NOx: 93.0431,
        NO2: 54.4106,
        NO: 25.2206,
        PM10: 0,
        NVPM10: 0,
        VPM10: 0,
        'NVPM2.5': 0,
        'PM2.5': 0,
        'VPM2.5': 0,
        CO: 0,
        O3: 0,
        SO2: 0,
        Temperature: 0,
        RH: 0,
        'Air Pressure': 0,
        DateStart: '2009-03-13T00:00:00+00:00',
        DateEnd: '',
        Current: 1,
        'Instrument Type': 'Continuous (Reference)'
      }
    ]
  }
  ...
]
````

   
   




### REFRENCES
[1] MongoDB. 2022. Document Database - NoSQL. [online] Available at: <https://www.mongodb.com/document-databases> [Accessed 13 January 2023].