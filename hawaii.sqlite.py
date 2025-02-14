# Import the dependencies.
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

#################################################
# Database Setup
#################################################

# Create engine to connect to database
database_path = "sqlite:///hawaii.sqlite"  
engine = create_engine(database_path)

# Reflect an existing database into a new model
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_path
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    return (
        "Available Routes:<br/>"
        "/api/v1.0/precipitation<br/>"
        "/api/v1.0/stations<br/>"
        "/api/v1.0/tobs<br/>"
        "/api/v1.0/<start><br/>"
        "/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    last_year_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= "2016-08-23").all()
    return jsonify(dict(last_year_data))

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    return jsonify([station[0] for station in results])

@app.route("/api/v1.0/tobs")
def tobs():
    last_year_tobs = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == "USC00519281").filter(Measurement.date >= "2016-08-23").all()
    return jsonify(last_year_tobs)

@app.route("/api/v1.0/<start>")
def start_date(start):
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
        .filter(Measurement.date >= start).all()
    return jsonify(results)

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
        .filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    return jsonify(results)debug=True)
    )

if __name__ == "__main__":
    app.run(debug=True)
