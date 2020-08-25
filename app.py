# Step 2 CLIMATE APP

# Now that you have completed your initial analysis, design a Flask API based on the queries that you have just developed.
# * Use Flask to create your routes.
from flask import Flask, jsonify

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
session=Session(engine)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine,reflect=True)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

last_date = session.query(func.max(measurement.date)).all()[0][0]
last_date = dt.datetime.strptime(last_date,"%Y-%m-%d")
prior_year = last_date-dt.timedelta(365)

#Create an app
app = Flask(__name__)

@app.route("/")
def Home_Page():
    """List all routes that are available."""
    return(
        "Available routes:"
        '<ul>'
            '<li><a href="/api/v1.0/precipitation">Precipitation</a></li>'
            '<li><a href="/api/v1.0/station">Stations</a></li>'
            '<li><a href="/api/v1.0/tobs">Temperatures</a></li>'
            '<li><a href="/api/v1.0/<start>">Start Date</a></li>'
            '<li><a href="/api/v1.0/<start>/<end>">Start and End Dates</a></li>'
    )

# * `/api/v1.0/precipitation`
@app.route("/api/v1.0/precipitation")
def precepitation():
        """Return a list of precipitation data including date and precipitation of each station."""

#   * Convert the query results to a dictionary using `date` as the key and `prcp` as the value.
        results = session.query(measurement.date, measurement.prcp).all()
        # session.close()
        
        all_precipitation = []
        for date, prcp in results:
            precipitation_dict = {}
            precipitation_dict["date"] = date
            precipitation_dict["prcp"] = prcp
            all_precipitation.append(precipitation_dict)
            
#   * Return the JSON representation of your dictionary.
        return jsonify(all_precipitation)

# * `/api/v1.0/stations`
@app.route("/api/v1.0/station")
def stations():
    """Return a list of stations."""
    results=session.query(station.station).all()
    # session.close()
    
#   * Return a JSON list of stations from the dataset.
    return jsonify(results)

# * `/api/v1.0/tobs`
#   * Query the dates and temperature observations of the most active station for the last year of data.
@app.route("/api/v1.0/tobs")
def tobs():
    """Return the observations of the most active station in the last year."""
    
    results=session.query(measurement.date, measurement.tobs).filter(measurement.date>=prior_year).all()

#   * Return a JSON list of temperature observations (TOBS) for the previous year.
    return jsonify(results)

# * `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`
@app.route("/api/v1.0/<start>")
def tobs2(start):
    # results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
    #             filter(func.strftime("%Y-%m-%d", measurement.date) >=start).\
    #             group_by(measurement.date).all()
    results = session.query(func.min(measurement.tobs)).group_by(measurement.date).all()
    
    return_list = []
    # for date, tmin, tavg, tmax in results:
    for tmin in results:
        date_dict = {}
        date_dict["Min Temp"] = tmin
        # date_dict["Avg Temp"] = tavg
        # date_dict["Max Temp"] = tmax
        return_list.append(date_dict)
    
    return jsonify(return_list)

# @app.route("/api/v1.0/<start>/<end>")
# def tobs3(start,end):
#     results = session.query(measurement.date, func.min(measurement.tobs), func.avg(measurement.tobs, func.max(measurement.tobs)).\
#                 filter(func.strftime("%Y-%m-%d", measurement.date) >=startDate).\
#                 filter(func.strftime("%Y-%m-%d", measurement.date) <=endDate).\
#                 group_by(measurement.date).all()
    
#     return_list = []
#     for date, tmin, tavg, tmax in results:
#         date_dict = {}
#         date_dict["Date"] = date
#         date_dict["Min Temp"] = tmin
#         date_dict["Avg Temp"] = tavg
#         date_dict["Max Temp"] = tmax
#         return_list.append(date_dict)
    
#     return jsonify(return_list)

if __name__=='__main__':
    app.run()