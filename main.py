from flask import Flask, render_template, request
import requests
import pandas as pd
from pmdarima import auto_arima
import warnings
from statsmodels.tsa.arima.model import ARIMA
import matplotlib
from datetime import datetime, timedelta

app = Flask(__name__)

search_done = False
matplotlib.use('Agg')


@app.route('/', methods=['GET', 'POST'])
def home():
    search_done = False
    if request.method == "POST":
        try:
            city_form = request.form
            city = city_form['city']
            current_data = requests.get(
                f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=69f04e4613056b159c2761a9d9"
                "e664d2&units=metric")
            data_for_current_temp = current_data.json()
            city_name = data_for_current_temp['name']
        except KeyError:
            return render_template('404_error.html')
        else:
            city_form = request.form
            city = city_form['city']
            current_data = requests.get(
                f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=69f04e4613056b159c2761a9d9"
                "e664d2&units=metric")
            data_for_current_temp = current_data.json()
            city_name = data_for_current_temp['name']
            current_temp = round(data_for_current_temp['main']['temp'])
            feels_like = round(data_for_current_temp['main']['feels_like'])
            temp_min = round(data_for_current_temp['main']['temp_min'])
            temp_max = round(data_for_current_temp['main']['temp_max'])
            humidity = round(data_for_current_temp['main']['humidity'])
            country = data_for_current_temp['sys']['country']
            description = data_for_current_temp['weather'][0]['description']
            search_done = True
            return render_template('index.html', city=city_name, current_temp=current_temp, temp_max=temp_max,
                                   temp_min=temp_min, description=description, feels_like=feels_like, country=country,
                                   status=search_done, humidity=humidity)
    return render_template("index.html", status=search_done)


