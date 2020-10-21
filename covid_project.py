import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import calendar 
import datetime 
import urllib
import matplotlib.dates as m_dates
import matplotlib.ticker as ticker

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
@st.cache
def load_data():
    df_filter=pd.read_csv(url,error_bad_lines=False, usecols=["Jurisdiction of Occurrence","MMWR Year","MMWR Week","Week Ending Date","All Cause","COVID-19 (U071, Multiple Cause of Death)","COVID-19 (U071, Underlying Cause of Death)"])
    return df_filter



#population dataset
pop = pd.read_csv("Population.csv")
us_pop = 328239523  

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
us_df = df_filter[df_filter['Jurisdiction of Occurrence'] == 'United States']



if not states:
    us_df['Population'] = us_pop
    us_df['Capita'] = (us_df['All Cause']/us_df['Population']) * 1000
    us_df['Capita_COVID'] = (us_df['COVID-19 (U071, Underlying Cause of Death)']/us_df['Population']) * 1000
    us_df['month'] = pd.DatetimeIndex(us_df['Week Ending Date']).month
    us_df['month_name'] = us_df['month'].apply(lambda x: calendar.month_abbr[x])
    

    
    us_df = us_df.drop(['COVID-19 (U071, Multiple Cause of Death)','COVID-19 (U071, Underlying Cause of Death)','Population','All Cause','Jurisdiction of Occurrence'],axis = 1)
    us_df_rem = us_df.tail(6)
    us_df.drop(us_df.tail(5).index,inplace=True)
    
    st.write(us_df_rem)
    ()
    #---------------------------------------------------------------------------------------------------------------------
    plt.figure(figsize=(13,7))
    plt.title("Weekly All Cause Deaths (2019-2020) for the United States", fontsize = 20, style = 'normal')
    sns.lineplot('MMWR Week','Capita',hue='MMWR Year',data=us_df,ci=None,legend = 'full',palette = ['blue','black'],sort = False)
    sns.lineplot('MMWR Week','Capita',data=us_df_rem,ci=None,palette = ['red'],sort = False,dashes = [(2,2)])
    
    axes1 = plt.gca()
    axes1.set_xlabel("Week Number")
    plt.ylabel("Capita per 1000")
    x= us_df['MMWR Week']
    y= us_df['Capita']
    plt.xticks(np.arange(1, 53, 1.0))
    plt.xticks(rotation=90)
    plt.grid(linewidth = 0.5)
    locs, labels = plt.xticks()
    axes2 = axes1.twiny()
    newlabel = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    axes2.set_xticklabels(newlabel)
    newpos = np.arange(0.56,12.56,0.93)
    axes2.set_xticks(newpos)
    axes2.xaxis.set_ticks_position('bottom')
    axes2.xaxis.set_label_position('bottom')
    axes2.spines['bottom'].set_position(('outward', 36))
    axes2.set_xlabel('Month')
    st.pyplot()
    #---------------------------------------------------------------------------------------------------------------------
    plt.figure(figsize=(13,7))
    plt.title("Weekly COVID-19 Deaths (2019-2020) for the United States", fontsize = 20, style = 'normal')
    sns.lineplot('MMWR Week','Capita_COVID',hue='MMWR Year',data=us_df,ci=None,palette = ['blue','black'],legend = 'full')
    sns.lineplot('MMWR Week','Capita_COVID',data=us_df_rem,ci=None,palette = ['red'],sort = False,dashes = [(2,2)])
    axes1 = plt.gca()
    axes1.set_xlabel("Week Number")
    plt.ylabel("Capita per 1000")
    x= us_df['month']
    plt.xticks(np.arange(1, 53, 1.0))
    plt.xticks(rotation=90)
    plt.grid(linewidth=0.5)

    axes2 = axes1.twiny()
    newlabel = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    axes2.set_xticklabels(newlabel)
    newpos = np.arange(0.56,12.56,0.923)
    axes2.set_xticks(newpos)
    axes2.xaxis.set_ticks_position('bottom')
    axes2.spines['bottom'].set_position(('outward', 36))
    st.pyplot()
    st.write(us_df)
    st.markdown(" :warning: Note that the number of deaths reported in this graph may be incomplete due to lag in time (approx. 6 - 8 weeks) between the time the death occured and when the death certificate is completed.")
    st.markdown("---")
    st.write("Data Source: Weekly Counts of Deaths by State and Select Causes, 2019-2020, https://data.cdc.gov/NCHS/Weekly-Counts-of-Deaths-by-State-and-Select-Causes/muzy-jte6")
