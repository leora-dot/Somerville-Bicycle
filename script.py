import pandas as pd
import datetime

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
#VISUALIZE AS STACKED BAR CHARTS OVER TIME.

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

#print(crash_bike_time_df)

#Combined Date by Date
dates_df = pd.DataFrame(date_list, columns = ["date"])
combo_by_dates_df = pd.merge(dates_df, police_bike_time_pivot_df, how = "outer")
combo_by_dates_df = pd.merge(combo_by_dates_df, crash_bike_time_df, how = "outer")
combo_by_dates_df["BIKEVIOL"] = combo_by_dates_df["BIKEVIOL"].fillna(0)
combo_by_dates_df["BIKE CRASH"] = combo_by_dates_df["BIKE CRASH"].fillna(0)
combo_by_dates_df["BIKE STOP"] = combo_by_dates_df["BIKE STOP"].fillna(0)


print(combo_by_dates_df)


#QUESTION II:
#IF THERE APPEARS TO BE A CHRONOLOGICAL CONNECTION, IS THERE ALSO A GEOGRAPHICAL ONE?
#FIGURE OUT HOW TO TURN CROSS STREETS IN CRASH DATA INTO APPROXIMATE GPS COORDINATES (FOR FREE!) IN ORDER TO VISUALIZE.
