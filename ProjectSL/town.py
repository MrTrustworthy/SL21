__author__ = 'MrTrustworthy'
import town_db_handler
from building import get_building, get_all_aviable_building_names
from error_handling import *
class Town(object):
    
    def __init__(self, id, name, owner, wood, stone, food, water, iron, coal, gold, population):

        self.id = id
        self.name = name
        self.owner = owner

        self.resource_wood = wood
        self.resource_stone = stone
        self.resource_food = food
        self.resource_water = water
        self.resource_iron = iron
        self.resource_coal = coal
        self.resource_gold = gold
        self.resource_population = population

        self.building_list = list()


    #
    # BASIC INFORMATION GETTERS
    #
    def get_resources(self):
        d = {"wood": self.resource_wood,
             "stone": self.resource_stone,
             "food": self.resource_food,
             "water": self.resource_water,
             "iron": self.resource_iron,
             "coal": self.resource_coal,
             "gold": self.resource_gold,
             "population": self.resource_population}
        return d


    def get_total_production(self):
        d = {"wood": 0,
             "stone": 0,
             "food": 0,
             "water": 0,
             "iron": 0,
             "coal": 0,
             "gold": 0,
             "population": 0}
        for building in self.building_list:
            d2 = building.get_production()
            d["wood"] = d["wood"] + int(d2["wood"])
            d["stone"] = d["stone"] + int(d2["stone"])
            d["food"] = d["food"] + int(d2["food"])
            d["water"] = d["water"] + int(d2["water"])
            d["iron"] = d["iron"] + int(d2["iron"])
            d["coal"] = d["coal"] + int(d2["coal"])
            d["gold"] = d["gold"] + int(d2["gold"])
            d["population"] = d["population"] + int(d2["population"])
        return d


    #
    # BUILDING RELATED FUNCTIONS
    #
    def withdraw_resources(self, wood, stone, food, water, iron, coal, gold, population):
        if ( self.resource_wood - wood >= 0 ) \
        and ( self.resource_stone - stone >= 0 ) \
        and ( self.resource_food - food >= 0 ) \
        and ( self.resource_water - water >= 0 ) \
        and ( self.resource_iron - iron >= 0 ) \
        and ( self.resource_coal - coal >= 0 ) \
        and ( self.resource_gold - gold >= 0 ) \
        and ( self.resource_population - population >= 0 ):

            self.resource_wood -= wood
            self.resource_stone -= stone
            self.resource_food -= food
            self.resource_water -= water
            self.resource_iron -= iron
            self.resource_coal -= coal
            self.resource_gold -= gold
            self.resource_population -= population

        else:
            raise NotEnoughResources(self.name)



    def get_constructable_buildings(self):
        name_list = get_all_aviable_building_names()
        for building in self.building_list:
            name_list.remove(building.name)

        aviable_buildings_list = list()
        for name in name_list:
            # LVL 0 Building contains cost for creating and production of a lvl 1 building
            aviable_buildings_list.append(get_building(name, 0))
        return aviable_buildings_list


    def construct_building(self, building_name):
        for building in self.building_list:
            if building.name == building_name:
                raise BuildingAlreadyExists(building_name)
        create_building = get_building(building_name, 0)
        cost = create_building.get_upgrade_cost()

        try:
            self.withdraw_resources(int(cost["wood"]), int(cost["stone"]),
                                    int(cost["food"]), int(cost["water"]),
                                    int(cost["iron"]), int(cost["coal"]),
                                    int(cost["gold"]), int(cost["population"]))
        except (NotEnoughResources), e:
            e.purpose = "building " + building_name
            raise e
        else:
            new_building = get_building(building_name, 1)
            self.building_list.append(new_building)


    def upgrade_building(self, building_name):
        for building in self.building_list:
            if building.name == building_name:
                cost = building.get_upgrade_cost()

                try:
                    self.withdraw_resources(int(cost["wood"]), int(cost["stone"]),
                                            int(cost["food"]), int(cost["water"]),
                                            int(cost["iron"]), int(cost["coal"]),
                                            int(cost["gold"]), int(cost["population"]))
                except NotEnoughResources, e:
                    e.purpose = "upgrading " + building_name
                    raise e
                else:
                    new_building = get_building(building.name, (building.level+1) )
                    self.building_list.remove(building)
                    self.building_list.append(new_building)
                return


    #
    # OTHER FUNCTIONS AND UTILITIES
    #
    def process_tick(self):
        production = self.get_total_production()
        self.resource_wood += production["wood"]
        self.resource_stone += production["stone"]
        self.resource_food += production["food"]
        self.resource_water += production["water"]
        self.resource_iron += production["coal"]
        self.resource_coal += production["iron"]
        self.resource_gold += production["gold"]
        self.resource_population += production["population"]



    def __str__(self):
        return "Town: (" + str(self.id) + ") " \
               + self.name + "/" + self.owner + "[" \
               + str(self.resource_wood) + ":"\
               + str(self.resource_stone) + ":"\
               + str(self.resource_food) + ":" \
               + str(self.resource_water) + ":" \
               + str(self.resource_iron) + ":" \
               + str(self.resource_coal) + ":" \
               + str(self.resource_gold) + ":"\
               + str(self.resource_population) + "] Buildings:\n" \
               + str([ (str(building)) for building in self.building_list]) + "\n"

    def __repr__(self):
        return self.__str__()

#
# BASIC TOWN_LIST MANAGEMENT FUNCTIONS, MAYBE OUTSOURCE TO TOWN_HANDLER-CLASS??
#

def load_towns():
    town_list = list()
    db_elements = town_db_handler.get_towns()
    for town in db_elements:
        t = Town(town[0], town[1], town[2], town[3], town[4], town[5], town[6], town[7], town[8], town[9], town[10])
        buildings = town_db_handler.get_buildings(t.id)
        for building in buildings:
            b = get_building(building[1], building[2])
            t.building_list.append(b)
        town_list.append(t)
    return town_list


def save_towns(town_list):
    for town in town_list:
        town_db_handler.update_town(town.id,
                                    town.name,
                                    town.owner,
                                    town.resource_wood,
                                    town.resource_stone,
                                    town.resource_food,
                                    town.resource_water,
                                    town.resource_iron,
                                    town.resource_coal,
                                    town.resource_gold,
                                    town.resource_population)
        town_db_handler.delete_all_buildings(town.id)
        for building in town.building_list:
            town_db_handler.add_building(town.id, building.name, building.level)







if __name__ == "__main__":
    towns = load_towns()
    #towns[0].resource_wood = 222
    print towns
    for town in towns:
        print town.name, town.get_total_production()

    #print towns[1].construct_building("Fountain")
    print 50*"x"
    print towns[0]
    print towns[1]

    #towns[0].level_up_building("Farm")
    #print 20* "X"


    #towns[0].building_list.append(get_building("Fountain", "1"))
    #print towns
    #save_towns(towns)


    #Town("home2", "ad2")
    #for element in town_list:
    #    print element
