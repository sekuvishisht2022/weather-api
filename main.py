from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

stations = pd.read_csv("data_small/stations.txt", skiprows=17)
stations = stations[["STAID", "STANAME                                 "]]


@app.route("/")
def home():
    return render_template("home.html", data=stations.to_html())


@app.route("/api/v1/<station>/<date>")
def about(station, date):
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"

    df = pd.read_csv(
        filename,
        skiprows=20,
        parse_dates=["    DATE"]
    )

    # Convert the date from the URL into a pandas datetime value.
    requested_date = pd.to_datetime(date)

    temperature = (
        df.loc[df["    DATE"] == requested_date, "   TG"].squeeze() / 10
    )

    return {
        "station": station,
        "date": date,
        "temperature": temperature
    }


@app.route("/api/v1/<station>")
def all_data(station):
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"

    df = pd.read_csv(
        filename,
        skiprows=20,
        parse_dates=["    DATE"]
    )

    # Convert dates to strings so Flask can return them as JSON.
    df["    DATE"] = df["    DATE"].astype(str)

    return df.to_dict(orient="records")


@app.route("/api/v1/yearly/<station>/<year>")
def yearly(station, year):
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"

    df = pd.read_csv(filename, skiprows=20)

    df["    DATE"] = df["    DATE"].astype(str)

    result = df[df["    DATE"].str.startswith(str(year))]

    return result.to_dict(orient="records")


if __name__ == "__main__":
    app.run(debug=True)