import numpy as np
import pandas as pd
import streamlit as st
import joblib 

# lets load all the instances required over here
with open('transformer.joblib','rb') as file:
    transformer = joblib.load(file)

# Lets Load the model
with open('final_model.joblib','rb') as file:
    model = joblib.load(file)

# to add title
st.title('INN HOTEL GROUP')
st.header(':orange[This application will predict the chances of booking cancellation]')

# lets take input from user
arrival_month = st.slider('Select your month of arrival',min_value=1,max_value=12)
weekday_lambda = (lambda x:0 if x== 'Monday' else
                  1 if x=='Tuesday' else
                  2 if x=='Wednesday' else
                  3 if x=='Thursday' else
                  4 if x=='Friday' else
                  5 if x=='Saturday' else 6)
arrival_wday = weekday_lambda(st.selectbox('Select your weekday of arrival',['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']))
depart_wday = weekday_lambda(st.selectbox('Select your weekday of departure',['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']))

weekend_nights = st.number_input('Enter How many weekend nights are there in stay',min_value=0)
weekday_nights = st.number_input('Enter How many weekday nights are there in stay',min_value=0)
total_night = weekday_nights+weekend_nights
market_seg_type = (lambda x:0 if x=='Offline' else 1)(st.selectbox('How the booking has been made',['Online','Offline']))
lead_time = st.number_input('How many days prior the booking was made', min_value=0)
price = st.number_input('What is the average price per room',min_value=0)
no_of_adults = st.number_input('How many adult members in booking',min_value=0)
special_request = st.selectbox('Select the number of special request made',[0,1,2,3,4,5])
parking = (lambda x:0 if x=='No' else 1)(st.selectbox('Does guest need parking space',['Yes','No']))


# Transform the data
lead_time_t,price_t = transformer.transform([[lead_time,price]])[0]

# Create The input list

input_list = [lead_time_t,special_request,price_t,no_of_adults,weekend_nights,parking,weekday_nights,market_seg_type,arrival_month,arrival_wday,total_night,depart_wday]

# Make Prediction
prediction = model.predict_proba([input_list])[:,1][0]

# Lets show probability
# a button will be created where it will be written predict
if st.button('Predict'):
    st.success(f'Cancellation chances : {round(prediction,4)*100}%')

# this prediction is made on voting model