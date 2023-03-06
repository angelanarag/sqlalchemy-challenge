# Set-up
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

#################################################
# Flask Setup
#################################################
# Create an app, being sure to pass __name__
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
# 1. Create the homepage and display all available routes
@app.route("/")
def welcome():
    print("Server received request for 'Home' page...")
    """List all available api routes."""
    # Show all available routes
    return (
        f"Welcome to A.Narag's Module 10 SQLAlchemy Challenge!<br/>"
        f"----------------------------------------------------<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<end><br/>"
        f"/api/v1.0/start_date/end_date<br/>"
        f"<br>"
        f"Note: You will be asked to input the 'start_date' and 'end_date'. Format for querying is 'YYYY-MM-DD'.")

# 2. Return the JSON representation of the precipitation dictionary
#    Create dictionary of the query results from your precipitation analysis
#    Use date as the key and prcp as the value

@app.route("/api/v1.0/precipitation")
def precip():
    print("Server received request for 'Precipitation' page...")  

    # Create session (link) from Python to the DB
    session = Session(engine)

    """Return last 12 months of data) to a dictionary using date as the key and prcp as the value"""
    # Query the date and precipitations values from the measurement table
    sel = [measurement.date, measurement.prcp]

    recent_date = session.query(measurement.date).order_by(measurement.date.desc()).first()[0]
    recent_date = (dt.datetime.strptime(recent_date, "%Y-%m-%d")).date()
    start_date = recent_date - dt.timedelta(days=365)

    prcp_results = session.query(*sel).\
                    filter(measurement.date <= recent_date).filter(measurement.date >= start_date).\
                    order_by(measurement.date.desc()).all()
    
    session.close()

    # Create a dictionary from the queried data and append to a list 
    all_precipitation = []
    for date, prcp in prcp_results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["precipitation"] = prcp
        all_precipitation.append(precipitation_dict)

    # Return a JSON list of stations from the dataset.
    return jsonify(all_precipitation)


# 3. Return a JSON list of stations from the dataset.

@app.route("/api/v1.0/stations")
def all_stations():
    print("Server received request for 'Stations' page...")  

    # Create our session (link) from Python to the DB
    session = Session(engine)

   # Query station information
    station_results = session.query(station.id, station.station, station.name2).all()

    session.close()

    # Create a dictionary from the row data and append to a list 
    all_stations = []
    for station in station_results:
        stations_dict = {}
        stations_dict["ID"] = id
        stations_dict["Station"] = station
        stations_dict["Name"] = name
        all_stations.append(stations_dict)

    # Return a JSON list of stations from the dataset.
    return jsonify(all_stations)

# 4. Return a JSON list of temperature observations for the previous year
#    of the most-active station for the previous year of data.

@app.route("/api/v1.0/tobs")
def temperature():
    print("Server received request for 'Temperature' page...") 
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Find the most active station
    most_active_station = session.query(measurement.station, func.count(measurement.station)).\
                                        order_by(func.count(measurement.station).desc()).\
                                        group_by(measurement.station).\
                                        first()[0]

   # Query temperature information from the last recent year of data for the most active station
    sel3 = [measurement.station,
            measurement.date,
            measurement.tobs]
    
    date1 = dt.datetime(2017, 8, 23)
    date2 = dt.datetime(2016, 8, 23)
    
    temp_results = session.query(*sel3).\
            filter(measurement.date <= date1).filter(measurement.date >= date2).\
            filter(measurement.station == most_active_station).\
            order_by(measurement.date.desc()).all()

    session.close()

    return jsonify(temp_results)

# 5. Return a JSON list of the minimum temperature, average temperature, and maximum temperature
#    a. for all the dates greater than or equal to the specified start
#    b. for all the dates from the specified start-end range, inclusive
@app.route("/api/v1.0/<start>")
def start_date(start_date):
    print("Server received request... Please enter {start_date}. Use format YYYY-MM-DD.")

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query of min, max and avg temperature for all the dates greater than or equal to the specified start.
    start_results = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
             filter(measurement.date >= start_date).all()

    session.close()     

# Create a dictionary from the row data and append to a list 
    start_temps = []
    for date, min, avg, max in start_results:
        temp_dict = {}
        temp_dict["Minimum Temp"] = min
        temp_dict["Maximum Temp"] = max
        temp_dict["Average Temp "] = avg
        start_temps.append(temp_dict)

    return jsonify(start_temps)

@app.route("/api/v1.0/<start>")
def start_date(start_date, end_date):
    print("Server received request... Please enter {start_date} and {end_date}.  Use format YYYY-MM-DD.")

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query of min, max and avg temperature for dates between given start and end date.
    range_results = session.query(func.min(measurement.tobs),\
         func.max(measurement.tobs), func.avg(measurement.tobs)).\
             filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()

    session.close()        

    # Create a dictionary from the row data and append to a list of info
    range_temps = []
    for min, max, avg in range_results:
        temp_dict2 = {}
        temp_dict2["Minimum Temp"] = min
        temp_dict2["Maximum Temp"] = max
        temp_dict2["Average Temp "] = avg
        range_temps.append(temp_dict2)

    return jsonify(range_temps)


if __name__ == "__main__":
    app.run(debug=True)
