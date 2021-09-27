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

        location = df_raw["SHARKastics Marine Debris"][0].split(" ")[1]
        weatherlist = self.findWeatherList(df_raw)
        date = df_raw.iloc[:,3][0]

        col1name = df_raw.columns[0]

        for ind in df_raw.index:
            if ind != 0 and ind != 1:       # because of the inconsistent way in which types serve as headers over items, it's difficult to avoid this messy regex cell by cell IF hell.
                #column 1
                if re.match(r'^FOAM fragments:', df_raw["SHARKastics Marine Debris"][ind]): # can be replaced by df.columns for inferential reference
                    item = "Foam Fragment"
                    
                    data.append(self.numInSameCell(df_raw, ind, location, date, weatherlist, item))
                    """data.append([location,
                    weatherlist, 
                    df_raw["Unnamed: 3"][0], 
                    self.category(item), "N/A", item, 
                    int(re.findall(r'\d+', df_raw["SHARKastics Marine Debris"][ind])[0])])"""

                elif re.match(r'^Plastic fragments', df_raw["SHARKastics Marine Debris"][ind]):
                    if "hard" in df_raw["SHARKastics Marine Debris"][ind]:   
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
                
                elif re.match(r'^Food wrappers:', df_raw["SHARKastics Marine Debris"][ind]):
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

                elif re.match(r'^Beverage bottles', df_raw["SHARKastics Marine Debris"][ind]):
                    item = "Beverage Bottles"
                    data.append(self.numInThirdCell(df_raw, ind, location, date, weatherlist, item))

                elif re.match(r'^Cleaning bottles:', df_raw["SHARKastics Marine Debris"][ind]):  
                    item = "Cleaning Bottles"

                    data.append(self.numInSameCell(df_raw, ind, location, date, weatherlist, item))

                elif re.match(r'^Fishing containers/packaging:', df_raw["SHARKastics Marine Debris"][ind]):  
                    item = "Fishing Containers/Packaging"
                    data.append(self.numInThirdCell(df_raw, ind, location, date, weatherlist, item))

                elif re.match(r'^Bottle or container caps/lids', df_raw["SHARKastics Marine Debris"][ind]):  
                    item = "Bottle/Container Caps, Lids"
                    data.append(self.numInThirdCell(df_raw, ind, location, date, weatherlist, item))

                
                elif re.match(r'^Cigarettes', df_raw["SHARKastics Marine Debris"][ind]):
                    item = "Cigarettes/Filters/Cigars"
                    data.append(self.numInSameCell(df_raw, ind, location, date, weatherlist, item))
                
                

                #column 2
                try:
                    if re.match(r'^food-related:', df_raw.iloc[:,1][ind]):      #.iloc is an alternate way to reference the column
                        item = "Food-Related Foam Fragment"
                        data.append(self.numInSameCell(df_raw, ind, location, date, weatherlist, item))

                    elif re.match(r'^oil bottles:', df_raw.iloc[:,1][ind]):  
                        item = "Oil Bottles"
                        data.append(self.numInSameCell(df_raw, ind, location, date, weatherlist, item))
                    
                    elif re.match(r'^cigar tips:', df_raw.iloc[:,1][ind]):  
                        item = "Cigar Tips"
                        data.append(self.numInSameCell(df_raw, ind, location, date, weatherlist, item))

                except:
                    pass
        #print(df_raw)
        df_cleaned = pandas.DataFrame(self.clearListsInLoL(data))
        #df_cleaned.to_excel(os.path.join(self.script_dir,'cleanedoutput.xlsx'))
        print(data)
    
    def numInSameCell(self, inputDF, rowIndex, location, date, weatherlist, item):
        return [location, weatherlist, date,
            self.category(item), self.subCategory(item), item, 
            int(re.findall(r'\d+', inputDF.iloc[:,0][rowIndex])[0])]

    def numInThirdCell(self, inputDF, rowIndex, location, date, weatherlist, item):
        return [location, weatherlist, date, 
            self.category(item), self.subCategory(item), item, 
            inputDF.iloc[:,2][rowIndex]]
    
    def multiItemInSameCell(self, inputDF, rowIndex, location, date, weatherlist, item, i):
        itemNumberList = re.findall(r'\d+', inputDF.iloc[:,0][rowIndex])
        return [location, weatherlist, date, 
            self.category(item), self.subCategory(item), item, 
            itemNumberList[i]]

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
            "Diapers", "First Aid", "Personal Care", "Toothbrushes", "Combs/Brushs", "SHARKASTICS", "Oyster spacer (small)", 
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


newSheet = DataReader()
newSheet.readin()