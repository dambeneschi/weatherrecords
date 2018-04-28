#! /usr/bin/env python3
#coding: utf-8

""" =====================================================
Generates charts from dataframe according to parameter
========================================================="""

import logging
import os
import datetime
import matplotlib.pyplot as plt
import numpy
import pandas
import seaborn; seaborn.set() #Improve graphics aesthetics


class Visualization:
    def __init__(self, name):
        """Init"""
        self.name = name

    def data_from_dataframe(self, dataframe):
        """Add dataframe and check for duplicate rows"""
        self.dataframe = dataframe.drop_duplicates()
        #Convert numerical values into float type
        self.dataframe.apply(pandas.to_numeric, errors='ignore')
        #Convert timestamps into regular dates
        time_range = [datetime.datetime.fromtimestamp(time) for time in list(self.dataframe['time'])]
        beg = time_range[0]
        end = time_range[len(time_range)-1]
        #Attribute begining and ending dates
        self.beg = beg
        self.end = end

    def values(self, parameter):
        """Print all values from dataframe for given parameter"""
        self.values = self.dataframe[parameter]
        print(self.values)

    def display_plot(self, parameter):
        """Display plot from dataframe parameter values"""
        values = list(self.dataframe[parameter])
        #Begining and ending date of the dataset
        beg = self.beg
        end = self.end
        #Settings of the plot
        if parameter == 'temperature':
            #Differienciate the color of the points according to temeprature rule
            import matplotlib as mpl
            cmap = mpl.colors.ListedColormap(['blue', 'yellow', 'orange', 'red'])
            c_norm = mpl.colors.BoundaryNorm(boundaries=[-30,0,15,25,45], ncolors=4)
            plt.scatter(time_range, values, s=0.3, c=values, cmap=cmap, norm=c_norm)
            plt.colorbar()
        else:
            plt.plot(time_range, values, linewidth=0.2)
        plt.xlabel('from {} to {}'.format(beg, end))
        plt.ylabel(parameter)
        plt.title('Weather historical data')
        plt.grid(True)

    def display_hist(self, parameter):
        """Display histogram chart from dataframe parameter values"""
        values = self.dataframe[parameter]
        #Begining and ending date of the dataset
        beg = self.beg
        end = self.end
        #Settings of the hist chart with different bins according to parameter
        maxi = values.max()
        mini = values.min()
        #Weather parameter is either a value between 0-1 or a physical parameter >1
        if maxi > 1:  #ie if we are with a parameter with values not in [0,1]
            #bins = the number of integer between max and min value of the parameter
            bins = int(maxi - mini)
            plt.hist(values, bins=bins, range=(int(mini), int(maxi)))
        else:  #Else, for parameters with value between [0,1]
            bins = 2*int(10*(maxi - mini))
            plt.hist(values, bins=bins, range=(mini, maxi))
        plt.ylabel(parameter)
        plt.title('Weather historical data from {} to {}'.format(beg, end))

    def display_pie(self, parameter, constant):
        """Display pie chart of percentages of values for given parameter
        above/below given constant"""
        #Calculate percentage above & below constant
        masque = self.dataframe[parameter] >= constant
        above = self.dataframe[masque]
        below = self.dataframe[~masque]
        percent_above = round(len(above)/len(self.dataframe), 3)
        percent_below = round(len(below)/len(self.dataframe), 3)
        #Begining and ending date of the dataset
        beg = self.beg
        end = self.end
        #Create Pie plot
        fig, ax = plt.subplots()
        labels = ['% of {} above {}'.format(parameter, constant),
                  '% of {} below {}'.format(parameter, constant)]
        ax.pie([percent_above, percent_below], labels=labels,
               autopct='%1.1f percents')
        ax.axis('equal')
        plt.title('Weather historical data from {} to {}'.format(beg, end))

    def display_monotone(self, parameter):  #Monotone is x:cumulated occurencies y:value
        values = numpy.array(self.dataframe[parameter])
        if max(values) > 1:  #parameters with values not [0,1]
            values = values.round() #round values
        else:  #for parameters with values [0,1]
            values = numpy.around(values, decimals=2)
            values = numpy.array(values)

        values = numpy.sort(values)  #ascendingly sorted
        #Unique_values is a tuple! containing 2 arrays with the unique values and their occurencies
        #that has to be turned again into array to be changed
        unique_values = numpy.array(numpy.unique(values, return_counts=True))
        unique_values = numpy.fliplr(unique_values)
        #Array of cumulated occurencies in int format from already rounded values
        cumul_occ = [int(unique_values[1][0])]
        for  i in range(1, len(unique_values[1])):
            cumul_occ.append(int(unique_values[1][i] + cumul_occ[i-1]))
        cumul_occ = numpy.array(cumul_occ)
        
        #Begining and ending date of the dataset
        beg = self.beg.strftime("%d-%m-%y")  #only d/m/y
        end = self.end.strftime("%d-%m-%y")
        #Display chart
        plt.plot(cumul_occ, unique_values[0])
        plt.title('Monotone between {} and {}'.format(beg, end))
        plt.ylabel(parameter)
        plt.xlabel('cumulated hours')

        #Write monotone data into csv file
        dirname = os.path.dirname(os.path.dirname(__file__))
        path = os.path.join(dirname,
                            'csv', 'monotone_{}_{}_{}.csv'.format(parameter, beg, end))
        #Build the dataframe and write it
        spreadsheet = pandas.DataFrame()
        spreadsheet[parameter] = unique_values[0]
        spreadsheet['occurencies'] = unique_values[1]
        spreadsheet['cumul'] = cumul_occ
        spreadsheet.to_csv(path, sep=",", encoding='utf-8')
        logging.info('############### Monotone csv file created ############')

    def stats(self, parameter):
        #Return mean, median, standard deviation
        beg = self.beg
        end = self.end
        values = self.dataframe[parameter]
        average = float(round(numpy.mean(values), 2))
        median = float(round(numpy.median(values), 2))
        std_der = float(round(numpy.std(values), 2))
        return('[arithmetical average, median, standard derivation] for {} between {} and {}'.format(parameter, beg, end),
               [average, median, std_der])

    def margin(self, parameter, margin):
        """Add temporarly a margin to the parameter values"""
        #Use array type to multipy values by margin
        array = numpy.array(self.dataframe[parameter])
        array = array * (1+margin)
        self.dataframe[parameter] = array
        logging.info('Margin of {} successfully applied to the parameter values'.format(margin))


#TESTING on PYTHON SHELL
import os; directory = os.path.dirname(os.path.dirname(__file__))
path = os.path.join(directory, 'csv', 'data_records_01-01-13_31-12-13.csv')
weather_dataframe = pandas.read_csv(path, ",")
w = Visualization('weather')
w.data_from_dataframe(weather_dataframe)
