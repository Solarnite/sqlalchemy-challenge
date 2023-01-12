# sqlalchemy-challenge
 
 
# Summary
This project uses Python and SQLAlchemy to do basic data exploration and analysis of an SQLite climate database. All analysis is done using SQLAlchemy (ORM queries), Pandas, and Matplotlib. It also provides an API (designed using Flask) for querying this climate data.

# Tools
-SQLAlchemy, Pandas, Matplotlib
-Flask API


# Part 1: Analyze and Explore the Climate Data
[Climate analysis](https://github.com/Solarnite/sqlalchemy-challenge/blob/main/SurfsUp/climate_analysis.ipynb)

This part of the project analyzes the precipitation and weather station data in Hawaii. Visualizations were produced indicating the precipitation in last year from 2017-08-23 in a chart and a temperature histogram.

# Part 2: Design The Climate App
[App](https://github.com/Solarnite/sqlalchemy-challenge/blob/main/SurfsUp/app.py)

A Flask API was developedd with the queries from our initial analysis.
The following routes were created by using Flask.

**Routes**
/
   
   - Home Page
   - Lists all routes that are available.
   
/api/v1.0/precipitation

   - The inches of precipitation in the last year.
   
/api/v1.0/stations

   - Shows the active weather stations.
   
/api/v1.0/tobs

   - The daily temperatures for the most active station in the last year.
   
/api/v1.0/yyyy-mm-dd

   - Shows the minimum, maximum, and average temperatures for a specific start date.
   
/api/v1.0/yyyy-mm-dd/yyyy-mm-dd

   - Shows the minimum, maximum, and average temperatures for a specific start to end date.
