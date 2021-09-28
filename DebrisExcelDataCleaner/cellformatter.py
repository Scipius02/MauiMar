import re
import math

class CELLFORMATTER:
    def __init__(self, inputCell):
        self.inputCell = inputCell

    def camelCaseValidator(self, inputCell):       # filter out empty cells and numbers, if input is a valid item, camel case and strip it of bad characters
        if type(inputCell) == str:
            if re.search(r"total+|width+|length+|^\#", inputCell, re.IGNORECASE):
                return -1
            elif re.match(r"\b(?:PLASTICS|GLASS|^Rubber$|Processed Wood|Cloth/Fabric|^Metal$)\b", inputCell):
                return -1
            else:
                #print(inputCell)
                #print(type(inputCell))
                if inputCell[0] == "6":     # specific case dealing with 6pack
                    inputCell = inputCell[1:]
                elif "1st" in inputCell:
                    inputCell = inputCell.replace("1st", "First")
                    #print(inputCell)
                inputCell = inputCell.title()
                inputCell = re.sub(r"\W+", "", inputCell)
                cellItemsList = self.autoSort(inputCell)
        else:
            return -1
        
        #print(cellItemsList)
        return cellItemsList

    def autoSort(self, inputCell):
        #tempList = [["FOAM fragments:  85", ""], ["Plastic fragments (hard)", 5000], ["Food wrappers:    58          Food packaging: 79"]]
        newList = []

        newList = re.findall('([A-Za-z=]+|\d*)', inputCell)
        if newList[-1] == "":
            newList.pop()

        #print(newList)
        return newList

#for cell in ["FOAM fragments:  85", "Plastic fragments (hard)", "Food wrappers:    58          Food packaging: 79", "total plastic"]:
#    camelCaseValidator(cell)
"""sample = CELLFORMATTER("FOAM fragments:  85")
sample.camelCaseValidator(sample.inputCell)"""