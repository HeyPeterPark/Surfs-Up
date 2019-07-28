# import dependencies
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from flask import Flask, jsonify
import datetime as dt

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
base = automap_base()
base.prepare(engine, reflect=True)

measurement = base.classes.measurement
station = base.classes.station
session = Session(engine)

app = Flask(__name__)

@app.route("/")
def home():
    return"""
    <!DOCTYPE><html>
        <h2>List all routes that are available: </h2>
        <ul>
            <li>List of precipitation scores <a target="_blank" href="/api/v1.0/precipitation">here</a></li>
            <li>List of stations <a target="_blank" href="/api/v1.0/stations">here</a></li>
            <li>List of observed temperatures <a target="_blank" href="/api/v1.0/tobs">here</a></li>
            <li>List of min., avg., and max. temperatures given date yyyy-mm-dd: <a target="_blank" href="/api/v1.0/2017-03-14">2017-03-14</a></li>
            <li>List of min., avg., and max. temperatures given a date range: <a target="_blank" href="/api/v1.0/2017-03-14/2017-03-28">2017-03-14/2017-03-28</a></li>
        </ul>
    </html>
    """

@app.route("/api/v1.0/precipitation")
def precipitation(): 
    last_date = session.query(measurement.date).order_by(measurement.date.desc()).first()
    one_year_ago = dt.datetime.strptime(last_date[0], "%Y-%m-%d") - dt.timedelta(days=365)
    
    last_year = dict(session.query(measurement.date,measurement.prcp).filter(measurement.date >= one_year_ago).all())
    return jsonify(last_year)

@app.route("/api/v1.0/stations")
def stations(): 
    stations_all = session.query(station.station, station.name).all()
    stations_list = list(stations_all)
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs(): 
    last_date = session.query(measurement.date).order_by(measurement.date.desc()).first()
    one_year_ago = dt.datetime.strptime(last_date[0], "%Y-%m-%d") - dt.timedelta(days=365)

    tobs_data_list = list(session.query(measurement.date, measurement.tobs).filter(measurement.date >= one_year_ago).all())
    return jsonify(tobs_data_list)

@app.route("/api/v1.0/<start>")
def start_day(start):
    start_day = session.query(measurement.date, func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).\
        group_by(measurement.date).all()
    start_day_list = list(start_day)
    return jsonify(start_day_list)

# Start-End Day Route
@app.route("/api/v1.0/<start>/<end>")
def start_end_day(start, end):
    start_end_day = session.query(measurement.date, func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).\
        filter(measurement.date <= end).\
        group_by(measurement.date).all()
    start_end_day_list = list(start_end_day)
    return jsonify(start_end_day_list)

if __name__ == '__main__':
    app.run(debug=True)