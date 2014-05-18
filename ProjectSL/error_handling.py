__author__ = 'MrTrustworthy'

class UserDoesNotExist(Exception):
    def __init__(self, username):
        self.username = username
    def __str__(self):
        return "User does not exist: " + self.username

class WrongPassword(Exception):
    def __init__(self, username):
        self.username = username
    def __str__(self):
        return "Password is Wrong for user: " + self.username

class DatabaseQueryFailed(Exception):
    def __init__(self, query_info):
        self.query_info = query_info
    def __str__(self):
        return "Datbase Query Failed: " + self.query_info

class NotEnoughRessources(Exception):
    def __init__(self, town_name):
        self.town_name = town_name
        self.purpose = "unknown"
    def __str__(self):
        return "Not Enough ressources in " + self.town_name + " for " + self.purpose

class BuildingAlreadyExists(Exception):
    def __init__(self, building_name):
        self.building_name = building_name
    def __str__(self):
        return "This building already exists: " + self.building_name

if __name__ == "__main__":
    e = UserDoesNotExist("hans")
    print e.message