@app.route('/predict-weather', methods=['GET', 'POST'])
def prediction():
    predict_status = False
    if request.method == "POST":
        try:
            city_form = request.form
            city = city_form['city']
            current_data = requests.get(
                f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=69f04e4613056b159c2761a9d9"
                "e664d2&units=metric")
            data_for_current_temp = current_data.json()
            LAT = data_for_current_temp['coord']['lat']
            LON = data_for_current_temp['coord']['lon']
            parameters = {
                "lat": LAT,
                "lon": LON,
                "appid": "69f04e4613056b159c2761a9d9e664d2",
            }
        except KeyError:
            return render_template('404_error.html')
        else:
            city_form = request.form
            city = city_form['city']
            current_data = requests.get(
                f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=69f04e4613056b159c2761a9d9"
                "e664d2&units=metric")
            data_for_current_temp = current_data.json()
            LAT = data_for_current_temp['coord']['lat']
            LON = data_for_current_temp['coord']['lon']
            parameters = {
                "lat": LAT,
                "lon": LON,
                "appid": "69f04e4613056b159c2761a9d9e664d2",
                # "exclude": "current,minutely,daily"
            }
            response = requests.get("https://api.openweathermap.org/data/2.5/onecall", params=parameters)
            response.raise_for_status()
            data = response.json()

            # DATA SLICING
            temperature = []
            humidity = []
            hours = []
            for i in range(48):
                hourly_data = data['hourly'][i]
                hours.append(i)
                temperature.append(hourly_data['temp'] - 273)
                humidity.append(hourly_data['humidity'])

            reversed_hour = hours[::-1]

            # DATA MODELLING
            dict_data = {'hours': reversed_hour, 'temp': temperature, 'hum': humidity}
            df = pd.DataFrame(dict_data)
            df.to_csv('static/csv/weather_data.csv')

            # MACHINE LEARNING MODEL
            data = pd.read_csv("static/csv/weather_data.csv", index_col='hours')
            data = data.dropna()

            weather_data = data['temp']
            hum_data = data['hum']

            warnings.filterwarnings("ignore")

            weather_fit = auto_arima(weather_data, trace=True, suppress_warnings=True)
            weather_param = weather_fit.get_params().get("order")

            hum_fit = auto_arima(hum_data, trace=True, suppress_warnings=True)
            hum_param = hum_fit.get_params().get("order")

            model_temp = ARIMA(weather_data, order=weather_param)
            model_temp_fit = model_temp.fit()

            model_hum = ARIMA(hum_data, order=hum_param)
            model_hum_fit = model_hum.fit()

            index_future_time = []
            for i in range(0, 5):
                index_future_time.append(datetime.now() + timedelta(hours=i))
            index_future_hours = []
            for x in index_future_time:
                index_future_hours.append(x.time())
            s_index_future_hours = []
            for y in index_future_hours:
                s_index_future_hours.append(y.strftime("%H:%M"))
            weather_pred = model_temp_fit.predict(start=48, end=52, typ='levels')
            weather_pred.index = s_index_future_hours
            df = weather_pred
            list_file = df.to_list()
            temperature_1 = round(list_file[0], 1)
            temperature_2 = round(list_file[1], 1)
            temperature_3 = round(list_file[2], 1)
            temperature_4 = round(list_file[3], 1)
            temperature_5 = round(list_file[4], 1)

            hum_pred = model_hum_fit.predict(start=48, end=52, typ='levels')
            hum_pred.index = s_index_future_hours
            df2 = hum_pred
            list_file2 = df2.to_list()
            humidity_1 = round(list_file2[0], 1)
            humidity_2 = round(list_file2[1], 1)
            humidity_3 = round(list_file2[2], 1)
            humidity_4 = round(list_file2[3], 1)
            humidity_5 = round(list_file2[4], 1)

            current_data = requests.get(
                f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=69f04e4613056b159c2761a9d9"
                "e664d2&units=metric")
            data_for_current_temp = current_data.json()
            city_name = data_for_current_temp['name']
            current_temp = round(data_for_current_temp['main']['temp'])
            feels_like = round(data_for_current_temp['main']['feels_like'], 1)
            temp_min = round(data_for_current_temp['main']['temp_min'], 1)
            temp_max = round(data_for_current_temp['main']['temp_max'], 1)
            humidity = round(data_for_current_temp['main']['humidity'], 1)
            country = data_for_current_temp['sys']['country']
            description = data_for_current_temp['weather'][0]['description']
            predict_status = True
            search_done = True

            graph_temp = [
                (s_index_future_hours[0], temperature_1),
                (s_index_future_hours[1], temperature_2),
                (s_index_future_hours[2], temperature_3),
                (s_index_future_hours[3], temperature_4),
                (s_index_future_hours[4], temperature_5),
            ]

            tlabels = []
            tvalues = []
            for row in graph_temp:
                    tlabels.append(row[0])
                    tvalues.append(row[1])

            graph_hum = [
                (s_index_future_hours[0], humidity_1),
                (s_index_future_hours[1], humidity_2),
                (s_index_future_hours[2], humidity_3),
                (s_index_future_hours[3], humidity_4),
                (s_index_future_hours[4], humidity_5),
            ]

            hlabels = []
            hvalues = []
            for row in graph_hum:
                    hlabels.append(row[0])
                    hvalues.append(row[1])

            return render_template("index.html", predicted_temp=weather_pred, predicted_humidity=hum_pred,
                                   predict_status=predict_status, status=search_done, temperature_1=temperature_1,
                                   temperature_2=temperature_2, temperature_3=temperature_3, temperature_4=temperature_4,
                                   temperature_5=temperature_5, humidity_1=humidity_1, humidity_2=humidity_2,
                                   humidity_3=humidity_3, humidity_4=humidity_4, humidity_5=humidity_5,
                                   city=city_name, current_temp=current_temp, temp_max=temp_max,
                                   temp_min=temp_min, description=description, feels_like=feels_like, country=country,
                                   humidity=humidity, tlabels=tlabels, tvalues=tvalues, hlabels=hlabels, hvalues=hvalues)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