#---------------------------------------------------------------------------------------------------------------------    
#functions    
def listToString(s):      
    str1 = ""      
    for ele in s:  
        str1 += ele
    return str1

if states:    
    selected_state = listToString(states)   
    new_df = merged[merged['Jurisdiction of Occurrence'].isin(states)]
    new_df['Population'] = new_df['Population'].str.replace(',','').astype(float)
    new_df['Capita'] = (new_df['All Cause']/new_df['Population']) * 1000
    new_df['Capita_COVID'] = (new_df['COVID-19 (U071, Underlying Cause of Death)']/new_df['Population']) * 1000
    #st.write(new_df)
    df2 = new_df 
    df3 = new_df 
#---------------------------------------------------------------------------------------------------------------------


    new_df = new_df.drop(['All Cause','COVID-19 (U071, Multiple Cause of Death)','Jurisdiction of Occurrence','States'],axis=1)
    fig, ax = plt.subplots()
    plt.figure(figsize=(13,7))
    df2 = df2.drop(['COVID-19 (U071, Multiple Cause of Death)','COVID-19 (U071, Underlying Cause of Death)','Population','All Cause','Jurisdiction of Occurrence','States'],axis = 1)
    fig, ax = plt.subplots()
    df2['month'] = pd.DatetimeIndex(df2['Week Ending Date']).month
    df2['month_name'] = df2['month'].apply(lambda x: calendar.month_abbr[x])
    df2['date'] = pd.DatetimeIndex(df2['Week Ending Date']).date
    df2['date'] = pd.to_datetime(df2['date'],format = '%Y-%m-%d')
    df2['MM-DD'] = df2['date'].dt.strftime('%m-%d')

    #plot 1
    plt.figure(figsize=(13,7))
    plt.title("Weekly All Cause Deaths (2019-2020) for "+selected_state, fontsize = 20, style = 'normal')
    sns.lineplot('MMWR Week','Capita',hue='MMWR Year',data=df2,ci=None,legend = 'full',palette = ['red','black'],sort = False)
    axes1 = plt.gca()
    axes1.set_xlabel("Week Number")
    plt.ylabel("Capita per 1000")
    x= df2['MMWR Week']
    y= df2['Capita']
    plt.xticks(np.arange(1, 53, 1.0))
    plt.xticks(rotation=90)
    plt.grid(linewidth = 0.5)
    locs, labels = plt.xticks()
    axes2 = axes1.twiny()
    newlabel = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    axes2.set_xticklabels(newlabel)
    newpos = np.arange(0.56,12.56,0.923)
    axes2.set_xticks(newpos)
    axes2.xaxis.set_ticks_position('bottom')
    axes2.xaxis.set_label_position('bottom')
    axes2.spines['bottom'].set_position(('outward', 36))
    axes2.set_xlabel('Month')
    st.pyplot()
#---------------------------------------------------------------------------------------------------------------------
    #plot 2

    plt.title("Weekly COVID-19 Deaths (2019-2020) for " + selected_state, fontsize = 20, style = 'normal')
    sns.lineplot('MMWR Week','Capita_COVID',hue='MMWR Year',data=new_df,ci=None,palette = ['red','black'],legend = 'full')
    axes1 = plt.gca()
    axes1.set_xlabel("Week Number")
    plt.ylabel("Capita per 1000")
    x= new_df['MMWR Week']
    plt.xticks(np.arange(1, 53, 1.0))
    plt.xticks(rotation=90)
    plt.grid(linewidth=0.5)
    axes2 = axes1.twiny()
    newlabel = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    axes2.set_xticklabels(newlabel)
    newpos = np.arange(0.56,12.56,0.923)
    axes2.set_xticks(newpos)
    axes2.xaxis.set_ticks_position('bottom')
    axes2.spines['bottom'].set_position(('outward', 36))
    st.pyplot()


#---------------------------------------------------------------------------------------------------------------------
    #notes 
    st.markdown(" :warning: Note that the number of deaths reported in this graph may be incomplete due to lag in time (approx. 6 - 8 weeks) between the time the death occured and when the death certificate is completed.")
    st.markdown("---")
    st.write("Weekly Death Rates for ",selected_state)
    st.write(df3)
    st.write("Weekly Death Rates for all states")
    st.write(merged)
    st.write("Data Source: Weekly Counts of Deaths by State and Select Causes, 2019-2020, https://data.cdc.gov/NCHS/Weekly-Counts-of-Deaths-by-State-and-Select-Causes/muzy-jte6")








