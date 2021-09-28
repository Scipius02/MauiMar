import re

class FINDOTHERCELL:
    def __init__(self, inputDF):
        self.inputDF = inputDF

    def findWeatherList(self, inputDF):
        weather = inputDF.columns[1].split(" ")
        for i, word in enumerate(weather):
            if word not in ["windy", "sunny", "overcast", "low", "high"]:
                weather.pop(i)
        return weather

    """def quantityInSameCell(self):
        return [int(re.findall(r'\d+', inputDF.iloc[:,column][rowIndex])[0])]

    def quantityInThirdCell(self):
        return [self.inputDF.iloc[:,columnIndex][rowIndex]]"""