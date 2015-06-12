# -*- coding: utf-8 -*-
import json
import time
from pseudo_pid_controller import PID
import gspread
from oauth2client.client import SignedJwtAssertionCredentials


#### INITIALIZE #####
# connect to google spreadsheet
json_key = json.load(open('SmokehouseController-5be721d918b4.json'))
scope = ['https://spreadsheets.google.com/feeds']

credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)

gc = gspread.authorize(credentials)

worksheet = gc.open_by_key("1pzZBRAO7qukY5rArVy-YA1tSJ8zQ9Ihckl7degFTNdM").sheet1

# configure copernicus board
serial = s.Serial('/dev/ttyS0', 38400, timeout=1)
serial.write(chr(128+4))    #automatic update: knob position (as temperature value)

# initialize PID 
p = PID(3.0, 0.4, 1.2)

min_row = 2


#### FUNCTIONS ####

def PIDsetPrefferedTemperature(temperature):
    print "Going to set temperature to " + temperature + "."
    p.setPoint(temperature)


def temperature(cc):  # interpretation of received byte
    if 128 > cc > 63:
        return 2 * (cc - 63)
    return -1

def PIDgetCalculatedValue(currentTemperature):
    p.update(currentTemperature)

#### MAIN ####

prefferedTemperature = 50  # readed from spreadsheet, used by PID
airInflowLevel = 0  # updated by PID, sended to Copernicus
lastPrefferedTempperatureValueColumn = 0  # last readed column to be updated if no connection to spreadsheet
lastPrefferedTempperatureTimeLeftColumn = 0  # -//-

currentTemperature = 20
currentTime = 0
currentTimeInMinutes = 0

try:
    currentTimeInMinutes = int(worksheet.cell(2, 9).value)
except:
    print "No connectionn to spreadsheet."

while True:
    # 1: read temperature
    cc = serial.read(1)
    temperature = temperature(cc);
    if temperature > 0:     # check, if readed byte is a new temperature value; if true, react
        currentTemperature = temperature

    # 2: update current time, current temperature (if anything changed)
    if currentTime == 0:
        worksheet.update_cell(2, 9, currentTimeInMinutes)  # (row, col, val, key)
    if currentTime % 10 == 0:
        worksheet.update_cell(2, 10, currentTemperature)  # (row, col, val, key)

    # 3: read columns: preferred temperatue, time left, find current pref. temper.
    if currentTime == 0:
        try:
            prefferedTemperatureValueColumn = worksheet.col_values(1)[min_row:]
            # print prefferedTemperatureValueColumn
            
            prefferedTemperatureTimeLeftColumn = worksheet.col_values(3)[min_row:]
            #print prefferedTemperatureTimeLeftColumn
            
        except:
            print "No connection to spreadsheet."
            # work on lastPrefferedTempperatureValueColumn and lastPrefferedTempperatureTimeLeftColumn
            # do the same as in case of connection to internet ()it should be separate function probably)

        # search current preferred temperature (first record in TimeLeft column, that is not zero) read value and write it to preferredTemperature
        index = 0
        for entry in prefferedTemperatureTimeLeftColumn: #.entry:
            if int(entry) != 0:
                break
            index += 1

        prefferedTemperature = prefferedTemperatureValueColumn[index]
        PIDsetPrefferedTemperature(prefferedTemperature)


    # 4: move valve (servo on Copernicus) to the prescaled value (from airFlowLevel variable)
    airFlowLevel = PIDgetCalculatedValue(int(currentTemperature))
    # print airFlowLevel
    serial.write(airFlowLevel * 31 / 100)

    # 5: sleep
    time.sleep(1)
    currentTime += 1
    if currentTime == 3:
        currentTime = 0
        currentTimeInMinutes += 1
