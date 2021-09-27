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

        weatherlist = self.findWeatherList(df_raw)
        date = df_raw["Unnamed: 3"][0]

        col1name = df_raw.columns[0]

        for ind in df_raw.index:
            if ind != 0 and ind != 1:       # because of the inconsistent way in which types serve as headers over items, it's difficult to avoid this messy regex cell by cell IF hell.
                print(ind)
                if re.match(r'^FOAM fragments:', df_raw["SHARKastics Marine Debris"][ind]): # can be replaced by df.columns for inferential reference
                    data.append([df_raw["SHARKastics Marine Debris"][0],
                    "WEATHER1", "WEATHER2", "TIDE X", 
                    df_raw["Unnamed: 3"][0], 
                    "Foam", "N/A", "Foam Fragment", 
                    int(re.findall(r'\d+', df_raw["SHARKastics Marine Debris"][ind])[0])])

                elif re.match(r'^Plastic fragments', df_raw["SHARKastics Marine Debris"][ind]):
                    if "hard" in df_raw["SHARKastics Marine Debris"][ind]:   
                        data.append([df_raw["SHARKastics Marine Debris"][0],    # location
                        weatherlist,                       # weather, weather, tide
                        date,                                # date
                        "Plastic", "N/A", "Hard Plastic Fragment",                         # type, subtype, item name
                        df_raw["Unnamed: 2"][ind]])  # number
                    else:
                        data.append([df_raw["SHARKastics Marine Debris"][0],    # location
                        weatherlist,                       # weather, weather, tide
                        date,                                # date
                        "Plastic", "N/A", "Plastic Film",                         # type, subtype, item name
                        df_raw["Unnamed: 2"][ind]])  # number
                
                elif re.match(r'^Food wrappers:', df_raw["SHARKastics Marine Debris"][ind]):  
                    data.append([df_raw["SHARKastics Marine Debris"][0],    # location
                    weatherlist,                       # weather, weather, tide
                    date,                                # date
                    "Plastic", "N/A", "Food Wrappers",                         # type, subtype, item name
                    int(re.findall(r'\d+', df_raw["SHARKastics Marine Debris"][ind])[0])])  # number

                    data.append([df_raw["SHARKastics Marine Debris"][0],    # location
                    weatherlist,                       # weather, weather, tide
                    date,                                # date
                    "Plastic", "N/A", "Food Packaging",                         # type, subtype, item name
                    int(re.findall(r'\d+', df_raw["SHARKastics Marine Debris"][ind])[1])])  # number

                elif re.match(r'^Beverage bottles', df_raw["SHARKastics Marine Debris"][ind]):
                    data.append([df_raw["SHARKastics Marine Debris"][0], 
                    weatherlist, 
                    date, 
                    "Plastic", "N/A", "Beverage Bottles", 
                    df_raw["Unnamed: 2"][ind]])

                elif re.match(r'^Cleaning bottles:', df_raw["SHARKastics Marine Debris"][ind]):  
                    data.append([df_raw["SHARKastics Marine Debris"][0],    # location
                    weatherlist,                       # weather, weather, tide
                    date,                                # date
                    "Plastic", "N/A", "Cleaning Bottles",                         # type, subtype, item name
                    int(re.findall(r'\d+', df_raw["SHARKastics Marine Debris"][ind])[0])])  # number 

                elif re.match(r'^Fishing containers/packaging:', df_raw["SHARKastics Marine Debris"][ind]):  
                        data.append([df_raw["SHARKastics Marine Debris"][0],    # location
                        weatherlist,                       # weather, weather, tide
                        date,                                # date
                        "Plastic", "N/A", "Fishing Containers/Packaging",                         # type, subtype, item name
                        df_raw["Unnamed: 2"][ind]])  # number

                elif re.match(r'^Bottle or container caps/lids', df_raw["SHARKastics Marine Debris"][ind]):  
                        data.append([df_raw["SHARKastics Marine Debris"][0],    # location
                        weatherlist,                       # weather, weather, tide
                        date,                                # date
                        "Plastic", "N/A", "Bottle/Container Caps, Lids",                         # type, subtype, item name
                        df_raw["Unnamed: 2"][ind]])  # number
                
                elif re.match(r'^Cigarettes', df_raw["SHARKastics Marine Debris"][ind]):
                    data.append([df_raw["SHARKastics Marine Debris"][0], 
                    weatherlist, 
                    date, 
                    "Plastic", "N/A", "Cigarettes/Filters/Cigars", 
                    int(re.findall(r'\d+', df_raw["SHARKastics Marine Debris"][ind])[0])])

                #col 2
                try:
                    if re.match(r'^food-related:', df_raw.iloc[:,1][ind]):      #.iloc is an alternate way to reference the column
                        data.append([df_raw["SHARKastics Marine Debris"][0],    # location
                        weatherlist,                       # weather, weather, tide
                        date,                                # date
                        "Foam", "N/A", "Food-Related Foam Fragment",                         # type, subtype, item name
                        int(re.findall(r'\d+', df_raw.iloc[:,1][0])[0])])  # number

                    elif re.match(r'^oil bottles:', df_raw.iloc[:,1][ind]):  
                        data.append([df_raw["SHARKastics Marine Debris"][0],    # location
                        weatherlist,                       # weather, weather, tide
                        date,                                # date
                        "Plastic", "N/A", "Oil Bottles",                         # type, subtype, item name
                        int(re.findall(r'\d+', df_raw.iloc[:,1][0])[0])])  # number
                    
                    elif re.match(r'^cigar tips:', df_raw.iloc[:,1][ind]):  
                        data.append([df_raw["SHARKastics Marine Debris"][0],    # location
                        weatherlist,                       # weather, weather, tide
                        date,                                # date
                        "Plastic", "N/A", "Cigar Tips",                         # type, subtype, item name
                        int(re.findall(r'\d+', df_raw.iloc[:,1][0])[0])])  # number
                except:
                    pass
            #print(df_raw['Location: Ka\'ehu'][ind], df_raw['Vols: 25'][ind])
        #print(df_raw)
        print(data)
        #df_raw.to_excel(os.path.join(self.script_dir,'output.xlsx'))
        df_cleaned = self.clearListsInLoL(data)
        print(" ")
        print(data)
    
    def findWeatherList(self, inputDF):
        weather = inputDF.columns[1].split(" ")
        for i, word in enumerate(weather):
            if word not in ["windy", "sunny", "overcast", "low", "high"]:
                weather.pop(i)
        return weather
    
    def clearListsInLoL(self, inputList):
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
            "Crates/Trays", "Large Drums/Jugs", "Auto Parts", "Shipping Tags", "Drug", "Personal Stuff", 
            "Pet Stuff", "Misc. Household Items", ]:
            return "Plastic"
        elif item in [Beer or Other Bottles
Wine Bottles
Jars
Glass Fragments
Fiberglass Pieces
Lightbulbs
Ceramics
]:
            return "Glass"
        elif item in [Flip-flops/slippers
Gloves
Tyres
Rubber Fragments
Auto Parts
Rubber Toys
]:
            return "Rubber"
        elif item in [Cardboard Cartons
Paper and Cardboard
Paper Bags
Lumber/Building Materials
]:
            return "Processed Wood"
        elif item in [Clothing (including hats)
Shoes (non-rubber)
Gloves (non-rubber)
Towels/Rags
Fabric Pieces
Carpet Pieces
Masks
Pillows
Bedspread
Burlap
]:
            return "Cloth/Fabric"
        elif item in [Aluminum Cans
Aerosol Cans
Food Tins
Roofing
Metal Fragments
Auto Parts
Bottle Caps
Batteries
Fishing Pole/Gear
Wire/Stakes/Pipes
Foil
Hydroflask
]:
            return "Metal"
        elif item in [N/A
]:
            return "Large Debris/Noteworthy"

    def subCategory(self, item):
        if item in :
            return
        else:
            return "N/A"


newSheet = DataReader()
newSheet.readin()