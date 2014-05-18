__author__ = 'MrTrustworthy'

from flask import request, render_template, redirect, url_for, flash, session
from functools import wraps
from ProjectSL import app
import db_handler
import app_config
import game
import town_db_handler
from error_handling import *
#
# FILTERS
#
def login_required(something):
    @wraps(something)
    def wrap(*args, **kwargs):
        if "user_name" in session:
            return something(*args, **kwargs)
        else:
            flash(u'Sie sind nicht eingeloggt!')
            return redirect(url_for("login_page"))
    return wrap


#
# GAME VIEWS
#
@app.route("/game", methods=["GET", "POST"])
@login_required
def game_page():

    if request.method == "GET":
        town = game.process_command(session["user_name"], "show_town")
        return render_template("town.html",
                                town = town)

    elif request.method == "POST":
        if request.form["requested_action"] == "upgrade_building":
            try:
                game.process_command(session["user_name"], "upgrade_building", request.form["building_name"])
            except (Exception), e:
                flash(str(e))
        return redirect(url_for("game_page"))



@app.route("/build", methods=["GET", "POST"])
@login_required
def game_build_page():
    if request.method == "GET":
        town = game.process_command(session["user_name"], "show_town")
        building_list = game.process_command(session["user_name"], "get_aviable_buildings")
        return render_template("construct_building.html",
                               town=town,
                               building_list=building_list)

    elif request.method == "POST":
        if request.form["requested_action"] == "construct_new_building":
            try:
                game.process_command(session["user_name"], "construct_new_building", request.form["building_name"])
            except (Exception), e:
                flash(str(e))
            return redirect(url_for("game_page"))

#
# MAIN VIEWS
#

@app.route("/", methods=["GET", "POST"])
@login_required
def main_page():
    return redirect(url_for("chat_page"))

@app.route("/chat", methods=["GET", "POST"])
@login_required
def chat_page():
    if request.method == "GET":
        if session["user_name"] == app_config.ADMIN_NAME:
            is_admin = True
        else:
            is_admin = False

        chat_log = db_handler.get_chatlogs()
        return render_template("chat.html",
                               chatlog = chat_log,
                               is_admin = is_admin)

    elif request.method == "POST":
        name = session["user_name"]
        content = request.form["content"]
        db_handler.add_chatlog(name, content)
        return redirect(url_for("chat_page"))

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile_page():
    if request.method == "GET":

        user_list = db_handler.all_users()
        town_list = town_db_handler.get_towns()
        return render_template("profiles.html",
                               user_list = user_list,
                               town_list = town_list)




#
# ADMIN RELEVANT VIEWS
#

@app.route("/chat/deletepost", methods=["GET"])
@login_required
def delete_post():
    #print "wanting to delete post id:" + request.args.get("post_id")
    db_handler.delete_chatlog(request.args.get("post_id"))
    return redirect(url_for("chat_page"))


#
# GENERAL ACCOUNT MANAGEMENT VIEWS
#

@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "GET":
        return render_template("login.html")


    elif request.method == "POST":
        try:
            db_handler.confirm_user_login(request.form["name"], request.form["password"])
        except (UserDoesNotExist, WrongPassword), e:
            flash(e)
            return render_template("login.html")
        else:
            session["user_name"] = request.form["name"]
            flash("You've been logged in")
            return redirect(url_for("chat_page"))


@app.route("/logout", methods=["GET", "POST"])
def logout():
    if "user_name" in session:
        session.pop("user_name", None)
    return redirect(url_for("login_page"))

@app.route("/register", methods=["GET", "POST"])
def register_page():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        db_handler.add_user(request.form["user_name"], request.form["password"])
        town_db_handler.add_town(request.form["town_name"], request.form["user_name"])
        game.process_command("", "reload")
        return render_template("login.html")