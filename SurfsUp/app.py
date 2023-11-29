# Import the dependencies.
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
engine = create_engine("sqlite:///./Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

one_year = dt.date(2016, 8, 23)
# Create our session (link) from Python to the DB
# Do this in each route / open and close

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/startdate<br/>----- (yyyy-mm-dd) will give average temperatures from date until the end of dataset<br/>"
        f"/api/v1.0/startdate/enddate<br/>----- (yyyy-mm-dd) will give average temperatures between dates<br/>"
    )

#Static

@app.route("/api/v1.0/precipitation")
def precipitation():
    #Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all passengers
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year).all()

    session.close()

        # Create a dictionary from the row data and append to a list of all_passengers
    all_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all passengers
    results = session.query(Station.name).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    #Create our session (link) from Python to the DB
    
    session = Session(engine)

    # Query tobs for one station
    results = session.query(Measurement.station, Measurement.date, Measurement.tobs)\
    .filter(Measurement.date >= one_year)\
        .filter(Measurement.station == 'USC00519281').all()

    session.close()

        # Create a dictionary from the row data and append to a list of all_passengers
    all_tobs = []
    for station, date, prcp in results:
        tobs_dict = {}
        tobs_dict["station"] = station
        tobs_dict["date"] = date
        tobs_dict["prcp"] = prcp
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

#Dynamic
# https://stackoverflow.com/questions/11830980/sqlalchemy-simple-example-of-sum-average-min-max

@app.route("/api/v1.0/<start_date>")
def get_start_date(start_date):
    """Get MIN, MAX, and AVG temperatures
       from dataset from the start date until the end"""

    session = Session(engine)

    qry = session.query(func.min(Measurement.tobs).label("min_temp"), 
                    func.max(Measurement.tobs).label("max_temp"),
                    func.avg(Measurement.tobs).label("avg_temp")
                    ).filter(Measurement.date > start_date)
    qry = qry.group_by(Measurement.tobs)

    session.close()

    temps = list(np.ravel(qry))

    return jsonify(temps)

@app.route("/api/v1.0/<start_date>/<end_date>")
def get_start_date(start_date, end_date):
    """Get MIN, MAX, and AVG temperatures
       from dataset from the start date until the end date"""

    session = Session(engine)

    qry = session.query(func.min(Measurement.tobs).label("min_temp"), 
                    func.max(Measurement.tobs).label("max_temp"),
                    func.avg(Measurement.tobs).label("avg_temp")
                    ).filter(Measurement.date > start_date).filter(Measurement.date < end_date)
    qry = qry.group_by(Measurement.tobs)

    session.close()

    temps = list(np.ravel(qry))

    return jsonify(temps)

if __name__ == '__main__':
    app.run(debug=True)
