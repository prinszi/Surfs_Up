import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc

from flask import Flask, jsonify

app = Flask(__name__)



@app.route("/")
def home():
    return (
        f"Welcome to Hawaii! Check out all these gnarly links!<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )
@app.route("/api/v1.0/precipitation")
def prcp():
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    Measurement = Base.classes.measurement
    Station = Base.classes.station
    session = Session(engine)
    date = session.query(Measurement.date).filter(Measurement.date).order_by(Measurement.date.desc()).first()
    date_time = dt.datetime.strptime(date[0], '%Y-%m-%d')
    query_date = date_time-dt.timedelta(days=365)
    rain = session.query(Measurement.date, Measurement.prcp).filter(func.strftime("%Y-%m-%d", Measurement.date) >= query_date).order_by(Measurement.date).all()
    prcp_dict = dict(rain)
    return jsonify(prcp_dict)

@app.route("/api/v1.0/stations")
def stations():
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    Measurement = Base.classes.measurement
    Station = Base.classes.station
    session = Session(engine)
    station_list = session.query(Station.station, Station.name).all()
    station_dict = dict(station_list)
    return jsonify(station_dict)

@app.route("/api/v1.0/tobs")
def tobs():
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    Measurement = Base.classes.measurement
    Station = Base.classes.station
    session = Session(engine)
    date_tobs = session.query(Measurement.date).filter(Measurement.date).order_by(Measurement.date.desc()).first()
    date_time_tobs = dt.datetime.strptime(date_tobs[0], '%Y-%m-%d')
    query_date_tobs = date_time_tobs-dt.timedelta(days=365)
    most_tobs = session.query(Measurement.station, func.count(Measurement.tobs)).filter(Measurement.tobs != "Null").group_by(Measurement.station).order_by(desc(func.count(Measurement.tobs))).all()
    tobs_12_mo = session.query(Measurement.date, Measurement.tobs).filter((func.strftime("%Y-%m-%d", Measurement.date) >= query_date_tobs) & (Measurement.station == most_tobs[0][0])).all()
    tobs_dict = dict(tobs_12_mo)
    return jsonify(tobs_dict)

# * `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`

#   * Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

#   * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

#   * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.











if __name__ == "__main__":
    app.run(debug=True)