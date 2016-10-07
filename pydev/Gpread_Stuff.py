# coding: utf-8


import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import pickle
import re

class gSpread_Stuff:
    ''' class to deal with google spreadsheet stuff '''
    def __init__(self,   configItems):
        self.client_key = configItems["client_key"]
        self.gscope = ['https://spreadsheets.google.com/feeds']
        self.gc = self.get_goog_client()
        self.picked_dir = configItems["pickle_dir"]

    def get_goog_client(self):
        credentials = ServiceAccountCredentials.from_json_keyfile_name(self.client_key, self.gscope)
        gc = gspread.authorize(credentials)
        return gc

    def get_wkbk(self, wkbook_key):
        wkbk = self.gc.open_by_key(wkbook_key)
        return wkbk
    
    @staticmethod
    def get_all_shts(wkbk):
        return wkbk.worksheets()
        
    @staticmethod
    def get_sht(wkbk, sht_name):
        return wkbk.worksheet(sht_name)
    
    @staticmethod
    def get_all_cells(sht):
        return sht.get_all_records()
    
    @staticmethod
    def findCells(sht, regex_str):
        # Find all cells with regexp
        cell_list = sht.findall(regex_str)
        return cell_list
        
    @staticmethod    
    def findRows(sht, regex_str):
        '''returns a list a row numbers that match a regex'''
        cell_list = sht.findall(regex_str)
        rows = [ cell.row for cell in cell_list ]
        return rows
        
    @staticmethod
    def findCellList(sht, regex_str):
         return sht.findall(regex_str)
    
    @staticmethod
    def batchUpdateCellRange(sht, cell_range, valToSet):
        updt_success = False
        # Select a range
        cell_list = sht.range(cell_range)
        #set the cell value
        for cell in cell_list:
            cell.value = valToSet
        # Update in batch
        try:
            sht.update_cells(cell_list)
            updt_success = True
        except:
            print "ERORR: Could not update cells"
        return cell_range, updt_success
    
    def batchUpdateCellRanges( self, sht, cell_ranges, valToSet):
        updt_log = {}
        for cell_range in cell_ranges:
            cell_range, updt_success  =  self.batchUpdateCellRange(sht, cell_range, valToSet) 
            updt_log[cell_range] = updt_success
        return updt_log
        
    @staticmethod   
    def getCellRange(column,rows):
        rows =  sorted(rows)
        cell_range = ""
        cell_range = column + str( rows[0] ) + ":" + column + str(rows[-1])
        return cell_range
    
    def getCellRows(self, sht, listOfDataToFind):
        all_rows = []
        for dataToFind in listOfDataToFind:
            rows = self.findRows(sht, dataToFind)
            all_rows.append(rows)
        return all_rows
    
    def getCellRanges(self, allRows, column):
        cell_ranges = []
        for rows in allRows:
            if len(rows) > 1:
                cell_range = self.getCellRange(column, rows )
                cell_ranges.append(cell_range)
        return cell_ranges
    
    
    def pickle_cells(self, cells, pickle_name ):
        pickle.dump( cells, open( self.picked_dir + pickle_name + "_pickled_cells.p", "wb" ) )
    
    def unpickle_cells(self, pickle_name):
        return pickle.load( open( self.picked_dir + pickle_name +"_pickled_cells.p", "rb" ) )

    def getMetaDataset(self, wkbk_key, sht_name, pickle_name):
        wkbk = self.get_wkbk(wkbk_key)
        sht = self.get_sht(wkbk, sht_name)
        cells = self.get_all_cells(sht)
        self.pickle_cells(cells, pickle_name)
    

        #https://github.com/burnash/gspread
if __name__ == "__main__":
    main()
