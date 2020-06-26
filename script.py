import pandas as pd

police_df = pd.read_csv("Police_Traffic_Enforcement_Activity.csv")
crash_df = pd.read_csv("Motor_Vehicle_Crash_Reports.csv")

#CLEANING POLICE DATA

police_bike_df = police_df[ (police_df.inctype == "BIKEVIOL") | (police_df.inctype == "BIKE STOP") ].reset_index(drop = True)

#Create date column
police_bike_df['str_split'] = police_bike_df.dtreceived.str.split(" ")
police_bike_df["date"] = police_bike_df.str_split.str.get(0)
police_bike_df.drop(columns = ["str_split"], inplace = True)

police_bike_df.drop(columns = ["incnum", "inctypecode", "dtreceived", "stnum", "stname2"], inplace = True)

print(police_bike_df.head())
#print(police_bike_df.dtypes)

#CLEANING CRASH DATA

crash_bike_df = crash_df[crash_df.Bicycle == 1].reset_index(drop = True)

crash_bike_df.drop(columns = ['City', 'State', 'Weather (2&3)',
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

#print(crash_bike_df.head(10))
#print(crash_bike_df.columns)
