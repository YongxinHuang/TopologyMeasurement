#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'Download 24h measurements from RIPENCC'

__author__ = 'Yongxin Huang'

import os
import sys
import time
import json
import urllib.request

url = 'https://atlas.ripe.net/api/v2/measurements/traceroute/?'

#Reads the parameters entered from the command line
def getTimeFromCommandLine():
    args = sys.argv
    if len(args)==1:
        print("Please enter a day in this time format:YYYYmmdd!")
    elif len(args)>3:
        print("Too many time arguments!")
    else:
        return args
    return -1

#Convert the entered time to the time stamp
def convertTimes(timeOfTheDay):
    timelist = []
    #format the time
    starttime = timeOfTheDay[0:4]+'-'+timeOfTheDay[4:6]+'-'+timeOfTheDay[6:8]+' 00:00:00'
    stoptime = timeOfTheDay[0:4]+'-'+timeOfTheDay[4:6]+'-'+timeOfTheDay[6:8]+' 23:59:59'
    #convert to an array of times
    start_time = time.strptime(starttime,"%Y-%m-%d %H:%M:%S")   
    stop_time = time.strptime(stoptime,"%Y-%m-%d %H:%M:%S")
    #convert to a time stamp
    timelist.append(time.mktime(start_time))
    timelist.append(time.mktime(stop_time))
    return timelist


#Fetching time period items data in the url from user wanted
#And generate a document input to the disk
def getHtml(req):
    with urllib.request.urlopen(req) as f:
        ##Read data
        data_bytes = f.read()
        data_str = data_bytes.decode('utf-8')
        data_dict = json.loads(data_str)
        return data_dict

def getMeasurementsItems(url,start_time,stop_time,fileName):
    url = url + 'start_time__lt='+stop_time +'&'+'stop_time__gt='+start_time+'&af=4'
    req = urllib.request.Request(url)
    ##Analyze the pages' data and save to the list
    id_list = []
    start_time_list = []
    stop_time_list = []
    result_list = []
    while True:
        #Fetching the data from requrl
        data_dict = getHtml(req)
        results_list = data_dict["results"]
        #Determine whether the data is returned
        if data_dict["count"] == 0 or data_dict["count"] == None:
            break
        for x in range(len(results_list)):
            id_list.append(results_list[x]["id"])
            start_time_list.append(results_list[x]["start_time"])
            stop_time_list.append(results_list[x]["stop_time"])
            result_list.append(results_list[x]["result"])
        if data_dict["next"] == None:
            break
        req = data_dict["next"] 
    #Write to the docunment
    pathOfTheFile = "/ldc/mdata/atlas/memlist."+str(timeOfFile)    
    dataLine = open(pathOfTheFile,"w")
    for x in range(len(id_list)):
        dataLine.write(str(id_list[x])+' '+str(start_time_list[x])+' '+str(stop_time_list[x])+' '+result_list[x]+'\n')
        #dataLine.write(result_list[x]+'\n')
    dataLine.close()




timeOfTheDay = getTimeFromCommandLine()
day_start = convertTimes(timeOfTheDay[1])
day_stop  = convertTimes(timeOfTheDay[2]) 
daysOfM = int((int(day_stop[1])-int(day_start[0])+1)/(24*3600))
for x in range(daysOfM):
    start_time = str(int(day_start[0]+((24*3600)*x)))
    stop_time = str(int(day_start[0]+((24*3600)*(x+1))))
    Itime = time.localtime((day_start[0]+((24*3600)*x)))
    timeOfFile = time.strftime("%Y%m%d",Itime)
    getMeasurementsItems(url,start_time,stop_time,timeOfFile)
