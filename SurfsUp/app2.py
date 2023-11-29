# Import the dependencies.
import numpy as np

import sqlalchemy
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
Base.prepare(autoload_with=engine)

# Save references to each table
Hawaii_Measurements = Base.classes.hawaii_measurements
Hawaii_Stations = Base.classes.hawaii_stations

# Create our session (link) from Python to the DB
session = Session(engine)

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
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def names():
     #Create our session (link) from Python to the DB
    #session = Session(engine)

    #"""Return a list of all passenger names"""
    # Query all passengers
    #results = session.query(Passenger.name).all()

    #session.close()

    # Convert list of tuples into normal list
   # all_names = list(np.ravel(results))

    #return jsonify(all_names)


@app.route("/api/v1.0/stations")
def names():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    results = session.query(Hawaii_Stations.name).all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)


#@app.route("/api/v1.0/stations")
#def passengers():
    ## Create our session (link) from Python to the DB
   # session = Session(engine)

   # """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    #results = session.query(Passenger.name, Passenger.age, Passenger.sex).all()

    #session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    #all_passengers = []
    #for name, age, sex in results:
    #    passenger_dict = {}
    #    passenger_dict["name"] = name
    #    passenger_dict["age"] = age
    #    passenger_dict["sex"] = sex
    #    all_passengers.append(passenger_dict)

    #return jsonify(all_passengers)

#@app.route("/api/v1.0/stations")
#def names():
   # # Create our session (link) from Python to the DB
    #session = Session(engine)

    #"""Return a list of all passenger names"""
    # Query all passengers
    #results = session.query(Passenger.name).all()

    #session.close()

    # Convert list of tuples into normal list
    #all_names = list(np.ravel(results))

    #return jsonify(all_names)


if __name__ == '__main__':
    app.run(debug=True)
