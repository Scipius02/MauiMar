import re

class FINDOTHERCELL:
    def __init__(self, inputDF):
        self.inputDF = inputDF

    def findWeatherList(self, inputDF):
        # sometimes weather is in same cell, sometimes in adjacent.
        if inputDF.columns[2] != "":
            weather = inputDF.columns[2].split(" ")
        else:
            weather = inputDF.columns[1].split(" ")

        for i, word in enumerate(weather):
            if re.search(r"windy|sunny|overcast|low|high", word, re.IGNORECASE) == None:
                weather.pop(i)
        
        while len(weather) < 3:
            weather.append("X")
        return weather

    """def quantityInSameCell(self):
        return [int(re.findall(r'\d+', inputDF.iloc[:,column][rowIndex])[0])]

    def quantityInThirdCell(self):
        return [self.inputDF.iloc[:,columnIndex][rowIndex]]"""