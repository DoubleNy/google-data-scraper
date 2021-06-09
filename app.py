import flask
import pandas as pd
from flask import jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True

GOOGLE_REPORT_PATH = "./google_reports/mobility_report_RO.csv"

HEADERS = [
    "country region code",
    "county",
    "city",
    "date",
    "retail and recreation",
    "grocery and pharmacy",
    "parks",
    "transit stations",
    "workplaces",
    "residential",
 ]

counties = set()

def read_file():
    df = pd.read_csv(GOOGLE_REPORT_PATH)

    df = df.sample(5000)

    df = df.fillna(0)

    # print(df.sample(10))

    series = list()

    global counties

    for index, row in df.iterrows():
        if isinstance(row['county'], str):
            counties.add(row['county'])
        series.append({
            'county': row['county'],
            'date': row['date'],
            "retail and recreation": row['retail and recreation'],
            "grocery and pharmacy": row['grocery and pharmacy'],
            "parks": row['parks'],
            "transit stations": row['transit stations'],
            "workplaces": row['workplaces'],
            "residential": row['residential'],
        })

    # print(series)

    # print(list(df['date']))
    # print(list(df['retail and recreation']))
    # print(list(df['grocery and pharmacy']))
    # print(list(df['workplaces']))
    # print(list(df['residential']))

    # series_by_county = dict()

    # counties = [x for x in list(set(df["county"])) if str(x) != 'nan']

    # print(len(counties), counties)

    # for county_name in counties:
    #     print(county_name)
    #     county_df = df[df["county"] == county_name]
    #
    #     series_collection = dict()
    #     for header in HEADERS:
    #         series_collection[header] = list(county_df[header])
    #     break
    #

    return sorted(series, key=lambda x: x['date'])



def filter_by_counties():
    series = read_file()

    filtered_series = dict()

    for county in counties:
        curr_items = []
        for item in series:
            if item['county'] == county:
                curr_items.append(item)
        # print(len(curr_items))
        filtered_series[county] = curr_items
        # break
    # print(filtered_series)
    # print(series[0]['county'])
    # county0 = [x for x in series if x['county'] == counties[0]]
    #
    # print(county0)
    return filtered_series

@app.route('/google/ro', methods=['GET'])
def ro():
    series = read_file()
    return jsonify(series)

@app.route('/google/ro/counties', methods=['GET'])
def county():
    series = filter_by_counties()
    return jsonify(series)


if __name__ == '__main__':
    app.run(threaded=True, port=5000)