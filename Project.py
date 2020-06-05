#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  3 17:09:46 2020

@author: rohitmathew and guoyichen
"""

# make sure to install these packages before running:
# pip install sodapy

import pandas as pd
from sodapy import Socrata
from datetime import datetime,date
import matplotlib.pyplot as plt

## Below section of codes obtains data

client = Socrata("health.data.ny.gov", None)
results = client.get("xdss-u53e", limit=50000)
data = pd.DataFrame.from_records(results)

## Below section cleans and makes data points into a readable format in Python

df = data.sort_values(by=['county', "test_date"])
df["new_positives"] = pd.to_numeric(df["new_positives"],errors='coerce')
df["cumulative_number_of_positives"] = pd.to_numeric(df["cumulative_number_of_positives"],errors='coerce')
df["total_number_of_tests"] = pd.to_numeric(df["total_number_of_tests"],errors='coerce')
df["cumulative_number_of_tests"] = pd.to_numeric(df["cumulative_number_of_tests"],errors='coerce')
df['test_date']= pd.to_datetime(df['test_date'])
#df['test_date'] = df['test_date'].dt.date


# Asks for country and puts into correct format
def county_name():
    county_name = input("What county in NYS do you want info on? ")
    county_name = county_name.capitalize()
    return county_name
    
# Asks for a date and puts into correct format
def what_date():
    date = input("Please enter a date in mmDDyyyy format: ")
    date = datetime.strptime(date,'%m%d%Y')
    return date

# For county infomation on dataframe.
def county_df ():
    name = county_name()
    data = df[(df.county == name)]
    return (data)

# For total cases by day in NYS
def by_date():
    df1 = df.groupby('test_date', as_index=False)['new_positives'].sum()
    return df1

"""
# Returns dataframe on selected county
#def county_date():
    #county_data = county(county_name)
"""
# Barchart showing ditrubution of new cases. Needs some fixing.
#ax = county_data.plot.bar(x='test_date', y='new_positives', rot=0)



### CODE BELOW FOR MENU
def menu():
    print("")
    print ("MAIN MENU:","\n1. Current County Statistics \n2. County Information on Certain date \n3. County with highest and lowest total positive cases \n4. Number of New Cases per Day in NYS; Barchart \n5. Summary of new cases in county by date; Barchart") 
    number = input("Enter your selection: ")
    number = int(number)
    
    #  County statistics
    if number == 1:
        county_info = county_df()
        total_pos = county_info["new_positives"].sum()
        total_tests = county_info["total_number_of_tests"].sum()
        total_neg = total_tests - total_pos
        pencentage_of_positives= total_pos/total_tests *100
        print("Information as of: ",max(df['test_date']) ,"\nTotal Number of Postives Cases are: ", total_pos, "\nTotal Number of Negatives are: ", total_neg, "\nTotal number of tests are: ", total_tests,"\n% of positive cases: ", pencentage_of_positives)
        menu()
    
    # County Information on Certain date
    elif number == 2:
        county = county_name()
        date = what_date()
        date_info = df.loc[(df['test_date'] == date) & (df['county'] == county)]
        day_pos = (date_info["new_positives"]).sum()
        day_total = (date_info["total_number_of_tests"]).sum()
        day_neg = day_total - day_pos
        print("Cases for date:  ", date, "\nNumber of Postives Cases: ", day_pos, "\nNumber of Negative Cases: ", day_neg, "\nNumber of tests done were: ", day_total)
        menu()
    
    # County with highest total cases
    elif number == 3:
        data = df[(df["test_date"] == max(df['test_date']))] 
        data3 = (data[data.cumulative_number_of_positives == data.cumulative_number_of_positives.max()])
        opt_3 = data3[['county','cumulative_number_of_positives']]
        data4 = (data[data.cumulative_number_of_positives == data.cumulative_number_of_positives.min()])
        opt_4 = data4[['county','cumulative_number_of_positives']]
        print (opt_3.iat[0, 0], "has the hightest number of positive cases with", opt_3.iat[0, 1], "cases.")
        print (opt_4.iat[0, 0], "has the lowest number of positive cases with", opt_4.iat[0, 1], "cases.")
        menu()

    
    # Dataframe ~ BARCHART Number of Positive New Cases per Day in NYS
    elif number == 4:
        data4 = df.groupby(["test_date"])[["new_positives"]].sum()
        print(data4)
        ans = input("Would you like a barchart of this data? y or n: ").lower()
        if ans == "y":
            ax = data4.plot(kind='bar')
            ax.axes.get_xaxis().set_visible(False)
            plt.xlabel('test date')
            plt.ylabel('numbers of new positive cases')
            plt.title('Number of Positive New Cases per Day in NYS')
            plt.grid(True)
            plt.show()
            menu()

        else:
            menu()
    
    # BARCHART summary of new cases in county by date
    elif number == 5:
        county_info = county_df()
        data5 = county_info.groupby(["test_date"])[["new_positives"]].sum()
        print(data5)
        ans = input("Would you like a barchart of this data? y or n: ").lower()
        if ans == "y":
            ax = data5.plot(kind='bar')
            ax.axes.get_xaxis().set_visible(False)
            plt.xlabel('test date')
            plt.ylabel('numbers of new positive cases in this county')
            plt.title('Summary of New Cases in the County')
            plt.grid(True)
            plt.show()
            menu()
        else:
            menu()
        

    else:
        print("\nInvalid Selection, try again.")
        menu()
        
        

menu()

