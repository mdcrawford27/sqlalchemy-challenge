# import dependencies
import datetime as dt
import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# setup database (do pretty much everything we did in the Jupiter Notebook file)
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)


# setup Flask
app = Flask(__name__)

# create the routes
@app.route("/")
def home():
    return (
        f"Aloha!<br/>"
        f"Check out these routes...<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start<br/>"
        f"/api/v1.0/temp/start/end"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Calc the year_ago date from step 1
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # create queries
    results = session.query(Measurement.prcp, Measurement.date).filter(Measurement.date >= year_ago).all()

    # create dictionary and convert to json
    dictionary = []
    for prcp, date in results:
        dict = {}
        dict["date"] = date, prcp
        dictionary.append(dict)

    return jsonify(dictionary)


@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()

    # convert to a list/json
    stations = list(np.ravel(results))
    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def tobs():
    # Calc the year_ago date from step 1
    year_ago= dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Query the pmost active station found in step 1
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= year_ago).all()

    # convert to list and return as json
    tobs = list(np.ravel(results))
    return jsonify(tobs)


@app.route("/api/v1.0/temp/<start>")
def date(start=None):

    functions = [func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]

    results = session.query(*functions).\
        filter(Measurement.date >= start).all()

    # convert to list and return as json
    temps = list(np.ravel(results))
    return jsonify(temps)

@app.route("/api/v1.0/temp/<start>/<end>")
def dates(start=None, end=None):

    functions = [func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]

    results = session.query(*functions).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()

    # convert to list and return as json
    temps = list(np.ravel(results))
    return jsonify(temps)


if __name__ == '__main__':
    app.run()
