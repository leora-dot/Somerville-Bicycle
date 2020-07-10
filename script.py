import pandas as pd
import datetime
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.dates as mdates

police_df = pd.read_csv("Police_Traffic_Enforcement_Activity.csv")
crash_df = pd.read_csv("Motor_Vehicle_Crash_Reports.csv")

#EQUALIZING DATES

#creating date column for police data
police_df['str_split'] = police_df.dtreceived.str.split(" ")
police_df["date"] = police_df.str_split.str.get(0)
police_df["date"] = pd.to_datetime(police_df.date)
police_df.drop(columns = ["str_split"], inplace = True)

#formating date column for crash data
crash_df["Date"] = pd.to_datetime(crash_df.Date)

#Identifying date cutoffs
min_police_date = min(police_df.date)
max_police_date = max(police_df.date)

min_crash_date = min(crash_df.Date)
max_crash_date = max(crash_df.Date)

min_date = max(min_crash_date, min_police_date)
max_date = min(max_crash_date, max_police_date)

date_list = pd.date_range(min_date, max_date).tolist()

#print(min_date)
#print(max_date)

#Limiting both dfs to overlapping time periods only
police_df = police_df[ (police_df.date >= min_date) & (police_df.date <= max_date) ].reset_index(drop = True)
crash_df = crash_df[ (crash_df.Date >= min_date) & (crash_df.Date <= max_date) ].reset_index(drop = True)

#CREATING & CLEANING BIKE POLICE DATA

police_bike_df = police_df[ (police_df.inctype == "BIKEVIOL") | (police_df.inctype == "BIKE STOP") ].reset_index(drop = True)

police_bike_df.drop(columns = ["incnum", "inctypecode", "dtreceived", "stnum", "stname2"], inplace = True)


#print(police_bike_df.dtypes)

#CREATING & CLEANING BIKE CRASH DATA

crash_bike_df = crash_df[crash_df.Bicycle == 1].reset_index(drop = True)

crash_bike_df.drop(columns = ['City', 'Time', 'State', 'Weather (2&3)',
       'Road Surface (6)', 'Traffic Control Device (4)',
       'Intersection Type (7)', 'Traffic Way Desc (8)', '# of Involved Vehicles',
       'Vehicle1 Configuration (21)', 'Driver1 Contrib Code1 (25)',
       'Driver1 Contrib Code2 (25)', 'Vehicle2 Configuration (21)',
       'Driver2 Contrib Code1 (25)', 'Driver2 Contrib Code2 (25)',
       'Vehicle3 Configuration (21)', 'Driver3 Contrib Code1 (25)',
       'Driver3 Contrib Code2 (25)', 'Vehicle4 Configuration (21)',
       'Driver4 Contrib Code1 (25)', 'Driver4 Contrib Code2 (25)',
       'Vehicle5 Configuration (21)', 'Driver5 Contrib Code1 (25)',
       'Driver5 Contrib Code2 (25)', 'Vehicle6 Configuration (21)',
       'Driver6 Contrib Code1 (25)', 'Driver6 Contrib Code2 (25)',
       'Vehicle7 Configuration (21)', 'Driver7 Contrib Code1 (25)',
       'Driver7 Contrib Code2 (25)', 'Bicycle', 'Pedestrian', 'Non-MV',
       'Non-Motorist Location (16)', 'Non-Motorist Action (15)',
       'Non-Motorist Type',
       'Injury', 'Multiple', 'Gender1', 'Age1', 'Severity1', 'Hospital1',
       'Gender2', 'Age2', 'Severity2', 'Hospital2', 'Gender3', 'Age3',
       'Severity3', 'Hospital3', 'Gender4', 'Age4', 'Severity4', 'Hospital4',
       'Gender5', 'Age5', 'Severity5', 'Hospital5', 'City Vehicle?', 'Notes',
       'column 65', 'column 66', 'column 67', 'column 68', 'column 69',
       'column 70', 'column 71', 'column 72', 'column 73', 'column 74',
       'column 75', 'column 76', 'column 77', 'column 78', 'column 79',
       'column 80', 'column 81', 'column 82', 'column 83', 'column 84',
       'column 85', 'column 86', 'column 87', 'column 88', 'column 89', 'Collision Manner (11)', 'Manner of Non-Motorist (Person) Collision'], inplace = True)

crash_bike_df.rename(columns = {"Date": "date"}, inplace = True)

#print(crash_bike_df.head())
#print(crash_bike_df.columns)

#COMPARING DATA

#QUESTION I:
#ARE MORE LIKELY TO STOP CYCLISTS IMMEDIATELY AFTER CYCLISTS HAVE BEEN HIT BY CARS?
#FOR EACH DAY IN THE TIME PERIOD, HOW MANY CRASHES WITH CYCLISTS HAVE OCCURED? HOW MANY CYCLIST STOPS HAVE OCCURED?

#QUESTION I, METHOD I
#WHAT CAN YOU SEE BY OBSERVING THE DATA VISUALLY?

