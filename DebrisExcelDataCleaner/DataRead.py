from posixpath import split
import pandas
from pathlib import Path
import os
import re
import cellformatter
import findothercell

class DATAREAD:
    def __init__(self):
    #self.path = Path.cwd() / '2020.11.27KaehuCleanupData.xlsx'
        self.script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        rel_path = "2020.11.27KaehuCleanupData.xlsx"        # this is the name of your file. make sure it's in the same folder as the .py script.
        self.abs_file_path = os.path.join(self.script_dir, rel_path)

    def readin(self):       # read in bad file, clean up, then spit out formatted excel.
        df_raw = pandas.read_excel(self.abs_file_path,sheet_name=98, usecols='A:F') #skiprows=1
        data = []

        col1 = df_raw.iloc[:,0]

        location = col1[0].split(" ")[1]
        weatherlist = findothercell.FINDOTHERCELL.findWeatherList(self, df_raw)
        date = df_raw.iloc[:,3][0]

        for column in range(0,4):
            for row in df_raw.index:
                if row != 0 and row != 1:
                    cell = cellformatter.CELLFORMATTER(df_raw.iloc[:,column][row])
                    cellData = cell.camelCaseValidator(cell.inputCell)
                    
                    #print(cellData)
                    if cellData == -1:
                        pass
                    elif len(cellData) == 1:
                        item = cellData
                        data.append([location, weatherlist, date, item, self.numInThirdCell(df_raw, column, row), f"column:{column} row:{row}"])
                    elif len(cellData) == 2:
                        item = cellData[0]
                        itemQuantity = int(cellData[1])
                        data.append([location, weatherlist, date, item, itemQuantity, f"column:{column} row:{row}"])
                    else:
                        if len(cellData) % 2 == 1:
                            cellData.pop()
                        for i in range(0, len(cellData), 2):
                            data.append([location, weatherlist, date, cellData[i], int(cellData[i+1]), f"column:{column} row:{row}"])
        #print(data)
        return data

    def exportDFtoExcel(self, listOfListsData, i):
        df_cleaned = pandas.DataFrame(self.clearListsInLoL(listOfListsData))
        df_cleaned.to_excel(os.path.join(self.script_dir,f"cleanedoutput{i}.xlsx"))

    def clearListsInLoL(self, inputList):   # findWeatherList gives a list. we want to clear subsublists
        for subList in inputList:
            for i, element in enumerate(subList):
                if type(element) == list:
                    for x in element:
                        subList.insert(i, x)
                    subList.pop(i+len(element))
                    i += len(element)
        return inputList

    def numInThirdCell(self, inputDF, columnIndex, rowIndex):
        return inputDF.iloc[:,columnIndex+2][rowIndex]

newSheet = DATAREAD()
data = newSheet.readin()
newSheet.exportDFtoExcel(data, 2)