from posixpath import split
import pandas
from pathlib import Path
import os
import re

class DataReader:
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
        weatherlist = self.findWeatherList(df_raw)
        date = df_raw.iloc[:,3][0]

        for ind in df_raw.index:
            if ind != 0 and ind != 1:       # because of the inconsistent way in which types serve as headers over items, it's difficult to avoid this messy regex cell by cell IF hell.
                #column 1
                if re.match(r'^FOAM fragments:', col1[ind]):
                    item = "Foam Fragment"
                    
                    data.append(self.numInSameCell(df_raw, ind, location, date, weatherlist, item, 0))
                    """data.append([location,
                    weatherlist, 
                    df_raw["Unnamed: 3"][0], 
                    self.category(item), "N/A", item, 
                    int(re.findall(r'\d+', df_raw["SHARKastics Marine Debris"][ind])[0])])"""

                elif re.match(r'^Plastic fragments', col1[ind]):
                    if "hard" in col1[ind]:   
                        item = "Hard Plastic Fragment"

                        data.append(self.numInThirdCell(df_raw, ind, location, date, weatherlist, item))
                        """data.append([location,    # location
                        weatherlist,                       # weather, weather, tide
                        date,                                # date
                        self.category(item), "N/A", item,                         # type, subtype, item name
                        df_raw["Unnamed: 2"][ind]])  # number"""
                    else:
                        item = "Plastic Film"
                        data.append(self.numInThirdCell(df_raw, ind, location, date, weatherlist, item))
                
                elif re.match(r'^Food wrappers:', col1[ind]):
                    item = "Food Wrappers"
                    data.append(self.multiItemInSameCell(df_raw, ind, location, date, weatherlist, item, 0))
                    """data.append([location,    # location
                    weatherlist,                       # weather, weather, tide
                    date,                                # date
                    self.category(item), "N/A", item,                         # type, subtype, item name
                    int(re.findall(r'\d+', df_raw["SHARKastics Marine Debris"][ind])[0])])  # number

                    data.append([location,    # location
                    weatherlist,                       # weather, weather, tide
                    date,                                # date
                    self.category(item), "N/A", "Food Packaging",                         # type, subtype, item name
                    int(re.findall(r'\d+', df_raw["SHARKastics Marine Debris"][ind])[1])])  # number"""

                    item = "Food Packaging"
                    data.append(self.multiItemInSameCell(df_raw, ind, location, date, weatherlist, item, 1))

                elif re.match(r'^Beverage bottles', col1[ind]):
                    item = "Beverage Bottles"
                    data.append(self.numInThirdCell(df_raw, ind, location, date, weatherlist, item))

                elif re.match(r'^Cleaning bottles:', col1[ind]):  
                    item = "Cleaning Bottles"
                    data.append(self.numInSameCell(df_raw, ind, location, date, weatherlist, item, 0))

                elif re.match(r'^Fishing containers/packaging:', col1[ind]):  
                    item = "Fishing Containers/Packaging"
                    data.append(self.numInThirdCell(df_raw, ind, location, date, weatherlist, item))

                elif re.match(r'^Bottle or container caps/lids', col1[ind]):  
                    item = "Bottle/Container Caps, Lids"
                    data.append(self.numInThirdCell(df_raw, ind, location, date, weatherlist, item))
                
                elif re.match(r'^Cigarettes', col1[ind]):
                    item = "Cigarettes/Filters/Cigars"
                    data.append(self.numInSameCell(df_raw, ind, location, date, weatherlist, item, 0))
                
                elif re.match(r'^Cigarette lighters', col1[ind]):
                    item = "Cigarette Lighters"
                    data.append(self.numInThirdCell(df_raw, ind, location, date, weatherlist, item))
                
                elif re.match(r'^6 pack rings', col1[ind]):
                    item = "6 Pack Rings"
                    data.append(self.numInThirdCell(df_raw, ind, location, date, weatherlist, item))
                
                elif re.match(r'^Bags', col1[ind]):
                    item = "Bags"
                    data.append(self.numInThirdCell(df_raw, ind, location, date, weatherlist, item))

                elif re.match(r'^Plastic rope/small net pieces', col1[ind]):
                    item = "Plastic Rope/Small Net Pieces"
                    data.append(self.numInThirdCell(df_raw, ind, location, date, weatherlist, item))

                elif re.match(r'^Buoys and floats', col1[ind]):
                    item = "Buoys, Floats"
                    data.append(self.numInThirdCell(df_raw, ind, location, date, weatherlist, item))

                elif re.match(r'^Fishing lures', col1[ind]):
                    item = "Fishing Lures"
                    data.append(self.numInSameCell(df_raw, ind, location, date, weatherlist, item, 0))
                
                elif re.match(r'^Cup:', col1[ind]):
                    item = "Cups"
                    data.append(self.numInSameCell(df_raw, ind, location, date, weatherlist, item, 0))

                elif re.match(r'^Plastic utensils', col1[ind]):
                    item = "Plastic Utensils"
                    data.append(self.numInThirdCell(df_raw, ind, location, date, weatherlist, item))

                elif re.match(r'^Straws', col1[ind]):
                    item = "Straws"
                    data.append(self.numInThirdCell(df_raw, ind, location, date, weatherlist, item))

                elif re.match(r'^Balloons', col1[ind]):
                    item = "Balloons"
                    data.append(self.numInSameCell(df_raw, ind, location, date, weatherlist, item, 0))
                
                elif re.match(r'^Sanitary:', col1[ind]):
                    item = "Sanitary"
                    data.append(self.multiItemInSameCell(df_raw, ind, location, date, weatherlist, item, 0))

                    item = "Diapers"
                    data.append(self.multiItemInSameCell(df_raw, ind, location, date, weatherlist, item, 1))

                    item = "First Aid"
                    data.append(self.multiItemInSameCell(df_raw, ind, location, date, weatherlist, item, 3))

                    item = "Personal Care"
                    data.append(self.multiItemInSameCell(df_raw, ind, location, date, weatherlist, item, 4))
                
                elif "Toothbrush" in col1[ind]:
                    item = "Toothbrushes"
                    data.append(self.numInThirdCell(df_raw, ind, location, date, weatherlist, item))

                elif "Combs" in col1[ind]:
                    item = "Combs/Brushes"
                    data.append(self.numInThirdCell(df_raw, ind, location, date, weatherlist, item))

                elif re.search(r'\bSHARKASTICS\b', col1[ind]):
                    item = "SHARKASTICS"
                    data.append(self.numInThirdCell(df_raw, ind, location, date, weatherlist, item))

                elif re.match(r'^Oyster spacer  Small', col1[ind]):
                    item = "Oyster spacer (small)"
                    data.append(self.numInThirdCell(df_raw, ind, location, date, weatherlist, item))

                elif re.match(r'^Oyster spacer  Large', col1[ind]):
                    item = "Oyster spacer (large)"
                    data.append(self.numInThirdCell(df_raw, ind, location, date, weatherlist, item))

                elif re.match(r'^Hagfish traps', col1[ind]):
                    item = "Hagfish Traps"
                    data.append(self.numInThirdCell(df_raw, ind, location, date, weatherlist, item))

                elif re.match(r'^Strapping bands', col1[ind]):
                    item = "Strapping Bands"
                    data.append(self.numInThirdCell(df_raw, ind, location, date, weatherlist, item))

                elif re.match(r'^Weed whacker pieces', col1[ind]):
                    item = "Weed Whacker Pieces"
                    data.append(self.numInThirdCell(df_raw, ind, location, date, weatherlist, item))

                elif re.match(r'^Zipties', col1[ind]):
                    item = "Zipties"
                    data.append(self.numInThirdCell(df_raw, ind, location, date, weatherlist, item))

                elif re.match(r'^Irrigation tubing', col1[ind]):
                    item = "Irrigation Tubing/Parts"
                    data.append(self.numInThirdCell(df_raw, ind, location, date, weatherlist, item))

                elif re.match(r'^Toys', col1[ind]):
                    item = "Toys (plastic only)"
                    data.append(self.numInThirdCell(df_raw, ind, location, date, weatherlist, item))

                elif re.match(r'^Firecracker remnants', col1[ind]):
                    item = "Firecracker Remnants"
                    data.append(self.numInThirdCell(df_raw, ind, location, date, weatherlist, item))

                elif re.match(r'^Duct tape pieces', col1[ind]):
                    item = "Duct Tape Pieces"
                    data.append(self.numInThirdCell(df_raw, ind, location, date, weatherlist, item))

                elif re.match(r'^Golf balls', col1[ind]):
                    item = "Golf Balls"
                    data.append(self.numInThirdCell(df_raw, ind, location, date, weatherlist, item))

                elif re.match(r'^Christmas tree parts/ornaments', col1[ind]):
                    item = "Christmas Tree Parts/Ornaments"
                    data.append(self.numInThirdCell(df_raw, ind, location, date, weatherlist, item))

                elif re.match(r'^Pens/markers/pencils', col1[ind]):
                    item = "Pens/Markers/Pencils"
                    data.append(self.numInThirdCell(df_raw, ind, location, date, weatherlist, item))

                elif re.match(r'^Melted plastic', col1[ind]):
                    item = "Melted Plastic"
                    data.append(self.numInThirdCell(df_raw, ind, location, date, weatherlist, item))

                elif re.match(r'^Snorkel/dive/surf/kayak/camping gear', col1[ind]):
                    item = "Outdoor Sports Gear"
                    data.append(self.numInThirdCell(df_raw, ind, location, date, weatherlist, item))

                elif re.match(r'^DVD/cd/cassette/records', col1[ind]):
                    item = "DVD/CD/Cassette/Records"
                    data.append(self.numInThirdCell(df_raw, ind, location, date, weatherlist, item))

                elif re.match(r'^Spools', col1[ind]):
                    item = "Spools"
                    data.append(self.numInThirdCell(df_raw, ind, location, date, weatherlist, item))

                elif re.match(r'^Popsicle', col1[ind]):
                    item = "Popsicle Sticks"
                    data.append(self.numInThirdCell(df_raw, ind, location, date, weatherlist, item))

                elif re.match(r'^Shotgun', col1[ind]):
                    item = "Shotgun Shells"
                    data.append(self.numInSameCell(df_raw, ind, location, date, weatherlist, item, 0))

                elif re.match(r'^Linoleum', col1[ind]):
                    item = "Linoleum"
                    data.append(self.numInSameCell(df_raw, ind, location, date, weatherlist, item, 0))

                elif re.match(r'^Gardening pots/trays', col1[ind]):
                    item = "Gardening Pots/Trays"
                    data.append(self.numInThirdCell(df_raw, ind, location, date, weatherlist, item))

                elif re.match(r'^Crates/trays:', col1[ind]):
                    item = "Crates/Trays"
                    data.append(self.multiItemInSameCell(df_raw, ind, location, date, weatherlist, item, 0))

                    item = "Large Drums/Jugs"
                    data.append(self.multiItemInSameCell(df_raw, ind, location, date, weatherlist, item, 1))

                elif re.match(r'^Auto parts', col1[ind]):
                    item = "Auto Parts"
                    data.append(self.numInThirdCell(df_raw, ind, location, date, weatherlist, item))

                elif re.match(r'^Shipping Tags', col1[ind]):
                    item = "Shipping Tags"
                    data.append(self.numInThirdCell(df_raw, ind, location, date, weatherlist, item))

                elif re.match(r'^Drug:', col1[ind]):
                    item = "Drug"
                    data.append(self.multiItemInSameCell(df_raw, ind, location, date, weatherlist, item, 0))

                    item = "Personal Stuff"
                    data.append(self.multiItemInSameCell(df_raw, ind, location, date, weatherlist, item, 1))

                elif re.match(r'^Misc. household items', col1[ind]):
                    item = "Misc. Household Items"
                    data.append(self.numInThirdCell(df_raw, ind, location, date, weatherlist, item))

                #column 2
                try:
                    if re.match(r'^food-related:', df_raw.iloc[:,1][ind]):      #.iloc is an alternate way to reference the column
                        item = "Food-Related Foam Fragment"
                        data.append(self.numInSameCell(df_raw, ind, location, date, weatherlist, item, 1))

                    elif re.match(r'^oil bottles:', df_raw.iloc[:,1][ind]):  
                        item = "Oil Bottles"
                        data.append(self.numInSameCell(df_raw, ind, location, date, weatherlist, item, 1))
                    
                    elif re.match(r'^cigar tips:', df_raw.iloc[:,1][ind]):  
                        item = "Cigar Tips"
                        data.append(self.numInSameCell(df_raw, ind, location, date, weatherlist, item, 1))

                    elif re.match(r'^line:', df_raw.iloc[:,1][ind]):  
                        item = "Line"
                        data.append(self.numInSameCell(df_raw, ind, location, date, weatherlist, item, 1))

                    elif re.match(r'^plates:', df_raw.iloc[:,1][ind]):  
                        item = "Plates"
                        data.append(self.numInSameCell(df_raw, ind, location, date, weatherlist, item, 1))

                    elif re.match(r'^ribbons:', df_raw.iloc[:,1][ind]):  
                        item = "Ribbons"
                        data.append(self.numInSameCell(df_raw, ind, location, date, weatherlist, item, 1))

                    elif re.match(r'^Lightsticks:', df_raw.iloc[:,1][ind]):  
                        item = "Lightsticks"
                        data.append(self.numInSameCell(df_raw, ind, location, date, weatherlist, item, 1))

                    elif re.match(r'^Vinyl:', df_raw.iloc[:,1][ind]):  
                        item = "Vinyl"
                        data.append(self.numInSameCell(df_raw, ind, location, date, weatherlist, item, 1))

                    elif re.match(r'^ pet stuff:', df_raw.iloc[:,1][ind]):  
                        item = "Pet Stuff"
                        data.append(self.numInSameCell(df_raw, ind, location, date, weatherlist, item, 1))

                except:
                    pass
        #print(df_raw)
        print(data)
        return data
    
    def exportDFtoExcel(self, listOfListsData, i):
        df_cleaned = pandas.DataFrame(self.clearListsInLoL(listOfListsData))
        df_cleaned.to_excel(os.path.join(self.script_dir,f"cleanedoutput{i}.xlsx"))

    def numInSameCell(self, inputDF, rowIndex, location, date, weatherlist, item, column):
        return [location, weatherlist, date,
            self.category(item), self.subCategory(item), item, 
            int(re.findall(r'\d+', inputDF.iloc[:,column][rowIndex])[0])]

    def numInThirdCell(self, inputDF, rowIndex, location, date, weatherlist, item):
        return [location, weatherlist, date, 
            self.category(item), self.subCategory(item), item, 
            inputDF.iloc[:,2][rowIndex]]
    
    def multiItemInSameCell(self, inputDF, rowIndex, location, date, weatherlist, item, i):
        itemNumberList = re.findall(r'\d+', inputDF.iloc[:,0][rowIndex])
        return [location, weatherlist, date, 
            self.category(item), self.subCategory(item), item, 
            int(itemNumberList[i])]

    def findWeatherList(self, inputDF):
        weather = inputDF.columns[1].split(" ")
        for i, word in enumerate(weather):
            if word not in ["windy", "sunny", "overcast", "low", "high"]:
                weather.pop(i)
        return weather
    
    def clearListsInLoL(self, inputList):   # findWeatherList gives a list. we want to clear subsublists
        for subList in inputList:
            for i, element in enumerate(subList):
                if type(element) == list:
                    for x in element:
                        subList.insert(i, x)
                    subList.pop(i+len(element))
                    i += len(element)
        return inputList

    def category(self, item):
        if item in ["Foam Fragment", "Food-Related Foam Fragment", "Insulation/Packaging", "Buoys", "Carpet Padding"]:
            return "Foam"
        elif item in ["Hard Plastic Fragment", "Plastic Film", "Food Wrappers", "Food Packaging", "Beverage Bottles", 
            "Cleaning Bottles", "Oil Bottles", "Fishing Containers/Packaging", "Bottle/Container Caps, Lids", 
            "Cigarettes/Filters/Cigars", "Cigar Tips", "Cigarette Lighters", "6 Pack Rings", 
            "Bags", "Plastic Rope/Small Net Pieces", "Buoys, Floats", "Fishing Lures", "Line", 
            "Cups", "Plates", "Plastic Utensils", "Straws", "Balloons", "Ribbons", "Sanitary", 
            "Diapers", "First Aid", "Personal Care", "Toothbrushes", "Combs/Brushes", "SHARKASTICS", "Oyster spacer (small)", 
            "Oyster spacer (large)", "Hagfish Traps", "Strapping Bands", "Weed Whacker Pieces", "Zipties", "Irrigation Tubing/Parts", 
            "Toys (plastic only)", "Firecracker Remnants", "Duct Tape Pieces", "Golf Balls", "Christmas Tree Parts/Ornaments", 
            "Pens/Markers/Pencils", "Melted Plastic", "Outdoor Sports Gear", "DVD/CD/Cassette/Records", 
            "Spools", "Popsicle Sticks", "Shotgun Shells", "Lightsticks", "Linoleum", "Vinyl", "Gardening Pots/Trays", 
            "Crates/Trays", "Large Drums/Jugs", "Shipping Tags", "Drug", "Personal Stuff", 
            "Pet Stuff", "Misc. Household Items", ]:
            return "Plastic"
        elif item in ["Beer or Other Bottles", "Wine Bottles", "Jars", 
            "Glass Fragments", "Fiberglass Pieces", "Lightbulbs", "Ceramics"]:
            return "Glass"
        elif item in ["Flip-flops/slippers", "Gloves", "Tyres", "Rubber Fragments", "Rubber Toys"]:
            return "Rubber"
        elif item in ["Cardboard Cartons", "Paper and Cardboard", "Paper Bags", "Lumber/Building Materials"]:
            return "Processed Wood"
        elif item in ["Clothing (including hats)", "Shoes (non-rubber)", "Gloves (non-rubber)", "Towels/Rags", "Fabric Pieces", 
            "Carpet Pieces", "Masks", "Pillows", "Bedspread", "Burlap"]:
            return "Cloth/Fabric"
        elif item in ["Aluminum Cans", "Aerosol Cans", "Food Tins", "Roofing", "Metal Fragments", 
            "Bottle Caps", "Batteries", "Fishing Pole/Gear", "Wire/Stakes/Pipes", "Foil", "Hydroflask"]:
            return "Metal"
        elif item == "N/A":
            return "Large Debris/Noteworthy"
        elif item == "Auto Parts":
            return "UNKNOWN AUTO PARTS TYPE"

    def subCategory(self, item):
        if item in ["Food Wrappers", "Food Packaging"]:
            return "Food"
        elif item in ["Cleaning Bottles", "Oil Bottles"]:
            return "Cleaning/Oil"
        elif item in ["Cigarettes/Filters/Cigars", "Cigar Tips"]:
            return "Smoking"
        elif item in ["Fishing Lures", "Line"]:
            return "Lures/Line"
        elif item in ["Cups", "Plates"]:
            return "Silverware"
        elif item in ["Balloons", "Ribbons"]:
            return "Party"
        elif item in ["Sanitary", "Diapers", "First Aid", "Personal Care"]:
            return "Personal Care"
        elif item in ["Shotgun Shells", "Lightsticks"]:
            return "Cartridge"
        elif item in ["Linoleum", "Vinyl"]:
            return "Flooring"
        elif item in ["Crates/Trays", "Large Drums/Jugs"]:
            return "Containers"
        elif item in ["Drug", "Personal Stuff", "Pet Stuff"]:
            return "Care"
        elif item in ["Beer or Other Bottles", "Wine Bottles"]:
            return "Bottles"
        elif item in ["Bedspread", "Burlap"]:
            return "Bed/Burlap"
        elif item in ["Aluminum Cans", "Food Tins"]:
            return "Containers"
        elif item in ["Aerosol Cans", "Food Tins", "Roofing"]:
            return "Subcat1"
        else:
            return "N/A"

    #remove all whitespace, flip toggle when sees number, flip off when non number, then add all previous chars and numbers into list? then if the list is 1) only string, check third column, 2) string and number, add number, 3) multiple strings and numbers, split then add
    """def autoSort(self, inputDF):     # maybe there is a pattern after all? strip all whitespace, then strip every time you see a number except for 6 pack, tyres, and popsicle sticks?
        for row in df_raw.index:
            for jColumn in range(0,5):  #column0 = df_raw.iloc[:,0]
                if row != 0 and row != 1: """
                    

#newSheet = DataReader()
#data = newSheet.readin()
#newSheet.exportDFtoExcel(data, 1)

def autoSort():
    tempList = [["FOAM fragments:  85", ""], ["Plastic fragments (hard)", 5000], ["Food wrappers:    58          Food packaging: 79"]]
    flag = 0
    tempItemName = ""
    tempItemNumber = ""
    newList = []

    for subList in tempList:
        subList[0] = subList[0].replace(" ", "")
        #print(subList)
        for letter in subList[0]:
            if letter in "0123456789":
                flag = 1
                tempItemNumber += letter
            else:
                #print(letter)
                if flag == 1:
                    flag = 0
                    newList.append([tempItemName, int(tempItemNumber)])
                    tempItemName, tempItemNumber = "", ""
                tempItemName += letter
        if tempItemName != "" and tempItemNumber == "":
            tempItemNumber = subList[1]
            newList.append([tempItemName, int(tempItemNumber)])
            tempItemName, tempItemNumber = "", ""

    print(newList)

autoSort()