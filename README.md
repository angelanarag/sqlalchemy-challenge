# sqlalchemy-challenge

Module 10 Challenge SQLAlchemy

By A.Narag

March 2, 2023

This project has the following:

Part 1: Analyze and Explore the Climate Data


1. Please refer to the climate_starter.ipynb Jupyter Notebook. 
2. Python and SQLAlchemy - specifically, you’ll use SQLAlchemy ORM queries, Pandas, and Matplotlib - are utilized to do a basic climate analysis and data exploration of the climate database. 
3. SQLAlchemy create_engine() function was used to connect to the SQLite database (hawaii.sqlite). 
4. SQLAlchemy automap_base() function was used to reflect the tables into classes, and then save references to the classes named station and measurement.
5. Linked Python to the database by creating a SQLAlchemy session.

Precipitation Analysis
1. Find the most recent date in the dataset.
2. Using that date, get the previous 12 months of precipitation data by querying the previous 12 months of data.
3. Select only the "date" and "prcp" values.
4. Load the query results into a Pandas DataFrame, and set the index to the "date" column.
5. Sort the DataFrame values by "date".
6. Plot the results by using the DataFrame plot method
7. Use Pandas to print the summary statistics for the precipitation data

Station Analysis
1. Design a query to calculate the total number of stations in the dataset.
2. Design a query to find the most-active stations (that is, the stations that have the most rows). To do so, complete the following steps:
    - List the stations and observation counts in descending order.
    - Which station id has the greatest number of observations?
3. Design a query that calculates the lowest, highest, and average temperatures that filters on the most-active station id found in the previous query.
4. Design a query to get the previous 12 months of temperature observation (TOBS) data. To do so, complete the following steps:
    - Filter by the station that has the greatest number of observations.
    - Query the previous 12 months of TOBS data for that station.
    - Plot the results as a histogram with bins=12

Part 2: Climate App

1. Please refer to the Python app.py file
2. Start at the homepage and list all the available routes.
3. Convert the query results from the precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
4. Return a JSON list of stations from the dataset.
5. Query the dates and temperature observations of the most-active station for the previous year of data
6. Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.

