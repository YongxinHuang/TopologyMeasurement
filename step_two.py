#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'Download 24h measurements from RIPENCC'

__author__ = 'Yongxin Huang'

import os
import sys
import time
import json
import urllib.request
import requests
from ripe.atlas.sagan import Result
from ripe.atlas.sagan import SslResult
from ripe.atlas.sagan import TracerouteResult

#Reads the parameters entered from the command line
def getTimeFromCommandLine():
    args = sys.argv
    if len(args)==1:
        print("Please enter a day in this time format:YYYYmmdd!")
    elif len(args)>3:
        print("Too many time arguments!")
    else:
        print("The script is downloading %s's measurements..."%args[1])
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
        
        data_bytes = f.read()
        data_str = data_bytes.decode('utf-8')
        return data_str

#Fetching time period Measurements data in the urls from results doc in the disk


def fetchResult(result_list,start_time,stop_time,timeOfFile):
   
    pathOfTheFile ="/ldc/mdata/atlas/rawdata."+str(timeOfFile)
    dataLine = open(pathOfTheFile,"a+")
    source = result_list+'?start='+start_time+'&stop='+stop_time
    response = getHtml(source)
    dataLine.write(response+'\n')
    dataLine.close()



################**********************test*******************************************#################
#fetchResult(start_time,stop_time,timeOfTheDay)
timeOfTheDay = getTimeFromCommandLine()
day_start = convertTimes(timeOfTheDay[1])
day_stop  = convertTimes(timeOfTheDay[2])
daysOfM = int((int(day_stop[1])-int(day_start[0])+1)/(24*3600))
for x in range(daysOfM):
    start_time = str(int(day_start[0]+((24*3600)*x)))
    stop_time = str(int(day_start[0]+((24*3600)*(x+1))))
    Itime = time.localtime((day_start[0]+((24*3600)*x)))
    timeOfFile = str(int(time.strftime("%Y%m%d",Itime)))
   
    pathf = '/ldc/mdata/atlas/memlist.'+timeOfFile
    with open(pathf,'r+') as rs:
        for result_0 in rs:
            result_1 =result_0.split()
            result =result_1[-1]
            fetchResult(result,start_time,stop_time,timeOfFile)              
    
