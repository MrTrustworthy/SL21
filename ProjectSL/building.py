__author__ = 'MrTrustworthy'

from xml.etree.ElementTree import parse



class Building(object):

    def __init__(self, name, level, p_wood, p_stone, p_food, p_water, p_iron, p_coal, p_gold, p_population, c_wood, c_stone, c_food, c_water, c_iron, c_coal, c_gold, c_population):
        self.name = name
        self.level = level

        self.production_wood = p_wood
        self.production_stone = p_stone
        self.production_food = p_food
        self.production_water = p_water
        self.production_iron = p_iron
        self.production_coal = p_coal
        self.production_gold = p_gold
        self.production_population = p_population

        self.upgrade_cost_wood = c_wood
        self.upgrade_cost_stone = c_stone
        self.upgrade_cost_food = c_food
        self.upgrade_cost_water = c_water
        self.upgrade_cost_iron = c_iron
        self.upgrade_cost_coal = c_coal
        self.upgrade_cost_gold = c_gold
        self.upgrade_cost_population = c_population

    def get_production(self):
        p = {"wood" : self.production_wood,
             "stone" : self.production_stone,
             "food" : self.production_food,
             "water": self.production_water,
             "iron": self.production_iron,
             "coal": self.production_coal,
             "gold": self.production_gold,
             "population" : self.production_population}
        return p

    def get_upgrade_cost(self):
        p = {"wood" : self.upgrade_cost_wood,
             "stone" : self.upgrade_cost_stone,
             "food" : self.upgrade_cost_food,
             "water" : self.upgrade_cost_water,
             "iron" : self.upgrade_cost_iron,
             "coal" : self.upgrade_cost_coal,
             "gold" : self.upgrade_cost_gold,
             "population" : self.upgrade_cost_population}

        return p

    def __str__(self):
        return "Building: (" + self.name + " with level " + str(self.level) +") producing [" \
                + str(self.production_wood) + ":" \
                + str(self.production_stone) + ":" \
                + str(self.production_food) + ":" \
                + str(self.production_population) + "]" \
                + " upgrade costs: [" \
                + str(self.upgrade_cost_wood) + ":" \
                + str(self.upgrade_cost_stone) + ":" \
                + str(self.upgrade_cost_food) + ":" \
                + str(self.upgrade_cost_population) + "]"


    def __repr__(self):
        return self.__str__()

def get_all_aviable_building_names():
    tree = parse("buildings.xml")
    root = tree.getroot()
    l = list()
    for building in root.findall("building"):
        l.append(building.attrib["name"])
    return l

def get_building(name, lvl):
    tree = parse("buildings.xml")
    root = tree.getroot()
    for building in root.findall("building"):
        if building.attrib == {"name":name}:

            for level in building.findall("level"):
                if level.attrib == {"value":str(lvl)}:

                    for production in level.iter("production"):
                        for upgrade_cost in level.iter("upgrade_cost"):
                            return Building(name, int(lvl),
                                         production.attrib["wood"],
                                         production.attrib["stone"],
                                         production.attrib["food"],
                                         production.attrib["water"],
                                         production.attrib["iron"],
                                         production.attrib["coal"],
                                         production.attrib["gold"],
                                         production.attrib["population"],
                                         upgrade_cost.attrib["wood"],
                                         upgrade_cost.attrib["stone"],
                                         upgrade_cost.attrib["food"],
                                         upgrade_cost.attrib["water"],
                                         upgrade_cost.attrib["iron"],
                                         upgrade_cost.attrib["coal"],
                                         upgrade_cost.attrib["gold"],
                                         upgrade_cost.attrib["population"])



if __name__ == "__main__":
    print get_all_aviable_building_names()