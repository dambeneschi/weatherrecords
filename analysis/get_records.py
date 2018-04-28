#! /usr/bin/env python3
#coding: utf-8

"""=====================================================================
Recover weather data from Darksky API,
format it to return a list of dictionaries
containing hourly weather data ("dataset") and
return a dataframe and create a CSV file
===================================================================== """

import time
import datetime
import urllib.request
import ast
import os
import logging
import numpy
import pandas


#Recover the raw data from the API and format them into a list of dict for each hour
def get(begining_date, ending_date, location1=50.0611, location2=19.9378):
    """ begining and engind_dates are formatted 'DD/MM/YYY'
    location 1 & 2 are the GPS coordinates, set by default in Krakow """

    #Request to Darksky API
    url0 = 'https://api.darksky.net/forecast/'
    key = 'f40237f800ab015ed15eebb56940857b'
    settings = '?units=si&exclude=currently,daily,flags'

    loc1 = str(location1)
    loc2 = str(location2)

    #Convert date argument into UNIX timestamp
    beg_stamp = time.mktime(datetime.datetime.strptime(begining_date, "%d/%m/%Y").timetuple())
    beg_stamp = int(beg_stamp)
    end_stamp = time.mktime(datetime.datetime.strptime(ending_date, "%d/%m/%Y").timetuple())
    end_stamp = int(end_stamp)

    #Send requests to the API
    timestamp = beg_stamp

    dataset = []
    while timestamp <= end_stamp:
        list_hourly_records = []
        #url to request API
        url = url0 + key + '/' + loc1 + ',' + loc2 + ',' + str(timestamp) + settings
        req = urllib.request.urlopen(url)
        day_data = str(req.read())
        
        #pick-up only the hourly records between {} with slicing
        beg_index = day_data.find("[")
        day_data = day_data[beg_index+2:]
        end_index = day_data.find("]")
        day_data = day_data[:end_index]
        
        #Split into a list for every hourly data
        list_hourly_records = day_data.split(",{")
        
        #Formating each hourly record to fulfill the dataset
        for hour in list_hourly_records:
            #format as a dictionnary
            dico = ast.literal_eval("{" + hour)
            dataset.append(dico)

        #next day
        timestamp += 86400

    #Return the unique weather parameters of the records
    list_parameters = []
    #Get the list of unique parameters automatically:
    for record in dataset:
        #for each values recorded
        for key, value in record.items():
            list_parameters.append(key)
    #List of weather parameters
    list_parameters = list(set(list_parameters))

    logging.info('Data recovered from Darksky API')

    #Turn the dataset into a dataframe using pandas
    global_values = []
    list_timestamps = []
    #Generate a list of lists with all weather values
    for record in dataset:
        hourly_values = []
        #List of timestamps that will be used for dataframe rows index
        list_timestamps.append(record['time'])
        for parameter in list_parameters:
            if parameter not in record:
                hourly_values.append("")
            else:
                hourly_values.append(record[parameter])
        global_values.append(hourly_values)

    #Turn into dataframe
    weather_array = numpy.array(global_values)
    weather_dataframe = pandas.DataFrame(weather_array, list_timestamps, list_parameters)

    #Create a CSV file from dataframe
    name1 = datetime.datetime.fromtimestamp(list_timestamps[0]).strftime("%d-%m-%y")
    name2 = datetime.datetime.fromtimestamp(list_timestamps[len(list_timestamps)-1]).strftime("%d-%m-%y")
    name = 'data_records_'+ name1 + '_' + name2 + '.csv'
    #Get the path of the above directory if the script by doing 2x '.dirname'
    directory = os.path.dirname(os.path.dirname(__file__))
    #Path to the /csv folder
    path = os.path.join(directory, 'CSV', name)

    weather_dataframe.to_csv(path, sep=',', encoding="utf-8")
    logging.info("CSV file created in /csv")

    return name
