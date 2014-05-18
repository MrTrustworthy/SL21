__author__ = 'MrTrustworthy'


from ProjectSL import app, app_config, game
import logging




if __name__ == "__main__":
    #logging.basicConfig(filename="sl21.log", level=logging.DEBUG, format="%(asctime)s | %(levelname)s: %(message)s")
    game.start()
    app.run(debug=True)