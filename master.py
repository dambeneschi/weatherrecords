#! /usr/bin/env python3
#coding: utf-8

"""
===========================
Launch graphics generation of weather data from either
data recovered directly from DarkSky API
or from a CSV file
through command invite
===================================================================== """

import argparse
import urllib
import logging
import matplotlib.pyplot as plt

import analysis.get_records as get_records
import analysis.csv_to_dataframe as csv_to_dataframe
import analysis.visualization as viz

#Display INFO messages
logging.basicConfig(level=logging.INFO)

def parse_arguments():
    """Get from command invite the arguments to get data from API or frm CSV file"""
    
    #Request for arguments of the function in command line
    parser = argparse.ArgumentParser(description='Analysise Weather data from either .csv file or Darksky API')
    #Add the type of source as an arugment
    parser.add_argument("-s", "--source",
                        help="""Source of the data to analyse: csv or API ?""")
    parser.add_argument("-f", "--file",
                        help="""Name of the CSV file to open from the folder /csv""")
    parser.add_argument("-b", "--begining_date", type=str,
                        help="""Begining date for data recovery on API in format 'DD/MM/YY'""")
    parser.add_argument("-e", "--ending_date", type=str,
                        help="""Ending date for data recovery on API in format 'DD/MM/YY'""")
    parser.add_argument("-l1", "--location1",
                        help="""location for the weather data from API, formatted XX.XXXX""")
    parser.add_argument("-l2", "--location2",
                        help="""location for the weather data from API, formatted XX.XXXX""")
    parser.add_argument("-p", "--parameter", type=str,
                        help="""Enter the weather parameter you want to be displayed on a chart among
                        [precipIntensity, dewPoint, humidity, pressure, windbear, windSpeed,
                        cloudCover, apparentTemperature, visibility, temperature] """)
    parser.add_argument("-c", "--constant", type=float,
                        help="""Enter Constant value of the parameter to display pie chart
                        of the percentage under/above this value""")
    #Add margin argument, set at 0 as default value
    parser.add_argument("-m", "--margin", type=float, default=0,
                        help="""Margin to apply to the values of the parameter""")
    return parser.parse_args()


def main():
    ARGS = parse_arguments()
    SOURCE = ARGS.source
    #If no source entered in command
    if SOURCE is None:
        logging.critical("You must indicate a data source !")
    #Open csv file
    elif SOURCE == 'csv':
        try:
            FILE = ARGS.file
            weather_dataframe = csv_to_dataframe.ctd(FILE)
            logging.info('###########  DATA RECOVERED SUCCESFULLY  ##########')
        except FileNotFoundError:
            logging.critical('csv file in /csv to be specified')
    #Get data from API
    elif SOURCE == 'API':
        BEGINING = ARGS.begining_date
        ENDING = ARGS.ending_date
        LOC1 = ARGS.location1
        LOC2 = ARGS.location2
        logging.info('recovering data from Darksky weather API')
        if LOC1 is not None and LOC2 is not None:
            file_name = get_records.get(BEGINING,ENDING, LOC1, LOC2)
            logging.info('###########  DATA RECOVERED SUCCESFULLY  ##########')
        else:
            file_name = get_records.get(BEGINING,ENDING)
            logging.info('###########  DATA RECOVERED SUCCESFULLY  ##########')
        weather_dataframe = csv_to_dataframe.ctd(file_name)
    else:
        #Wrong type of source entered
        logging.critical("Wrong argument for source argument -> Must be 'API' or 'csv'")

    #Display charts using 'visualization' class methods
    PARAMETER=ARGS.parameter
    w = viz.Visualization('Weather data')
    w.data_from_dataframe(weather_dataframe)
    try:
        if PARAMETER is not None:
            w.stats(PARAMETER)
            w.display_hist(PARAMETER)
            plt.show()
            plt.clf()
            w.display_monotone(PARAMETER)
            CONSTANT=ARGS.constant
            if CONSTANT is not None:
                MARGIN=ARGS.margin
                w.margin(PARAMETER, MARGIN)
                w.display_pie(PARAMETER, CONSTANT)
        plt.show()
        logging.info('##############  CHARTS DISPLAYED  ############')
    except KeyError:
        logging.critical('Wrong argument for charts displaying. Must be a right parameter at least')
    logging.info('##########   END OF THE SCRIPT   ##############')


if __name__ == '__main__':
    main()
