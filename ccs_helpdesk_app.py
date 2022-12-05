## Mid term project ##

import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px
from datetime import datetime

# Global settings
st.set_option('deprecation.showPyplotGlobalUse', False)

# Read HelpDesk data
help_desk_data = pd.read_csv("data/helpdesk_data.csv")

# Convert the Date Created & Closed Date to a date format and extract the year for the dropdown box
help_desk_data["Date Created"] = pd.to_datetime(help_desk_data["Date Created"])
help_desk_data["Closed Date"] = pd.to_datetime(help_desk_data["Closed Date"])
years = pd.to_datetime(help_desk_data['Date Created'], errors='coerce').dt.year.astype(object)
help_desk_data["Year Created"] = pd.to_datetime(help_desk_data['Date Created'], errors='coerce').dt.year.astype(object)

# Get unique values of year
unique_years = years.unique()

# Create values for dropdown box
opt = np.append(["all years"],unique_years)

year = st.sidebar.selectbox("Please select a year:", opt)
st.sidebar.image("..\HelpDeskVertical.jpg", use_column_width=True)

# Preprocessing
# get total count of records  
total_tickets = len(help_desk_data)

# get count of records for selected year(s)
if year == "all years":
    open_tickets = np.sum(help_desk_data['Current Status'] == "Open")
    closed_tickets = np.sum(help_desk_data['Current Status'] == "Closed")
    resolved_tickets = np.sum(help_desk_data['Current Status'] == "Resolved")
    ticket_count = total_tickets

    # Calculating time to close tickets
    help_desk_data["Date Created"] = help_desk_data["Date Created"].dt.date
    help_desk_data["Closed Date"] = help_desk_data["Closed Date"].dt.date
    help_desk_data["Time_to_Close"] = (help_desk_data["Closed Date"] - help_desk_data["Date Created"]) / np.timedelta64(1, 'D')
    help_desk_data['Time_to_Close'].round()

    # Combine some bins of closed ticket timelines to make graph more readable
    help_desk_data.loc[help_desk_data['Time_to_Close'] > 14, 'Time_to_Close'] = 14
    all_help_desk_data = help_desk_data

else:
    #count occurrences of each unique value
    open_tickets = np.sum((help_desk_data['Current Status'] == "Open") & (years == year))
    closed_tickets = np.sum((help_desk_data['Current Status'] == "Closed") & (years == year))
    resolved_tickets = np.sum((help_desk_data['Current Status'] == "Resolved") & (years == year))
    ticket_count = np.sum(years == year)
    filtered_df_by_year = help_desk_data.loc[help_desk_data['Year Created'] == year]

    # Calculating time to close tickets for year selected
    filtered_df_by_year["Date Created"] = filtered_df_by_year["Date Created"].dt.date
    filtered_df_by_year["Closed Date"] = filtered_df_by_year["Closed Date"].dt.date
    filtered_df_by_year["Time_to_Close"] = (filtered_df_by_year["Closed Date"] - filtered_df_by_year["Date Created"]) / np.timedelta64(1, 'D')
    filtered_df_by_year['Time_to_Close'].round()

    # Combine some bins of closed ticket timelines to make graph more readable
    filtered_df_by_year.loc[filtered_df_by_year['Time_to_Close'] > 14, 'Time_to_Close'] = 14
    help_desk_data = filtered_df_by_year
   
# Set up tabs on user interface
tab1,tab2,tab3,tab4 = st.tabs([' Overview ', ' Team Member Contributions ', ' Departments Served ',' Yearly Ticket Trends '])

