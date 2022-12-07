from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient
import requests
import pandas as pd
import numpy as np
from datetime import date
from datetime import timedelta

app = Flask(__name__)



# MONGO DB Connection
client = MongoClient("mongodb+srv://lakshays:eTEeGzkcY7qmfMUX@cluster0.pz2d0qu.mongodb.net/data?ssl=true&ssl_cert_reqs=CERT_NONE")
db = client.get_database('data')
records = db.cryptocurr


y2 = '2022'
M2 = 11 # Month count
begin2022 = pd.date_range(y2, periods=12, freq='MS').strftime("%Y-%m-%d")
end2022 = pd.date_range(y2, periods=M2, freq='M').strftime("%Y-%m-%d")
begin2022 = begin2022.tolist()
end2022 = end2022.tolist()

today = date.today()
# Yesterday date
yesterday = today - timedelta(days = 1)
yes_str = yesterday.strftime("%Y-%m-%d")
yes_lst = list(yes_str.split(" "))

start_date =  begin2022
end_date =  end2022 + yes_lst


symbols = 'BTC,DOGEHEDGE,BABYXRP,BUSD,USD,INR,CAD'

lineChart_BTC = []
lineChart_ETH = []
lineChart_BABYXRP = []
lineChart_BUSD = []
btc = []
eth = []
babyxrp = []
busd = []
inr=[]
usd=[]


res = {start_date[i]: end_date[i] for i in range(len(start_date))}  
#print(str(res))

for start, end in res.items():

    url = "https://api.exchangerate.host/fluctuation?start_date=" + start + "&end_date=" +  end + "&symbols=" + symbols + '&base=CAD' + "&format=json&source=crypto"
    print(url)
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        #print(data)
        
        #time.sleep(5)
        records.insert_one(data) #inserting data into MongoDB

        #Line Charts
        lineChart_BTC.append(data["rates"]["BTC"]["change"])
        lineChart_ETH.append(data["rates"]["DOGEHEDGE"]["change"])
        lineChart_BABYXRP.append(data["rates"]["BABYXRP"]["change"])
        lineChart_BUSD.append(data["rates"]["BUSD"]["change"])

        #Bar Charts
        btc.append(data["rates"]["BTC"]["start_rate"])
        eth.append(data["rates"]["DOGEHEDGE"]["start_rate"])
        babyxrp.append(data["rates"]["BABYXRP"]["start_rate"])
        busd.append(data["rates"]["BUSD"]["start_rate"])
        inr.append(data["rates"]["INR"]["start_rate"])
        usd.append(data["rates"]["USD"]["start_rate"])
    else:
        exit()


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/lineChart1")
def lineChart1():
    months = ["Jan'22","Feb'22","Mar'22","Apr'22","May'22","Jun'22","Jul'22","Aug'22","Sep'22","Oct'22","Nov'22","Dec'22"]
    values = lineChart_BTC
    return render_template('lineChart1.html',labels = months, values = values)

@app.route("/lineChart2")
def lineChart2():
    months = ["Jan'22","Feb'22","Mar'22","Apr'22","May'22","Jun'22","Jul'22","Aug'22","Sep'22","Oct'22","Nov'22","Dec'22"]
    values = lineChart_ETH
    return render_template('lineChart2.html',labels = months, values = values)

@app.route("/lineChart3")
def lineChart3():
    months = ["Jan'22","Feb'22","Mar'22","Apr'22","May'22","Jun'22","Jul'22","Aug'22","Sep'22","Oct'22","Nov'22","Dec'22"]
    values = lineChart_BABYXRP
    return render_template('lineChart3.html',labels = months, values = values)

@app.route("/lineChart Multiple")
def lineChart_M():
    months = ["Jan'22","Feb'22","Mar'22","Apr'22","May'22","Jun'22","Jul'22","Aug'22","Sep'22","Oct'22","Nov'22","Dec'22"]
    values1 = lineChart_BUSD
    values2 = lineChart_ETH
    values3 = lineChart_BTC

    return render_template('lineChart Multiple.html',labels = months, values1 = values1, values2 = values2, values3 = values3)

Bar_Values = [ np.average(eth), np.average(busd),np.average(usd)]
@app.route("/BarChart")
def BarChart():
    labels = [ "ETH","BUSD","USD"]
    values = Bar_Values
    return render_template('BarChart.html', labels=labels, values=values)


if __name__ == "__main__":
    app.debug = False
    app.run()