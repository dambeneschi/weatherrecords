#! /usr/bin/env python3
#coding: utf-8

""" ========================================
Convert a txt file generated from darksky API data
into a csv file
==========================================="""


import ast


def txt_to_csv (texte):
    """Convert a txt file with weather data into a csv file"""
    dataset=[]
    dico0={}
    
    file = open(texte, "r", encoding="utf-8")
    
    #Convert data into list
    data = str(file.read())
    data = data[1:]
    data = data [:len(data)-1]
    data = data.split(", {")

    #First list argument has a "{", not the following ones
    dico0 = ast.literal_eval(data[0])
    dataset.append(dico0)

    #Addind { to following ones
    for d in data[1:]:
        #format as a dictionnary
        dico = "{" + d
        dico = ast.literal_eval(dico)
    
        dataset.append(dico)
    print(dataset)
    print(type(dataset), len(dataset), type(dataset[2]))

    #Return the unique weather parameters of the records
    list_parameters=[]
    unique_values=[]
    
    #for each hourly record:
    for record in dataset:
        #for each values recorded
        for key,value in record.items():
            list_parameters.append(key)
        
    #List of weather parameters
    parameters = list(set(list_parameters))
    
    #Create CSV file
    organize(dataset, parameters)    
        
    return('Done')
