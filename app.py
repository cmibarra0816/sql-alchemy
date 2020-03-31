import sqlalchemy
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.types import Date
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import time
import datetime as dt
from flask import Flask, jsonify, request

#Database Setup

engine=create_engine("sqlite:///Resources/hawaii.sqlite")

#Mirror database in python

Base=automap_base()

#Mirror tables in DB

Base.prepare(engine, reflect=True)

#Obtain SQL, save references to each table

Measurement=Base.classes.measurement
Station=Base.classes.station

#Create sessions (link) from Python to the DB

session=Session(engine)

#Flask setup

app=Flask(__name__)

#Flask routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"-When given the start date (YYYY-MM-DD), calculates the MIN/AVG/MAX temperature for all dates greater than and equal to the start date<br/>"
        f"/api/v1.0/<start>/<end><br/>"
        f"- When given the start and the end date (YYYY-MM-DD), calculate the MIN/AVG/MAX temperature for dates between the start and end date inclusive<br/>"
    )

###

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Returns a list of amounts of precipitation with dates"""
    #Query all measurements
    results=session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date>='2016-08-24').filter(Measurement.date<='2017-08-23').order_by(Measurement.date).all()
    prcp_dict={date:prcp for date,prcp in results}
    session.commit()
    time.sleep(2)

    #Convert list of tuples into normal list
    return jsonify(prcp_dict)

###

@app.route("/api/v1.0/tobs")
def tobs():
    """Returns a list of amounts of tobs with dates"""
    #Query all tobs
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= '2016-08-24').filter(Measurement.date<='2017-08-23').order_by(Measurement.date).all()
    tobs_dict= {date:tobs for date,tobs in results}
    session.commit()
    time.sleep(2)

    #Convert list of tuples into normal list
    return jsonify(tobs_dict)

###

@app.route("/api/v1.0/<date>")
def startDateOnly(date):
    day_temp_results=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date>=date).all()
    session.commit()
    time.sleep(2)

    #Convert list of tuples into normal list
    return jsonify(day_temp_results)

###

@app.route("/api/v1.0/<start>/<end>")
def startDateEndDate(start,end):
    multi_day_temp_results=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date>=start).filter(Measurement.date<=end).all()
    session.commit()
    time.sleep(2)

    #Convert list of tuples into normal list
    return jsonify(multi_day_temp_results)

if __name__=='__main__':
    app.run(debug=True)
