# -*- coding: utf-8 -*-

import time
import gdata.spreadsheet.service
from random import randint

# connect to google spreadsheet
email = 'Zachariasz19800@gmail.com'
password = '1980Zachariasza'
spr_client = gdata.spreadsheet.service.SpreadsheetsService()
spr_client.email = email
spr_client.password = password
spr_client.source = 'Smokehouse controller project'
spr_client.ProgrammaticLogin()

key = ''
worksheets_feed = spr_client.GetWorksheetsFeed(key)  

# configure copernicus board
serial = s.Serial('/dev/ttyS0', 38400, timeout=1)
serial.write(chr(128+4))    #automatic update: knob position


#Reading cells from the first sheet
query = gdata.spreadsheet.service.CellQuery()
query.max_row = '3'
query.min_row = '3'
query.min_col = '5'
query.max_col = '5'

function temperature(cc):
    if 128 > cc > 63:
        



while True:
    # 1 
    cc = serial.read(1)
    temperature(cc)
    
    # 2
    try:
        cells = spr_client.GetCellsFeed(key, query=query)
        for entry in cells.entry:
            print entry.content.text
    except:
        print "no connection to spreadsheet"
    
