#! /usr/bin/env python3
#coding: utf-8

"""========================================================
Generate a dataframe of weather data from Darksky API from
CSV file created by get_records.py
============================================================"""

import os
import logging
import pandas

def ctd(file):
    """Convert a csv file in /CSV with weather data into a dataframe"""
    directory = os.path.dirname(os.path.dirname(__file__))
    path = os.path.join(directory, 'csv', file)
    logging.info("Opening CSV file {} from directory {}".format(file, path))

    try:
        #get_records generate a .csv file with "," as separations
        weather_dataframe = pandas.read_csv(path, sep=",")
        logging.info("File successfully opened")
    except FileNotFoundError as error:
        logging.critical("File not found: {}".format(error))

    return weather_dataframe
