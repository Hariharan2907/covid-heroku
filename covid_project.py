import pandas as pd
import streamlit as st

import matplotlib.pyplot as plt

from matplotlib.dates import DateFormatter
import matplotlib.ticker as ticker
from pylab import *

url="https://data.cdc.gov/api/views/muzy-jte6/rows.csv?accessType=DOWNLOAD"
#df=pd.read_csv(url,error_bad_lines=False)
def load_data():
    df_filter=pd.read_csv(url,error_bad_lines=False, usecols=["Jurisdiction of Occurrence","MMWR Year","MMWR Week","Week Ending Date","All Cause","COVID-19 (U071, Multiple Cause of Death)","COVID-19 (U071, Underlying Cause of Death)"])
    return df_filter
df_filter = load_data()

#gk = df_filter.groupby('Jurisdiction of Occurrence')
#list1 = gk.groups

states = st.sidebar.multiselect("Choose states",df_filter['Jurisdiction of Occurrence'].unique())

    
st.write("Weekly Death Rate")
new_df = df_filter[df_filter['Jurisdiction of Occurrence'].isin(states)]
st.write(new_df)
df2 = new_df

#plot 1
new_df = new_df.drop(['All Cause','COVID-19 (U071, Multiple Cause of Death)'],axis=1)
#new_df['month'] = pd.DatetimeIndex(new_df['Week Ending Date']).month
#new_df['month'] = new_df['month'].apply(lambda x: calendar.month_abbr[x])
plt.style.use('fivethirtyeight')
plt.grid(color='#d4d4d4')
#fig, ax = plt.subplots(figsize=(10,6))
new_df=new_df.groupby(['MMWR Week','MMWR Year']).mean().unstack()
st.write(new_df)
plot = new_df.plot.bar(figsize = (12,9))
plot.legend(loc = 'upper right')
plot.set_title("COVID-19 (Underlying Cause of Death) Deaths")
plot.set_xlabel("Week Number")
plot.set_ylabel("Number of Deaths")
plot.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))


st.pyplot()

#plot 2
df2 = df2.drop(['COVID-19 (U071, Multiple Cause of Death)','COVID-19 (U071, Underlying Cause of Death)'],axis = 1)
#fig, ax = plt.subplots(figsize=(10,6))
#df2['month'] = pd.DatetimeIndex(df2['Week Ending Date']).month
df2=df2.groupby(['MMWR Week','MMWR Year']).mean().unstack()

plot1 = df2.plot.bar(figsize = (12,9))
plot1.legend()
plot1.set_title("All Cause Deaths")
plot1.set_xlabel("Week Number")
plot1.set_ylabel("Number of Deaths")
st.pyplot()




#years = st.sidebar.multiselect("Choose the year",new_df['year'].unique())
#final = new_df[new_df['year'].isin(years)]

#is_2019 = new_df['year'] == 2019
#final_2019 = new_df[is_2019]
#ax = final_2019.plot(x="Week Ending Date", y="COVID-19 (U071, Multiple Cause of Death)", kind='scatter')

#is_2020 = new_df['year'] == 2020
#final_2020 = new_df[is_2020]
#final_2020.plot(y="COVID-19 (U071, Multiple Cause of Death)",ax=ax,kind="scatter")

#fig, ax = plt.subplots(figsize=(10,6))
#new_df=new_df.groupby(['month','year']).mean().unstack()
#st.write(new_df)
#new_df.plot(ax=ax)

#ax.set_title(label='COVID-19 (U071, Underlying Cause of Death) in 2019 and 2020')
#ax.legend(loc = 'upper right')

#st.pyplot()

#df2 = df2.drop(['COVID-19 (U071, Multiple Cause of Death)','COVID-19 (U071, Underlying Cause of Death)'],axis = 1)
#df2['year'] = pd.DatetimeIndex(df2['Week Ending Date']).year
#df2['month'] = pd.DatetimeIndex(df2['Week Ending Date']).month
#fig, ax = plt.subplots(figsize=(10,6))
#df2.groupby(['month','year']).mean().unstack().plot(ax=ax)
#ax.set_title(label='All Cause Deaths in 2019 and 2020')
#ax.legend(loc = 'bottom left')
#st.pyplot()


#new_df.groupby(['month','year']).mean().unstack().plot(x="Week Ending Date", y="COVID-19 (U071, Multiple Cause of Death)", kind='scatter')