# Tabs
with tab1:
    #st.write("<h4 style='text-align: center; color: gray;'>{temp}</h1>".format(temp = year), unsafe_allow_html=True)

    col1, col2= st.columns(2)
    with col1:

        st.write('<p style="font-family:sans-serif; color:Navy; font-size: 20px;"> Open Tickets: <b>{temp1}</b></p>'.format(temp1 = open_tickets), unsafe_allow_html=True)
        st.write('<p style="font-family:sans-serif; color:Navy; font-size: 20px;"> Closed Tickets: <b>{temp2}<b/></p>'.format(temp2 = closed_tickets), unsafe_allow_html=True)

    with col2:

        st.write('<p style="font-family:sans-serif; color:Navy; font-size: 20px;">Resolved Tickets: <b>{temp3}</b></p>'.format(temp3 = resolved_tickets), unsafe_allow_html=True)
        st.write('<p style="font-family:sans-serif; color:Navy; font-size: 20px;">Total Tickets: <b>{temp4}<b/></p>'.format(temp4 = ticket_count), unsafe_allow_html=True)

    fig = px.histogram(data_frame=help_desk_data, x='Time_to_Close', title="Count of Tickets by Number of Days to Close",
    labels=dict(Time_to_Close="Number of Days to Close" ), color_discrete_sequence=['navy'],
    width=500, height=500,)
    labels = ["<= 1","1+", "2", "3", "4", "5", "6", "7", "8", "9", "10","11","12", "13", ">= 14"]
    fig.update_xaxes(tickvals=np.arange(15), ticktext=labels)
    fig.update_layout(title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Team Member Contributions")

    if year == "all years":

        #Bar Chart
        
        fig2 = px.bar(help_desk_data, x=help_desk_data["Agent Assigned"].value_counts(), y=help_desk_data["Agent Assigned"].value_counts().index, orientation='h', title=year)
        fig2.update_traces(marker_color='gold')
        fig2.update_layout(title_x=0.5,
        xaxis_title="Count of Tickets",
        yaxis_title="Team Member")
        st.plotly_chart(fig2, use_container_width=True)

    else:

        # Create bar chart for selected year
        fig2 = px.bar(help_desk_data, x=help_desk_data["Agent Assigned"].value_counts(), y=help_desk_data["Agent Assigned"].value_counts().index, orientation='h', title=year)
        fig2.update_traces(marker_color='gold')
        fig2.update_layout(title_x=0.5,
        xaxis_title="Count of Tickets",
        yaxis_title="Team Member")
        st.plotly_chart(fig2, use_container_width=True)

with tab3:
    st.subheader("Tickets by Department")

    # Pie Chart
    fig3 = px.pie(help_desk_data, values=help_desk_data['Department'].value_counts(), names=help_desk_data['Department'].value_counts().index, title=year)
    fig3.update_layout(title_x=0.5)
    st.plotly_chart(fig3, use_container_width=True)

with tab4:
    st.subheader("Yearly Ticket Trends")

    if year == 'all years':
        
        ts_df = [pd.to_datetime(all_help_desk_data["Date Created"]).dt.year.rename('year'), pd.to_datetime(all_help_desk_data["Date Created"]).dt.month.rename('month')]
        ts_df = pd.DataFrame(ts_df)
        ts_df = pd.DataFrame.transpose(ts_df)
        ts_df_count =(ts_df.groupby(['year','month'])['month'].count())
        ts_df_count = pd.DataFrame(ts_df_count).reindex()

        ts_df_count = ts_df_count.rename(columns={'month': 'Count of Tickets'})

        fig4 =  px.line(data_frame=ts_df_count, x= ts_df_count.index.get_level_values(1), y="Count of Tickets", color=ts_df_count.index.get_level_values(0),
                        labels={"x":"Month"}, title=year)
        fig4.update_layout(title_x=0.5)
        fig4.update_xaxes(nticks=12)
        st.plotly_chart(fig4, use_container_width=True)

    else:
        ts_s = pd.to_datetime(help_desk_data["Date Created"], errors='coerce').dt.month.astype(object).value_counts().sort_index()
        ts_df = pd.DataFrame(ts_s)
        ts_df.columns = ['Count of Tickets']

        fig4 =  px.line(data_frame=ts_df, y="Count of Tickets", labels=dict(index="Month"), title=year)
        fig4.update_layout(title_x=0.5)
        fig4.update_xaxes(nticks=12)
        st.plotly_chart(fig4, use_container_width=True)