#Police Stops by Day
police_bike_time_df = police_bike_df.groupby(["date", "inctype"]).stname1.count().reset_index()
police_bike_time_df.rename(columns = {"stname1":"count"}, inplace = True)
police_bike_time_pivot_df = police_bike_time_df.pivot(columns = "inctype", index = "date", values = "count").reset_index()
police_bike_time_pivot_df["BIKE STOP"] = police_bike_time_pivot_df["BIKE STOP"].fillna(0)
police_bike_time_pivot_df["BIKEVIOL"] = police_bike_time_pivot_df["BIKEVIOL"].fillna(0)

#print(police_bike_time_pivot_df)

#Crashes by Day

#print(crash_bike_df.head())
crash_bike_time_df = crash_bike_df.groupby(["date",]).Location.count().reset_index()
crash_bike_time_df.rename(columns = {"Location" :"BIKE CRASH"}, inplace = True)

#Combined Date by Date
dates_df = pd.DataFrame(date_list, columns = ["date"])
combo_by_dates_df = pd.merge(dates_df, police_bike_time_pivot_df, how = "outer")
combo_by_dates_df = pd.merge(combo_by_dates_df, crash_bike_time_df, how = "outer")
combo_by_dates_df["BIKEVIOL"] = combo_by_dates_df["BIKEVIOL"].fillna(0)
combo_by_dates_df["BIKE CRASH"] = combo_by_dates_df["BIKE CRASH"].fillna(0)
combo_by_dates_df["BIKE STOP"] = combo_by_dates_df["BIKE STOP"].fillna(0)

#combo_by_dates_df["date"] = combo_by_dates_df["date"].apply(str)

#Visualizing Trends

def crash_and_stop_visualizer(date_cutoff_list):
    num_periods = len(date_cutoff_list)
    #plt.figure(figsize=(15, 4*num_periods))
    plt.figure(figsize = (10, 10))

    for i in range(num_periods):
        #limit data to correct range
        cutoff_min_date, cutoff_max_date = date_cutoff_list[i][0], date_cutoff_list[i][1]
        combo_by_dates_df_cutoff = combo_by_dates_df[(combo_by_dates_df.date < cutoff_max_date) & (combo_by_dates_df.date > cutoff_min_date)].reset_index(drop = True)

        #generate label names
        year = pd.to_datetime(cutoff_min_date).year
        q1_dates = combo_by_dates_df_cutoff["date"].values.tolist()
        q1_crashes = combo_by_dates_df_cutoff["BIKE CRASH"].values.tolist()
        q1_stops = combo_by_dates_df_cutoff["BIKE STOP"].values.tolist()
        q1_crashes_plus_stops = [q1_crashes[i] + q1_stops[i] for i in list(range(len(q1_dates)))]
        q1_viol = combo_by_dates_df_cutoff["BIKEVIOL"].values.tolist()
        #create visualization
        ax = plt.subplot(num_periods, 1, i+1)
        plt.bar(range(len(q1_dates)), q1_crashes, label = "Bike Crashes")
        plt.bar(range(len(q1_dates)), q1_stops, label = "Police Bike Stops", bottom = q1_crashes)
        plt.bar(range(len(q1_dates)), q1_viol, label = "Police Bike Violations", bottom = q1_crashes_plus_stops)

        #plt.legend()
        ax.set_ylim([0, 5.5])
        ax.set_xlim([0, 365])
        plt.title(year)
        #plt.ylabel("Number of Incidents")

        #if you were going to label every date
        #plt.xticks(np.arange(len(q1_dates)), (q1_dates), rotation = 45)
        
        months = mdates.MonthLocator()
        months_fmt = mdates.DateFormatter("%m")
        ax.xaxis.set_major_formatter(months_fmt)

        #if you're going to label each month
        #months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        #plt.xticks(range(1,13), (months), rotation = 45)


    #show & close
    plt.suptitle("Daily Bike Incidents")

    plt.tight_layout()
    plt.show()
    plt.close("all")

date_cutoffs_2010_2018 =[ [np.datetime64(datetime.date(i, 1, 1)), np.datetime64(datetime.date(i, 12, 31))] for i in range(2010, 2019)]

crash_and_stop_visualizer(date_cutoffs_2010_2018)

#What is wrong with this visualization:
    #need to space out subplots...it seems to resist every attempt to do so.
    #can you add a legends and titles that are shared by the whole figure?
    #add tickmarks and labels for dates. maybe by month?

#QUESTION I, METHOD 2
#WHAT IS STATISTICALLY SIGNIFICANT?

#just based on the visual inspection, I'm not sure whether this worthwhile.

#A regression predicting the number of bike tickets per day should do the trick. There are a couple of attributes it might make sense to look at:
    #days since last bike accident
    #accidents in last 30 days (rolling)
    #weekend vs weekday
    #month - there is some seasonality here. probably will be smartest to treat it is a categorical variable.
        #look into how scipy handles mutually exclusive variables - you may need to exclude one month...
    #it may make sense to truncate the data in order to exclude the years where bike stops either didn't happen or weren't recorded. Alternatively, treat year as a categorical variable.
    #how do you want to look at stops vs tickets? add them up? or treat seperately?



#QUESTION II:
#IF THERE APPEARS TO BE A CHRONOLOGICAL CONNECTION, IS THERE ALSO A GEOGRAPHICAL ONE?
#FIGURE OUT HOW TO TURN CROSS STREETS IN CRASH DATA INTO APPROXIMATE GPS COORDINATES (FOR FREE!) IN ORDER TO VISUALIZE.
