# -*- coding: utf-8 -*-

import time
import gdata.spreadsheet.service
from random import randint

#### INITIALIZE #####
# connect to google spreadsheet
email = 'Zachariasz19800@gmail.com'
password = '1980Zachariasza'
spr_client = gdata.spreadsheet.service.SpreadsheetsService()
spr_client.email = email
spr_client.password = password
spr_client.source = 'Smokehouse controller project'
spr_client.ProgrammaticLogin()

key = '1pzZBRAO7qukY5rArVy-YA1tSJ8zQ9Ihckl7degFTNdM'
worksheets_feed = spr_client.GetWorksheetsFeed(key)  

# configure copernicus board
# serial = s.Serial('/dev/ttyS0', 38400, timeout=1)
# serial.write(chr(128+4))    #automatic update: knob position (as temperature value)

#Reading cells from the first sheet:
query_prefferedTemperatureValueColumn = gdata.spreadsheet.service.CellQuery()
query_prefferedTemperatureValueColumn.min_row = '3'
query_prefferedTemperatureValueColumn.max_row = '14'
query_prefferedTemperatureValueColumn.min_col = '1'
query_prefferedTemperatureValueColumn.max_col = '1'

query_prefferedTempperatureTimeLeftColumn = gdata.spreadsheet.service.CellQuery()
query_prefferedTempperatureTimeLeftColumn.min_row = '3'
query_prefferedTempperatureTimeLeftColumn.max_row = '14'
query_prefferedTempperatureTimeLeftColumn.min_col = '3'
query_prefferedTempperatureTimeLeftColumn.max_col = '3'

#### FUNCTIONS ####



#### MAIN ####

# niech będą na razie globalne jakieś :)
prefferedTemperature = 0       # readed from spreadsheet, used by PID
airInflowLevel = 0              # updated by PID, sended to Copernicus
lastPrefferedTempperatureValueColumn = 0       # last readed column to be updated if no connection to spreadsheet
lastPrefferedTempperatureTimeLeftColumn = 0    # -//-

currentTemperature = 20
currentTime = 0

# INITIALIZE PID HERE - probably sepparate thread 

def temperature(cc):
    if 128 > cc > 63:
        return cc-63

def PIDonTemperatureChanged(temperature):
    print "to na razie mock, ja to robię, ewentualnie dostosuję jakoś " + temperature
        

while True:
    # 1 read temperature
    # cc = serial.read(1)
    # if temperature(cc) != currentTemperature:     # check, if readed byte is a new temperature value; if true, react
    #     currentTemperature = temperature(cc)




    # 2 update current time, current temperature (if anything changed)
    spr_client.UpdateCell(2, 9, currentTime, key)              # (row, col, val, key)
    spr_client.UpdateCell(2, 10, currentTemperature, key)      # (row, col, val, key)
    
    # 3 read columns: preferred temperatue, time left, find current pref. temper.
    try:
        prefferedTemperatureValueColumn = spr_client.GetCellsFeed(key, query=query_prefferedTemperatureValueColumn)
        prefferedTemperatureTimeLeftColumn = spr_client.GetCellsFeed(key, query=query_prefferedTempperatureTimeLeftColumn)
        
        # it should be separate function probably:




            # search current preferred temperature (first record in TimeLeft column, that is not zero) read value and write it to preferredTemperature 
            
    except:
        print "no connection to spreadsheet"
        # work on lastPrefferedTempperatureValueColumn and lastPrefferedTempperatureTimeLeftColumn
        # do the same as in case of connection to internet ()it should be separate function probably)

    index = int(query_prefferedTemperatureValueColumn.min_row)
    print index
    for entry in prefferedTemperatureTimeLeftColumn.entry:
        if entry != 0:
            break
        index += 1

    prefferedTemperature = prefferedTemperatureValueColumn[index]
    if prefferedTemperature != currentTemperature: # abs() <
        PIDonTemperatureChanged(prefferedTemperature)


    # 4 move valve (servo on Copernicus) to the prescaled value (from airFlowLevel variable)
    # serial.write(milijonpińcetjednostekobjetości)
    time.sleep(1)
    currentTime += 1

    

