class CLASSIFY:
    def __init__(self, itemName):
        self.name = itemName

    def category(self, itemName):
        print(itemName)
        categoryDict = {"Foam":["FoamFragments", "FoodRelated", "InsulationPackaging", "Buoys", "CarpetPadding"],
                        "Plastic":["PlasticFragmentsHard", "PlasticFragmentsFilm", "FoodWrappers", "FoodPackaging", "BeverageBottles", 
                            "CleaningBottles", "OilBottles", "FishingContainersPackaging", "BottleOrContainerCapsLids", 
                            "CigarettesFiltersCigars", "CigarTips", "CigaretteLighters", "PackRings", 
                            "Bags", "PlasticRopeSmallNetPieces", "BuoysAndFloats", "FishingLures", "Line", 
                            "Cup", "Plates", "PlasticUtensils", "Straws", "Balloons", "Ribbons", "Sanitary", 
                            "Diapers", "FirstAid", "PersCare", "Toothbrushes", "CombsBrushes", "Sharkastics", "OysterSpacerSmall", 
                            "OysterSpacerLarge", "HagfishTraps", "StrappingBands", "WeedWhackerPieces", "Zipties", "IrrigationTubingPartsPvcToo", 
                            "ToysPlasticOnly", "FirecrackerRemnants", "DuctTapePieces", "GolfBalls", "ChristmasTreePartsOrnaments", 
                            "PensMarkersPencils", "MeltedPlastic", "SnorkelDiveSurfKayakCampingGear", "DvdCdCassetteRecords", 
                            "Spools", "PopsicleSticks", "ShotgunShells", "Lightsticks", "Linoleum", "Vinyl", "GardeningPotsTrays", 
                            "CratesTrays", "LargeDrumsJugs", "ShippingTags", "Drug", "PersonalStuff", 
                            "PetStuff", "MiscHouseholdItems"],
                        "Glass":["BeerOrOtherBottles", "WineBottles", "Jars", 
                            "GlassFragments", "FiberglassPieces", "OtherLightbulb", "OtherCeramics"],
                        "Rubber":["FlipFlopsSlippers", "Gloves", "Tires", "RubberFragments", "RubberToysTennisBalls"],
                        "Processed Wood":["CardboardCartons", "PaperAndCardboard", "PaperBags", "LumberBuildingMaterial"],
                        "Cloth/Fabric":["ClothingIncludingHats", "ShoesNonRubber", "GlovesNonRubber", "TowelsRags", "FabricPieces", 
                            "CarpetPieces", "Masks", "Pillows", "Bedspread", "Burlap"],
                        "Metal":["AluminumCans", "AerosolCans", "FoodTins", "Roofing", "MetalFragments", 
                            "BottleCaps", "Batteries", "FishingPoleGear", "WireStakesPipes", "Foil", "Hydroflask"],
                        "UNKNOWN AUTO PARTS TYPE":["AutoParts"]}
        for key, valueList in categoryDict.items():
            if itemName in valueList:
                    return key
        else:
            return -1

    def subCategory(self, itemName):
        if itemName in ["Food Wrappers", "Food Packaging"]:
            return "Food"
        elif itemName in ["Cleaning Bottles", "Oil Bottles"]:
            return "Cleaning/Oil"
        elif itemName in ["Cigarettes/Filters/Cigars", "Cigar Tips"]:
            return "Smoking"
        elif itemName in ["Fishing Lures", "Line"]:
            return "Lures/Line"
        elif itemName in ["Cups", "Plates"]:
            return "Silverware"
        elif itemName in ["Balloons", "Ribbons"]:
            return "Party"
        elif itemName in ["Sanitary", "Diapers", "First Aid", "Personal Care"]:
            return "Personal Care"
        elif itemName in ["Shotgun Shells", "Lightsticks"]:
            return "Cartridge"
        elif itemName in ["Linoleum", "Vinyl"]:
            return "Flooring"
        elif itemName in ["Crates/Trays", "Large Drums/Jugs"]:
            return "Containers"
        elif itemName in ["Drug", "Personal Stuff", "Pet Stuff"]:
            return "Care"
        elif itemName in ["Beer or Other Bottles", "Wine Bottles"]:
            return "Bottles"
        elif itemName in ["Bedspread", "Burlap"]:
            return "Bed/Burlap"
        elif itemName in ["Aluminum Cans", "Food Tins"]:
            return "Containers"
        elif itemName in ["Aerosol Cans", "Food Tins", "Roofing"]:
            return "Subcat1"
        else:
            return "N/A"
