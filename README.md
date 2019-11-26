# Data Engineering Nanodegree, Data Warehouse with AWS Services

A music streaming startup, Sparkify, has grown their user base and song database and want to move their processes and data onto the cloud. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

This codebase creates a database containing 5 tables in star schema,
that organizes data related to this music library, and user listening data. This data
has been extracted from these two next sources: 

- Song data: `s3://udacity-dend/song_data`

Sample: 
```
{
    "num_songs": 1, 
    "artist_id": "ARJIE2Y1187B994AB7", 
    "artist_latitude": null, 
    "artist_longitude": null, 
    "artist_location": "", 
    "artist_name": "Line Renaud",
    "song_id": "SOUPIRU12A6D4FA1E1", 
    "title": "Der Kleine Dompfaff", 
    "duration": 152.92036, 
    "year": 0
 }
```
- Log data: `s3://udacity-dend/log_data`

Sample: 

![log data sample](img/log-data.png)

First of all, using Redshift, these s3 buckets are read and copied to a table each in a database.
Then, using these two tables, the data is selected an introduced into 5 different tables in star-schema: 

- **Songplay Table**: this represents the only fact table in the star schema. It contains 
  data related to how users listen to music, including the time at which they listen to it, 
  their location, what song and artist (related with their IDs) the event relates to, and other
  pieces of information that can be used to analyze user listening activity. 

- **Users Table**: a dimension table, that holds user's data, including their first and last name,
  their gender and whether or not they're subscribed. 

- **Songs Table**: a dimension table, that holds songs details, including the title, it's 
  contributing artist, the duration, the year of its release, etc. 

- **Artist Table**: a dimension table, that holds aritst details, including their name and 
  their location. 

- **Time Table**: a dimension table, that holds many different ways of interpreting a timestamp, 
  like a weekday, hour, month, day of month, etc. 

## Brief explanation of each file in this repository

- `iac.ipynb`: Stands for "Infrastructure As Code", this file is a Jupiter notebook that 
  aids in the creation of a Redshift Cluster that will handle the process of  extracting data
  from the S3 buckets and inserting them into tables.

- `dwh.cfg`: Config file where credentials and other configurations for Redshift Cluster and AWS
  access are entered.

- `sql_queries.py`: contains the queries for `DROP`-ping, `CREATE`-ing, and `INSERT`-ing data
  into tables. 

- `create_tables.py`: connects safely to database and runs the table creation queries, one by one,
  dropping a table with the same name if it exists first. This way we make sure that we insert
  into a fresh new table. 

- `etl.py`: performs the bulk of the work, analyzing the files cited above, parsing the data, and 
  inserting it into their respective tables, while giving a progress in the console. 

## Running this project

1. Create an AWS account and get credentials for the IAM User. These will include
   an API key and a secret. 
2. Copy these values to the `dwh.cfg` file, it will look something like this: 

```
[AWS]
KEY=akeyofletterandnumbers
SECRET=morelettersandnumbers
```

3. Also fill out the next values in `dwh.cfg`: 

```
DB_NAME=<insert_value>
DB_USER=<insert_value>
DB_PASSWORD=<insert_value>
```

4. Open the Jupiter notebook and run each cell (before where it says DANGER) to 
   create a Redshift Cluster and IAM Role. You will have to wait a few minutes
   while the Cluster gets created. 
5. The values for the missing keys in `dhw.cfg` will be printed in the Jupiter notebook. 
   Copy these values to the config file. Now we're ready to create the tables. 
6. Run the `create_table.py`. This will delete existing tables with
   the names that we are using and create new, empty ones for us to insert the data parsed from
   the files.
7. Run the `etl.py` and wait for the script to finish. This will connect to the Redshift cluster
   and perform the copying of the data in the buckets to the 5 tables. 

Now you may access the cluster through the AWS webpage, and make queries using their query editor. 
