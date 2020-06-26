import pandas as pd

police_df = pd.read_csv("Police_Traffic_Enforcement_Activity.csv")
crash_df = pd.read_csv("Motor_Vehicle_Crash_Reports.csv")

#Filtering Police DF to relevant pieces

#print(police_df.columns)
#print(police_df.inctype.value_counts())

police_bike_df = police_df[ (police_df.inctype == "BIKEVIOL") | (police_df.inctype == "BIKE STOP") ].reset_index(drop = True)

#print(police_bike_df.head(10))

#Filtering Crash DF to relevant pieces

#print(crash_df.columns)
#print(crash_df.Bicycle.value_counts())

crash_bike_df = crash_df[crash_df.Bicycle == 1].reset_index(drop = True)

print(crash_bike_df.head())
