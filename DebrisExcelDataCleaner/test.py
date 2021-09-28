import re

class CELLFORMATTER:
    def __init__(self, inputCell):
        self.inputCell = inputCell

    def camelCaseValidator(inputCell):       # filter out empty cells and numbers, if input is a valid item, camel case and strip it of bad characters
        if inputCell == "":
            return -1
        elif type(inputCell) != int:
            if "total" in inputCell:
                return -1
            elif re.match(r"\b(?:PLASTICS|GLASS|Rubber|Processed Wood|Cloth/Fabric|Metal)\b", inputCell):
                return -1
            else:
                #print(inputCell)
                inputCell = inputCell.title()
                inputCell = re.sub(r"\W+", "", inputCell)
                inputCell = autoSort(inputCell)
        else:
            return -1
        
        return inputCell

    def autoSort(inputCell):
        #tempList = [["FOAM fragments:  85", ""], ["Plastic fragments (hard)", 5000], ["Food wrappers:    58          Food packaging: 79"]]
        newList = []

        newList = re.findall('([A-Za-z=]+|\d*)', inputCell)
        if newList[-1] == "":
            newList.pop()

        print(newList)
        return newList

for cell in ["FOAM fragments:  85", "Plastic fragments (hard)", "Food wrappers:    58          Food packaging: 79", "total plastic"]:
    camelCaseValidator(cell)