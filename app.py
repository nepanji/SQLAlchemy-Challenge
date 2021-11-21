#################################################
# Setup Dependencies
#################################################
import numpy as np
import datetime as dt

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurements = Base.classes.measurement
stations = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def Home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
        f"<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all precipitation"""
    # Query all precipitation
    results = session.query(measurements.date, measurements.prcp).all()

    session.close()

    # Convert list of tuples into normal list
    all_prcp = []
    for date, prcp in results:

        # Create an empty object
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of station data including the station and name"""
    # Query all station info
    results = session.query(stations.station, stations.name).all()

    session.close()

    # Convert list of tuples into normal list
    # Create a dictionary from the row data and append to a list of all_stations
    all_stations = []
    for station, name in results:

        # Create an empty object
        stations_dict = {}
        stations_dict["station"] = station
        stations_dict["name"] = name
        all_stations.append(stations_dict)

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Last date = most recent date (using order by desc)
    recent_date = session.query(measurements.date).order_by(measurements.date.desc()).first() 
    query_date = (dt.datetime.strptime(recent_date[0], "%Y-%m-%d") - dt.timedelta(days=365)).strftime('%Y-%m-%d')

    # most active station
    active_stations = session.query(measurements.station,func.count(measurements.station)).group_by(measurements.station).\
        order_by(func.count(measurements.station).desc()).first()

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    results = session.query(measurements.tobs).filter(measurements.date >= query_date).\
filter(measurements.station == active_stations[0]).all()


    session.close()

    # Convert list of tuples into normal list
    most_active_station = list(np.ravel(results))

    return jsonify(most_active_station)

   
@app.route("/api/v1.0/<start>")
def start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    sel = [measurements.station, 
       stations.name, 
       func.min(measurements.tobs), 
       func.max(measurements.tobs), 
       func.avg(measurements.tobs)]

    results = session.query(*sel).filter(measurements.date >= start).all()
    
    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_info = []
    for date, min, max, avg in results:

        # Create an empty object
        info_list_dict = {}
        info_list_dict["date"] = date
        info_list_dict["tmin"] = min
        info_list_dict["tmax"] = max
        info_list_dict["tavg"] = avg
        all_info.append(info_list_dict)

    return jsonify(all_info)

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    sel = [measurements.station, 
       stations.name, 
       func.min(measurements.tobs), 
       func.max(measurements.tobs), 
       func.avg(measurements.tobs)]

    results = session.query(*sel).filter(measurements.date <= end).all()
    
    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_info = []
    for date, min, max, avg in results:

        # Create an empty object
        info_list_dict = {}
        info_list_dict["date"] = date
        info_list_dict["tmin"] = min
        info_list_dict["tmax"] = max
        info_list_dict["tavg"] = avg
        all_info.append(info_list_dict)

    return jsonify(all_info)


if __name__ == '__main__':
    app.run(debug=True)

