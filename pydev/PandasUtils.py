# coding: utf-8
#!/usr/bin/env python

import pandas as pd
import json
from pandas.io.json import json_normalize
import unicodedata as ucd

class PandasUtils:

  @staticmethod
  def getWkbk(fn):
    wkbk = pd.ExcelFile(fn)
    return wkbk
  

  @staticmethod
  def groupbyCountStar(df, group_by_list):
    return df.groupby(group_by_list).size().reset_index(name='count')


  @staticmethod
  def removeCols(df, list_of_cols_to_remove):
    '''removes cols inplace'''
    df_col = list(df.columns)
    #check to make sure that column exists in the dataframe
    list_of_cols_to_remove = [col for col in list_of_cols_to_remove if col in df_col]
    return df.drop(list_of_cols_to_remove, axis=1)
    #return df.drop(df[list_of_cols_to_remove],inplace=True,axis=1)


  @staticmethod
  def loadCsv(fullpath):
    df = None
    try:
      df = pd.read_csv(fullpath)
    except Exception, e:
      print str(e)
    return df

  @staticmethod
  def fillNaWithBlank(df):
    return df.fillna("")

  @staticmethod
  def makeDfFromJson(json_obj):
    df = json_normalize(json_obj)
    return df

  @staticmethod
  def convertDfToDictrows(df):
    return df.to_dict(orient='records')

  @staticmethod
  def mapFieldNames(df, field_mapping_dict):
    return df.rename(columns=field_mapping_dict)

  @staticmethod
  def renameCols(df, colMappingDict):
    df = df.rename(columns=colMappingDict)
    return df

  @staticmethod
  def groupbyCountStar(df, group_by_list):
    return df.groupby(group_by_list).size().reset_index(name='count')

  @staticmethod
  def colToLower(df, field_name):
    '''strips off white space and converts the col to lower'''
    df[field_name] = df[field_name].astype(str)
    df[field_name] = df[field_name].str.lower()
    df[field_name] = df[field_name].map(str.strip)
    return df

  @staticmethod
  def makeLookupDictOnTwo(df, key_col, val_col):
      return dict(zip(df[key_col], df[val_col]))


if __name__ == "__main__":
    main()
