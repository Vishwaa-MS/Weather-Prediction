#   **Real Time Weather Prediction Using Machine Learning**
This project uses a machine learning model to predict the weather for the next five hours and gives the current weather data of your area. With the predicted data the model gives information, whether to irrigate your agricultural field. It also contains some information related to some efficient irrigation methods that will be helpful for farmers.

For data collection, we use Open-Weather API to get the hourly data of past 48 hours and predict the temperature and humidity for next 5 hours of the given place. The website also displays the current weather conditions of the same place.

For weather prediction the model uses a popular Time-series Forecasting algorithm called ARIMA (Autoregressive Integrated Moving Average). This model is a combination of the Auto Regression (AR) model and the Moving Average (MA) model. 


> Machine Learning Model

*ARIMA models are generally denoted as ARIMA (p,d,q)  where p is the order of autoregressive model, d is the degree of differencing, and q is the order of moving-average model. ARIMA models use differencing to convert a non-stationary time series into a stationary one, and then predict future values from historical data.*

> Frontend

In Frontend, we have used HTML for webpage structure, CSS and Bootstrap for styling the webpage, Chart.js for plotting the graphs.

> Backend

In Backend, we used Python framework called Flask to process the machine learning model and build the webpage.

> API

openWeather API


![image](https://github.com/Vishwaa-MS/Weather-Prediction/assets/93870138/fa3d851f-2359-4c6a-80f7-ee00221d95db)
![image](https://github.com/Vishwaa-MS/Weather-Prediction/assets/93870138/b94325cb-c60b-43b5-9897-938eac153171)
![image](https://github.com/Vishwaa-MS/Weather-Prediction/assets/93870138/084a7fd3-5960-4f27-95d3-0e27d054e165)
![image](https://github.com/Vishwaa-MS/Weather-Prediction/assets/93870138/e9b60e33-aded-403b-aa94-4afde97b1207)
![image](https://github.com/Vishwaa-MS/Weather-Prediction/assets/93870138/149165c2-e32e-4e1c-a2ec-c6a62d30890c)







