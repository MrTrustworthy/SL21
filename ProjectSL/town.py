__author__ = 'MrTrustworthy'
import town_db_handler
from building import get_building, get_all_aviable_building_names
from error_handling import *
class Town(object):
    
    def __init__(self, id, name, owner, wood, stone, food, population):

        self.id = id
        self.name = name
        self.owner = owner

        self.ressource_wood = wood
        self.ressource_stone = stone
        self.ressource_food = food
        self.ressource_population = population

        self.building_list = list()


    #
    # BASIC INFORMATION GETTERS
    #
    def get_ressources(self):
        d = {"wood": self.ressource_wood,
             "stone": self.ressource_stone,
             "food": self.ressource_food,
             "population": self.ressource_population}
        return d


    def get_total_production(self):
        d = {"wood": 0,
             "stone": 0,
             "food": 0,
             "population": 0}
        for building in self.building_list:
            d2 = building.get_production()
            d["wood"] = d["wood"] + int(d2["wood"])
            d["stone"] = d["stone"] + int(d2["stone"])
            d["food"] = d["food"] + int(d2["food"])
            d["population"] = d["population"] + int(d2["population"])
        return d


    #
    # BUILDING RELATED FUNCTIONS
    #
    def withdraw_ressources(self, wood, stone, food, population):
        if ( self.ressource_wood - wood >= 0 ) \
        and ( self.ressource_stone - stone >= 0 )\
        and ( self.ressource_food - food >= 0 )\
        and ( self.ressource_population - population >= 0 ): #if enough ressources are aviable

            self.ressource_wood -= wood
            self.ressource_stone -= stone
            self.ressource_food -= food
            self.ressource_population -= population
        else:
            raise NotEnoughRessources(self.name)



    def get_constructable_buildings(self):
        name_list = get_all_aviable_building_names()
        for building in self.building_list:
            name_list.remove(building.name)

        aviable_buildings_list = list()
        for name in name_list:
            aviable_buildings_list.append(get_building(name, 0)) # LVL 0 Building contains cost for creating and production of a lvl 1 building
        return aviable_buildings_list


    def construct_building(self, building_name):
        for building in self.building_list:
            if building.name == building_name:
                raise BuildingAlreadyExists(building_name)
        create_building = get_building(building_name, 0)
        cost = create_building.get_upgrade_cost()

        try:
            self.withdraw_ressources(int(cost["wood"]), int(cost["stone"]), int(cost["food"]), int(cost["population"]))
        except (NotEnoughRessources), e:
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
                    self.withdraw_ressources( int(cost["wood"]), int(cost["stone"]), int(cost["food"]), int(cost["population"]) )
                except NotEnoughRessources, e:
                    e.purpose = "upgrading " + building_name
                    raise e
                    new_building = get_building(building.name, (building.level+1) )
                    self.building_list.remove(building)
                    self.building_list.append(new_building)
                return


    #
    # OTHER FUNCTIONS AND UTILITIES
    #
    def process_tick(self):
        production = self.get_total_production()
        self.ressource_wood += production["wood"]
        self.ressource_stone += production["stone"]
        self.ressource_food += production["food"]
        self.ressource_population += production["population"]



    def __str__(self):
        return "Town: (" + str(self.id) + ") " \
               + self.name + "/" + self.owner + "[" \
               + str(self.ressource_wood) + ":"\
               + str(self.ressource_stone) + ":"\
               + str(self.ressource_food) + ":"\
               + str(self.ressource_population) + "] Buildings:\n" \
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
        t = Town(town[0], town[1], town[2], town[3], town[4], town[5], town[6])
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
                                    town.ressource_wood,
                                    town.ressource_stone,
                                    town.ressource_food,
                                    town.ressource_population)
        town_db_handler.delete_all_buildings(town.id)
        for building in town.building_list:
            town_db_handler.add_building(town.id, building.name, building.level)







if __name__ == "__main__":
    towns = load_towns()
    #towns[0].ressource_wood = 222
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
