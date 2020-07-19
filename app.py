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
conn = engine.connect()
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Create our session (link) from Python to the DB
session = Session(engine)
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

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
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )

### /api/v1.0/precipitation
##Convert the query results to a dictionary using date as the key and prcp as the value.
##Return the JSON representation of your dictionary.

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """date and precipitation scores"""
    # Query to retrieve the date and precipitation scores
    precipData = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date).\
        filter(Measurement.date >= "2016-08-23").all()

    precipDate = {date: prcp for date, prcp in precipData}
    return jsonify(precipDate)

###/api/v1.0/stations
##Return a JSON list of stations from the dataset.

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """list of stations from the dataset"""
    # Query list of stations from the dataset
    stationsList = session.query(Station.station).all()
    return jsonify(stationsList)

###/api/v1.0/tobs
##Query the dates and temperature observations of the most active station for the last year of data.
##Return a JSON list of temperature observations (TOBS) for the previous year

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """dates and temperature observations of the most active station"""
    # Query the dates and temperature observations of the most active station for the last year of data.
    tempMeasure = session.query(Measurement.tobs, Measurement.station).filter(Measurement.date).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= "2016-08-23").all()

    return jsonify(tempMeasure)

###/api/v1.0/<start> and /api/v1.0/<start>/<end>
##Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given or start-end range.
##When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
##When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.

@app.route("/api/v1.0/<start>")
def tempData1():

    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    """ """
    # Query
    startDate = datetime.strptime('2016-08-23', '%Y-%m-%d').date()
    tempDataStart= session.query(func.min(Measurements.tobs),
                                 func.avg(Measurements.tobs),
                                 func.max(Measurements.tobs)).filter(Measurements.date >= start).all()
    tempData1 = list(np.ravel(tempDataStart))
    return jsonify(tempData1)


##When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.

@app.route("/api/v1.0/<start>/<end>")
def tempData2():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """ """
    # Query
    startDate = datetime.strptime('2016-08-23', '%Y-%m-%d').date()
    endDate = dt.date(2016, 8, 23) + dt.timedelta(days=365)

    tempDataStart2= session.query(func.min(Measurements.tobs),
                                 func.avg(Measurements.tobs),
                                 func.max(Measurements.tobs)).filter(Measurements.date >= start).filter(Measurements.date <= end).all()
    tempData2 = list(np.ravel(tempDataStart2))
    return jsonify(tempData2)

if __name__ == '__main__':
     app.run(debug=True)