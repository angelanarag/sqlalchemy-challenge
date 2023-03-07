# Set-up
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
Station = Base.classes.station
measurement = Base.classes.measurement

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
        "<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/station<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f" ** Note: For the below two routes, you will need to include 'start_date' and 'end_date' in 'YYYY-MM-DD' format. **<br/>"
        f"/api/v1.0/<start><br/>"
        f"   Example: /api/v1.0/2016-01-01<br/>"
        f"/api/v1.0/<start>/<end><br/>"
        f"   Example: /api/v1.0/2016-01-01/2016-12-31")
        
        

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
        # Get the most recent date from the database and calculate one year back
    recent_date = session.query(measurement.date).order_by(measurement.date.desc()).first()[0]
    recent_date = (dt.datetime.strptime(recent_date, "%Y-%m-%d")).date()
    begin_date = recent_date - dt.timedelta(days=365)

    sel = [measurement.date, measurement.prcp]

    prcp_results = session.query(*sel).\
                    filter(measurement.date <= recent_date).filter(measurement.date >= begin_date).\
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

@app.route("/api/v1.0/station")
def all_station():
    print("Server received request for 'Stations' page...")  

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query station data from the Station dataset
    station_data = session.query(Station.station, Station.name).all()

    # Close the session                   
    session.close()

    # Convert list of tuples into normal list
    station_list = list(np.ravel(station_data))

    # Return a list of jsonified station data
    return jsonify(station_list)

# 4. Return a JSON list of temperature observations for the previous year
#    of the most-active station for the previous year of data.

@app.route("/api/v1.0/tobs")
def temps():
    print("Server received request for 'Temperature' page...") 
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Find the most active station
    most_active_station = session.query(measurement.station, func.count(measurement.station)).\
                                        order_by(func.count(measurement.station).desc()).\
                                        group_by(measurement.station).\
                                        first()[0]

   # Query temperature information from the last recent year of data for the most active station
    recent_date = session.query(measurement.date).order_by(measurement.date.desc()).first()[0]
    recent_date = (dt.datetime.strptime(recent_date, "%Y-%m-%d")).date()
    begin_date = recent_date - dt.timedelta(days=365)
    
    temp_results = session.query(measurement.date, measurement.tobs).\
            filter(measurement.date <= recent_date).filter(measurement.date >= begin_date).\
            filter(measurement.station == most_active_station).\
            order_by(measurement.date.desc()).all()

    session.close()

    # Create a dictionary from the row data and append to a list of tobs_list
    temps_list = []
    for date, tobs in temp_results:
        temps_dict = {}
        temps_dict["date"] = date
        temps_dict["temps"] = tobs
        temps_list.append(temps_dict)

    # Return a list of jsonified tobs data for the previous 12 months
    return jsonify(temps_list)


# 5. Return a JSON list of the minimum temperature, average temperature, and maximum temperature
#    a. for all the dates greater than or equal to the specified start
#    b. for all the dates from the specified start-end range, inclusive
@app.route("/api/v1.0/<start>")
def date_start(start=None):
    print("Server received request... Please use format YYYY-MM-DD for the date.")

    # replace <start> on the route with date format YYYY-MM-DD

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query of min, max and avg temperature for all the dates greater than or equal to the specified start.
    sel2 = [func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)]
    start_results = session.query(*sel2).filter(measurement.date >= start).all()

    session.close()     

# Create a dictionary from the row data and append to a list 
    start_list = []
    for min, max, avg in start_results:
        temp_dict = {}
        temp_dict["Minimum Temp"] = min
        temp_dict["Maximum Temp"] = max
        temp_dict["Average Temp "] = avg
        start_list.append(temp_dict)

    start_temps = list(np.ravel(start_list))
    return jsonify(start_temps)

@app.route("/api/v1.0/<start>/<end>")
def date_range(start=None, end=None):
    print("Server received request... Please use format YYYY-MM-DD for the date.")

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query of min, max and avg temperature for dates between given start and end date.

    sel3 = [func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)]
    range_results = session.query(*sel3).filter(measurement.date >= start).filter(measurement.date <= end).all()

    session.close()        

    # Create a dictionary from the row data and append to a list of info
    range_list = []
    for min, max, avg in range_results:
        temp_dict2 = {}
        temp_dict2["Minimum Temp"] = min
        temp_dict2["Maximum Temp"] = max
        temp_dict2["Average Temp "] = avg
        range_list.append(temp_dict2)

    range_temps = list(np.ravel(range_list))
    return jsonify(range_temps)


if __name__ == "__main__":
    app.run(debug=True)
