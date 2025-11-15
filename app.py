import streamlit as st
st .title('CALCULATE YOUR BMI')
wt = st.number_input('Enter your weight in kgs : ')
h = st.number_input('Enter your height in m : ')
if h==0:
    BMI = 0
else:
    BMI = wt/h**2
st.success(f'Your BMI is : {BMI} kg/cm^2')