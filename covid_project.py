import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import calendar 
import datetime as dt

#from datetime import datetime
#from matplotlib.dates import DateFormatter
#import matplotlib.ticker as ticker
#from pylab import *

st.title("All Cause Deaths and COVID-19 Deaths in the United States for 2019-2020")
st.markdown("-----")
st.markdown("**Provisonal counts of all cause deaths by week the deaths occured, by state, and by all causes of death. This dataset also includes weekly provisional counts of death for COVID-19, as underlying or multiple cause of death.**")
#CDC dataset
url="https://data.cdc.gov/api/views/muzy-jte6/rows.csv?accessType=DOWNLOAD"
#df=pd.read_csv(url,error_bad_lines=False)
def load_data():
    df_filter=pd.read_csv(url,error_bad_lines=False, usecols=["Jurisdiction of Occurrence","MMWR Year","MMWR Week","Week Ending Date","All Cause","COVID-19 (U071, Multiple Cause of Death)","COVID-19 (U071, Underlying Cause of Death)"])
    return df_filter
#map


#population dataset
pop = pd.read_csv("Population.csv")


try:
    df_filter = load_data()
except urllib.error.URLError as e:
    st.error(
        """
        **This demo requires internet access.**

        Connection error: %s
    """
        % e.reason
    )

merged = pd.merge(df_filter,pop,left_on='Jurisdiction of Occurrence', right_on = 'States')
states = st.sidebar.multiselect("Choose states",merged['Jurisdiction of Occurrence'].unique())

if not states:
    st.error("Please select a state")
def listToString(s):  
    
    # initialize an empty string 
    str1 = ""  
    
    # traverse in the string   
    for ele in s:  
        str1 += ele   
    
    # return string   
    return str1      
selected_state = listToString(states)   

new_df = merged[merged['Jurisdiction of Occurrence'].isin(states)]
new_df['Population'] = new_df['Population'].str.replace(',','').astype(float)
new_df['Capita'] = (new_df['All Cause']/new_df['Population']) * 1000
new_df['Capita_COVID'] = (new_df['COVID-19 (U071, Underlying Cause of Death)']/new_df['Population']) * 1000
#st.write(new_df)
df2 = new_df
df3 = new_df 


#plot 1
new_df = new_df.drop(['All Cause','COVID-19 (U071, Multiple Cause of Death)','Jurisdiction of Occurrence','States'],axis=1)
fig, ax = plt.subplots()
plt.figure(figsize=(13,7))
#st.write(new_df)
plt.title("Weekly COVID-19 Deaths (2019-2020) for " + selected_state, fontsize = 20, style = 'normal')
sns.lineplot('MMWR Week','Capita_COVID',hue='MMWR Year',data=new_df,ci=None,palette = ['red','black'],legend = 'full')
axes1 = plt.gca()
axes1.set_xlabel("Week Number")
plt.ylabel("Capita per 1000")
x= new_df['MMWR Week']
plt.xticks(np.arange(1, 53, 1.0))
plt.xticks(rotation=90)
plt.grid(linewidth=0.5)
st.pyplot()

#st.markdown(" :warning: Note that the number of deaths reported in this graph may be incomplete due to lag in time (approx. 6 - 8 weeks) between the time the death occured and when the death certificate is completed.") 
    

#new_df['month'] = pd.DatetimeIndex(new_df['Week Ending Date']).month
#new_df['month'] = new_df['month'].apply(lambda x: calendar.month_abbr[x])
#plt.style.use('fivethirtyeight')
#plt.grid(color='#d4d4d4')
#fig, ax = plt.subplots(figsize=(10,6))
#new_df=new_df.groupby(['MMWR Week','MMWR Year']).mean().unstack()
#st.write(new_df)
#plot = new_df.plot.bar(figsize = (12,9))
#plot.legend(loc = 'upper right')
#plot.set_title("COVID-19 (Underlying Cause of Death) Deaths") 
#plot.set_xlabel("Week Number")
#plot.set_ylabel("Number of Deaths")
#plot.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))


#st.pyplot()



#plot 2

df2 = df2.drop(['COVID-19 (U071, Multiple Cause of Death)','COVID-19 (U071, Underlying Cause of Death)','Population','All Cause','Jurisdiction of Occurrence','States'],axis = 1)
fig, ax = plt.subplots()
df2['month'] = pd.DatetimeIndex(df2['Week Ending Date']).month
df2['month_name'] = df2['month'].apply(lambda x: calendar.month_abbr[x])
df2['date'] = pd.DatetimeIndex(df2['Week Ending Date']).date
df2['date'] = pd.to_datetime(df2['date'],format = '%Y-%m-%d')
df2['MM-DD'] = df2['date'].dt.strftime('%m-%d')

#df2=df2.groupby(['MMWR Week','MMWR Year']).mean().unstack()
#st.write(df2)
plt.figure(figsize=(13,7))
plt.title("Weekly All Cause Deaths (2019-2020) for "+selected_state, fontsize = 20, style = 'normal')
sns.lineplot('MMWR Week','Capita',hue='MMWR Year',data=df2,ci=None,legend = 'full',palette = ['red','black'],sort = False)
axes1 = plt.gca()
axes1.set_xlabel("Week Number")
plt.ylabel("Capita per 1000")
x= df2['MMWR Week']
plt.xticks(np.arange(1, 53, 1.0))
plt.xticks(rotation=90)
#axes2 = axes1.twiny()
#axes2.set_xlabel("Month")
#ticks = np.arange(0,13,1)
#axes2.set_xticks(ticks)
plt.grid(linewidth = 0.5)
st.pyplot()
st.markdown(" :warning: Note that the number of deaths reported in this graph may be incomplete due to lag in time (approx. 6 - 8 weeks) between the time the death occured and when the death certificate is completed.")
st.markdown("---")
st.write("Weekly Death Rates for ",selected_state)
st.write(df3)
st.write("Weekly Death Rates for all states")
st.write(merged)









