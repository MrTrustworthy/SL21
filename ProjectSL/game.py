__author__ = 'MrTrustworthy'
import town as town_module
import time
import thread
from app_config import GAME_TURN_INTERVAL
import threading

# EXPERIMENTAL DECORATOR
def synchronized(func):
    func.__lock__ = threading.Lock()

    def synced_func(*args, **kws):
        with func.__lock__:
            return func(*args, **kws)

    return synced_func



#
# MODULE START
#
town_list = None

def start():
    global town_list
    town_list = town_module.load_towns()

    def time_passing():
        #global town_list
        while True:
            time.sleep(GAME_TURN_INTERVAL)
            process_command("", "process_tick")
            process_command("", "reload")
            print "Time has passed"
    thread.start_new_thread(time_passing, ())


def pause():
    pass
def stop():
    pass



#
# MAIN INTERFACE
#
@synchronized
def process_command(user_name, command, params=None):
    global town_list

    if command == "process_tick":
        for t in town_list:
            t.process_tick()
        return

    elif command == "reload":
        town_module.save_towns(town_list)
        town_list = town_module.load_towns()
        return

    try:
        for t in town_list:
            if t.owner == user_name:

                if command == "show_town":
                    return t
                elif command == "upgrade_building":
                    t.upgrade_building(params)
                elif command == "get_aviable_buildings":
                    return t.get_constructable_buildings()
                elif command == "construct_new_building":
                    t.construct_building(params)
                return

    except Exception, e:
        raise e



if __name__ == "__main__":
    start()
    print process_command("ad","show_town")


