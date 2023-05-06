import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image

st.set_page_config(layout="wide", initial_sidebar_state="expanded")
st.title(':red[Fuel Economy]')

image = Image.open('fuel-economy.jpg')

df = pd.read_csv('data/VehicleMPG-1984to2023.csv')

YearRnge = sorted(df['ModelYear'].unique())
MinYear = df['ModelYear'].min()
MaxYear = df['ModelYear'].max()


#Sidebar - Year selector
YearSlider = st.sidebar.select_slider("Year:", options=YearRnge, value=(MinYear, MaxYear))
LwrRnge, UpprRnge = list(YearSlider)[0], list(YearSlider)[1]

#Sidebar - MPG by Model
st.sidebar.title("MPG by Model")

#Multiselect - Make selector
df_make = df[(df['ModelYear']>=LwrRnge) & (df['ModelYear']<=UpprRnge)].sort_values('Make')
sb_make = st.sidebar.multiselect("Make:", options=df_make['Make'].unique(), max_selections=5)

#Multiselect - Model selector
df_model = df_make[df_make['Make'].isin(sb_make) ].sort_values('Model') 
# & (df_make['Fuel Type 1'].str.contains("Electricity") == False & df_make['Fuel Type 1'].str.contains("Natural Gas")) == False 
sb_model = st.sidebar.multiselect("Model:", options=df_model['Model'].unique(), max_selections=5)

#Dataframe - Final selection
df_final = df_model[df_model['Model'].isin(sb_model) ].sort_values('Model') 

#Sidebar - MPG by Model
st.sidebar.title("MPG by Vehicle Class")

#Multiselect - Make selector
df_vehicle_class = df[(df['ModelYear']>=LwrRnge) & (df['ModelYear']<=UpprRnge)].sort_values('VehicleClass')
sb_vehicle_class = st.sidebar.multiselect("Vehicle Class:", options=df_vehicle_class['VehicleClass'].unique(), max_selections=5)

#DataframeVehicleClass - Final selection
df_vc_final = df_vehicle_class[df_vehicle_class['VehicleClass'].isin(sb_vehicle_class) ].sort_values('VehicleClass') 

tab1,tab2,tab3 = st.tabs(['What is Fuel Economy?', 'MPG by Model', 'MPG by Vehicle Class'])

with tab1:
    st.markdown(""" <style> .font {font-size:18px ; font-family: 'Arial'; color: red;} </style> """, unsafe_allow_html=True)
    st.markdown(""" <p class="font">Car fuel economy is directly related to miles per gallon, or MPG or miles per gallon electric (MPGe). The higher its mpg, the better your car's fuel economy.</p>""", unsafe_allow_html=True)

    st.markdown(""" <style> .font {font-size:14px ; font-family: 'Arial'; color: red;} </style> """, unsafe_allow_html=True)
    st.markdown(""" <p class="font">Your car's fuel economy - how far your vehicle can go using a specific amount of fuel - can have a real impact on your expenses. Choosing a vehicle with good fuel economy or taking steps to boost the fuel economy of your current vehicle, just might save you money at the gas pump.</p>""", unsafe_allow_html=True)

    st.image(image, width=900)

with tab2:

    CityMPG=alt.Chart(df_final).mark_bar().encode(
        x=alt.X('Model', title=''),
        y=alt.Y('mean(CityMPG)', title='Miles per Gallon'),
        color=alt.Color('mean(CityMPG)', legend=None)
    ).properties(height=500,width=200,title='Average City MPG')
    
    HighwayMPG=alt.Chart(df_final).mark_bar().encode(
        x=alt.X('Model', title=''),
        y=alt.Y('mean(HighwayMPG)', title='Miles per Gallon'),
        color=alt.Color('mean(HighwayMPG)', legend=None)
    ).properties(height=500,width=200,title='Average Highway MPG')

    CombinedMPG=alt.Chart(df_final).mark_bar().encode(
        x=alt.X('Model', title=''),
        y=alt.Y('mean(CombinedMPG)',title='Miles per Gallon'),
        color=alt.Color('mean(CombinedMPG)', legend=None)
    ).properties(height=500,width=200,title='Average Combined MPG')

    if sb_model:
        CityMPG | HighwayMPG | CombinedMPG

with tab3:
    VCCityMPG=alt.Chart(df_vc_final).mark_bar().encode(
        x=alt.X('VehicleClass', title=''),
        y=alt.Y('mean(CityMPG)', title='Miles per Gallon'),
        color=alt.Color('mean(CityMPG)', legend=None)
    ).properties(height=500,width=200,title='Average City MPG')

    VCHighwayMPG=alt.Chart(df_vc_final).mark_bar().encode(
        x=alt.X('VehicleClass', title=''),
        y=alt.Y('mean(HighwayMPG)', title='Miles per Gallon'),
        color=alt.Color('mean(HighwayMPG)', legend=None)
    ).properties(height=500,width=200,title='Average Highway MPG')

    VCCombinedMPG=alt.Chart(df_vc_final).mark_bar().encode(
        x=alt.X('VehicleClass', title=''),
        y=alt.Y('mean(CombinedMPG)',title='Miles per Gallon'),
        color=alt.Color('mean(CombinedMPG)', legend=None)
    ).properties(height=500,width=200,title='Average Combined MPG')

    if sb_vehicle_class:
        VCCityMPG | VCHighwayMPG | VCCombinedMPG