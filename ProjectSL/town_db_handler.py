__author__ = 'MrTrustworthy'


import sqlite3
from app_config import TOWN_DB_URI
import error_handling


def setup_tables():
    with sqlite3.connect(TOWN_DB_URI) as connection:
        cursor = connection.cursor()
        cursor.execute("""CREATE TABLE towns(
                        town_id integer PRIMARY KEY AUTOINCREMENT,
                        town_name text,
                        town_owner text,
                        town_resource_wood integer,
                        town_resource_stone integer,
                        town_resource_food integer,
                        town_resource_water integer,
                        town_resource_iron integer,
                        town_resource_coal integer,
                        town_resource_gold integer,
                        town_resource_population integer
                        )""")
        cursor.execute("""CREATE TABLE buildings(
            town_id integer,
            building_name text,
            building_level integer
            )""")

#
# BUILDING HANDLING
#
def add_building(town_id, building_name, building_level):
    with sqlite3.connect(TOWN_DB_URI) as connection:
        cursor = connection.cursor()
        cursor.execute("""INSERT INTO buildings VALUES(?,?,?)""", (town_id, building_name, building_level))

def delete_all_buildings(town_id):
    with sqlite3.connect(TOWN_DB_URI) as connection:
        cursor = connection.cursor()
        cursor.execute("""DELETE FROM buildings WHERE town_id=?""", (town_id,))
        """ Does not work as intended (towns without buildings!)
        if cursor.rowcount == 0:
            raise error_handling.DatabaseQueryFailed("delete all buildings")
        """


def update_building_level(town_id, building_name, building_level): #### NOT USED / NEEDED AFAIK
    with sqlite3.connect(TOWN_DB_URI) as connection:
        cursor = connection.cursor()
        cursor.execute("""UPDATE buildings SET building_level=? WHERE town_id=? AND building_name=?""", (building_level, town_id, building_name))
        if cursor.rowcount == 0:
            raise error_handling.DatabaseQueryFailed("update building level")


def get_buildings(town_id):
    with sqlite3.connect(TOWN_DB_URI) as connection:
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM buildings WHERE town_id =?""", (town_id,))
        result = cursor.fetchall()
        return result

#
# TOWN HANDLING
#
def add_town(name, owner, wood=10, stone=10, food=5, water=5, iron=0, coal=0, gold=10, population=1):
    with sqlite3.connect(TOWN_DB_URI) as connection:
        cursor = connection.cursor()
        cursor.execute("""INSERT INTO towns VALUES(NULL,?,?,?,?,?,?,?,?,?,?)""", (name, owner, wood, stone, food, water, iron, coal, gold, population))
        if cursor.rowcount == 0:
            raise error_handling.DatabaseQueryFailed("add town")




def update_town(id, name, owner, wood, stone, food, water, iron, coal, gold, population):
    with sqlite3.connect(TOWN_DB_URI) as connection:
        cursor = connection.cursor()
        cursor.execute("""UPDATE towns SET
                            town_name=?,
                            town_owner=?,
                            town_resource_wood=?,
                            town_resource_stone=?,
                            town_resource_food=?,
                            town_resource_water=?,
                            town_resource_iron=?,
                            town_resource_coal=?,
                            town_resource_gold=?,
                            town_resource_population=?
                            WHERE town_id=?""", (name, owner, wood, stone, food, water, iron, coal, gold, population, id))
        if cursor.rowcount == 0:
            raise error_handling.DatabaseQueryFailed("update town")


def get_towns(owner = None):
    with sqlite3.connect(TOWN_DB_URI) as connection:
        cursor = connection.cursor()
        if owner is not None:
            cursor.execute("""SELECT * FROM towns WHERE town_owner=?""", (owner,))
        else:
            cursor.execute("""SELECT * FROM towns""")
        result = cursor.fetchall()
        return result


def get_town(owner):
    with sqlite3.connect(TOWN_DB_URI) as connection:
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM towns WHERE town_owner=?""", (owner,))
        result = cursor.fetchall()
        return result


def change_format(result):
    pass


def demo():
    setup_tables()
    add_town("home", "ad", 3, 3, 3, 3)
    add_town("home2", "ad2", 4, 5, 6, 7)
    add_building(1, "Headquarter", 1)
    add_building(1, "Farm", 2)
    add_building(2, "Headquarter", 3)
    print get_towns()
    print get_buildings(1)


if __name__ == "__main__":
    setup_tables()
