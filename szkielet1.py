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
serial = s.Serial('/dev/ttyS0', 38400, timeout=1)
serial.write(chr(128+4))    #automatic update: knob position (as temperature value)

#Reading cells from the first sheet:
query_prefferedTempperatureValueColumn = gdata.spreadsheet.service.CellQuery()
query_prefferedTempperatureValueColumn.min_row = '3'
query_prefferedTempperatureValueColumn.max_row = '14'
query_prefferedTempperatureValueColumn.min_col = '1'
query_prefferedTempperatureValueColumn.max_col = '1'

query_prefferedTempperatureTimeLeftColumn = gdata.spreadsheet.service.CellQuery()
query_prefferedTempperatureTimeLeftColumn.min_row = '3'
query_prefferedTempperatureTimeLeftColumn.max_row = '14'
query_prefferedTempperatureTimeLeftColumn.min_col = '3'
query_prefferedTempperatureTimeLeftColumn.max_col = '3'

#### FUNCTIONS ####



#### MAIN ####

# niech będą na razie globalne jakieś :)
var prefferedTemperature        # readed from spreadsheet, used by PID
var airInflowLevel              # updated by PID, sended to Copernicus
var lastPrefferedTempperatureValueColumn        # last readed column to be updated if no connection to spreadsheet
var lastPrefferedTempperatureTimeLeftColumn     # -//-

# INITIALIZE PID HERE - probably sepparate thread 

function temperature(cc):
    if 128 > cc > 63:
        

function PIDonTemperatureChanged(int temperature):
    print "to na razie mock, ja to robię, ewentualnie dostosuję jakoś"
        

while True:
    # 1 read temperature
    cc = serial.read(1)
    temperature(cc)     # check, if readed byte is a new temperature value; if true, react
    
    
    # 2 update current time, current temperature (if anything changed)
    spr_client.UpdateCell(2,9,currentTime,key)              # (row, col, val, key)
    spr_client.UpdateCell(2,10,currentTemperature,key)      # (row, col, val, key)
    
    # 3 read columns: preferred temperatue, time left, find current pref. temper.
    try:
        prefferedTempperatureValueColumn = spr_client.GetCellsFeed(key, query=query_prefferedTempperatureValueColumn)
        prefferedTempperatureTimeLeftColumn = spr_client.GetCellsFeed(key, query=query_prefferedTempperatureTimeLeftColumn)
        
        # it should be separate function probably:
        for entry in prefferedTempperatureTimeLeftColumn.entry:
            # search current preferred temperature (first record in TimeLeft column, that is not zero) read value and write it to preferredTemperature 
            
    except:
        print "no connection to spreadsheet"
        # work on lastPrefferedTempperatureValueColumn and lastPrefferedTempperatureTimeLeftColumn
        # do the same as in case of connection to internet ()it should be separate function probably)
    


    

