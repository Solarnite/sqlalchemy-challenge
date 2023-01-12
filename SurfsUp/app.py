import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(autoload_with = engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def homepage():
    """List all available api routes."""
    return (
        f"Welcome to the Hawaii Climate App. Here are the Available Routes:<br/>"
        f"<br/>"
        f"Precipitation data for a whole year:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"<br/>"
        f"List of active weather stations:<br/>"
        f"/api/v1.0/stations<br/>"
        f"<br/>"
        f"The observed temperatures of the most-active station for a whole year:<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"The average, maximum, and minimum temperature for a specified start date (Format:yyyy-mm-dd):<br/>"
        f"/api/v1.0/start<br/>"
        f"<br/>"
        f"The average, maximum, and minimum temperatures for a specified start date to end date (Format:yyyy-mm-dd/yyyy-mm-dd):<br/>"
        f"/api/v1.0/start/end<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Calculate the start date 1 year ago from the last data point in the database.
    start_date = dt.date(2017,8,23) - dt.timedelta(days = 365)

    # Query for annual precipitation
    results = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= start_date).all()
    
    # Close Session
    session.close()

    # Convert query results to a dictionary using date as the key and prcp as the value.
    precipitation_data = []

    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        precipitation_data.append(prcp_dict)
    return jsonify(precipitation_data)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all stations
    results = session.query(station.station).\
        order_by(station.station).all()
    
    # Close Session
    session.close()

    # Convert list of tuples into normal list
    total_stations = list(np.ravel(results))
    return jsonify(total_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query temperature observations of the most active station for the past 12 months
    start_date = dt.date(2017,8,23) - dt.timedelta(days = 365)
    results =  session.query(measurement.date, measurement.tobs).\
        filter(measurement.station == 'USC00519281').\
        filter(measurement.date >= start_date).all()

    # Close Session
    session.close()

    # Convert list of tuples into normal list
    active_station = list(np.ravel(results))
    return jsonify(active_station)

@app.route("/api/v1.0/<start>")
def start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Start Date
    start = dt.datetime.strptime(start, '%Y-%m-%d')

    # Query for minimum, maximum, and average temperatue for specific start to end date.
    results = session.query(func.min(measurement.tobs),\
        func.max(measurement.tobs),\
        func.avg(measurement.tobs)).\
        filter(measurement.date >= start).all()

    # Close Session
    session.close()

    # Covert query results to a dictionary
    start_date_tobs = []
    for min, max, avg in results:
        start_dict = {}
        start_dict["TMIN"] = min
        start_dict["TMAX"] = max
        start_dict["TAVG"] = avg
        start_date_tobs.append(start_dict)
    return jsonify(start_date_tobs)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Start Date to end date
    start = dt.datetime.strptime(start, '%Y-%m-%d')
    end = dt.datetime.strptime(end, "%Y-%m-%d")

# Query for minimum, maximum, and average temperatue for specific start to end date.
    results = session.query(func.min(measurement.tobs),\
        func.max(measurement.tobs),\
        func.avg(measurement.tobs)).\
        filter(measurement.date >= start).\
        filter(measurement.date <= end).all()

    # Close Session
    session.close()

    # Covert query results to a dictionary
    start_end_tobs = []
    for min, max, avg in results:
        start_end_dict = {}
        start_end_dict["TMIN"] = min
        start_end_dict["TMAX"] = max
        start_end_dict["TAVG"] = avg
        start_end_tobs.append(start_end_dict)
    return jsonify(start_end_tobs)

if __name__ == '__main__':
    app.run(debug=True)