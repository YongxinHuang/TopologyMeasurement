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


#Fetchinc time period items data in the url from user wanted
#And generate a document input to the disk


#Fetching time period Measurements data in the urls from results doc in the disk

def fetchResult(response,start_time,stop_time,fileName):
   
    pathOfTheFile ="/ldc/mdata/atlas/atlas."+str(fileName)
    dataLine = open(pathOfTheFile,"a")
    if len(response) != 0:
        for y in range(len(response)):
            res_ponse = response[y]
            mr = TracerouteResult(res_ponse)   
            source_address = mr.source_address
            destination_address = mr.destination_address
            res = mr.ip_path
            if destination_address ==None or source_address ==None:
                continue    
            ip_path = destination_address+' '+source_address
            for z in range(len(res)):
                
                if len(res[z]) <1:
                    continue
                elif len(res[z])==1:
                    if res[z][0] == None:
                        ip_path = ip_path+' '+'q'
                    else:
                        ip_path = ip_path +' '+res[z][0]
                elif len(res[z]) ==2:
                    if res[z][0]== res[z][1] ==None:
                        ip_path = ip_path+' '+'q'
                    elif res[z][0] == res[z][1] :
                        ip_path = ip_path +' '+res[z][1]
                    elif res[z][0] ==None:
                        ip_path = ip_path + ' '+res[z][1]
                    else:
                        ip_path = ip_path +' '+res[z][0]
                elif res[z][0] == res[z][1] == res[z][2] and res[z][0] != None:
                    ip_path = ip_path+' '+res[z][0]
                elif res[z][0] == res[z][1] == res[z][2] == None:
                    ip_path = ip_path+' '+'q'
                else:
                    list_of_badhop_ip =[]
                    for badhop in range(len(res[z])):
                        if res[z][badhop] == None:
                            continue
                        list_of_badhop_ip.append(res[z][badhop])
                    if len(list_of_badhop_ip)==1:
                        ip_path = ip_path+' '+list_of_badhop_ip[0]
                    elif len(list_of_badhop_ip)==2:
                        if list_of_badhop_ip[0]==list_of_badhop_ip[1]:
                            ip_path =ip_path+' '+list_of_badhop_ip[0]
                        else:
                            ip_path = ip_path+' '+list_of_badhop_ip[0]+','+list_of_badhop_ip[1]
                    else:
                        if  list_of_badhop_ip[0]!=list_of_badhop_ip[1] and list_of_badhop_ip[1] != list_of_badhop_ip[2] and list_of_badhop_ip[0] != list_of_badhop_ip[2]:
                            ip_path= ip_path+' '+list_of_badhop_ip[0]+','+list_of_badhop_ip[1]+','+list_of_badhop_ip[2]
                        elif list_of_badhop_ip[0] == list_of_badhop_ip[1]:
                            ip_path = ip_path+' '+list_of_badhop_ip[0]+','+list_of_badhop_ip[2]
                        elif list_of_badhop_ip[0]==list_of_badhop_ip[2]:
                            ip_path = ip_path+' '+list_of_badhop_ip[0]+','+list_of_badhop_ip[1]
                        elif list_of_badhop_ip[1] == list_of_badhop_ip[2]:
                            ip_path = ip_path+' '+list_of_badhop_ip[0]+','+list_of_badhop_ip[1]
            dataLine.writelines(ip_path+"\n")
    dataLine.close()

        


################**********************test*******************************************#################


args = sys.argv
for items in range(len(args)-1):
    x = args[items+1]
    dataOfFile_l = x.split('.')
    dataOfFile = dataOfFile_l[1]
    with open('/ldc/mdata/atlas/rawdata.'+str(dataOfFile),'r') as rs:
        for data_str in rs:
            #data_str = next(dataLines)
            #data_str = data_bytes.decode('utf-8')
            if len(data_str)<4:
               continue
            try:
                data_list = json.loads(data_str)
            
                #js = json.dumps(data_bytes)
                #md_str = json.loads(js).encode('utf-8')
                #md = json.loads(md_str)
                #mr = TracerouteResult(md[0])
                #print mr.ip_path

                sstList = convertTimes(dataOfFile)
                start_time = str(int(sstList[0]))
                stop_time  = str(int(sstList[1]))
                fetchResult(data_list,start_time,stop_time,dataOfFile)
            except json.decoder.JSONDecodeError:
                print("json.decoder.JSONDecodeError!")
                continue
        #except StopIteration:
            #dataLines.close()
            #continue
