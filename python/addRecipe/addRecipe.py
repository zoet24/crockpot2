import os
from flask import (
    Flask, flash, render_template, redirect,
    request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


def addRecipePost():
    # Format recipe url
    recUrl = request.form.get("name").lower().replace(' ', '-')

    # Format recipe ingredient names
    recDB_ingNames = []
    recDB_ingUrls = ""
    recIngIds = request.form.getlist("ingredientName")
    recIngIds.pop(0)
    for recIngId in recIngIds:
        recDB_ingName = ObjectId(recIngId)
        recDB_ingNames.append(recDB_ingName)
        recDB_ingUrls += (mongo.db.ingredients.find_one({ "_id": ObjectId(recIngId) })['url'])
        recDB_ingUrls += " "

    # Format recipe ingredient quantities to get quantities for 1 portion
    recServes = request.form.get("serves")
    recDB_ingNums = request.form.getlist("ingredientNum")
    recDB_ingNums.pop(0)
    recDB_ingNumsOne = []
    for recDB_ingNum in recDB_ingNums:
        recDB_ingNumOne = float(recDB_ingNum)/float(recServes)
        if recDB_ingNumOne.is_integer():
            recDB_ingNumOne = int(recDB_ingNumOne)
        recDB_ingNumsOne.append(recDB_ingNumOne)

    # Format recipe ingredient names
    recDB_recCats = []
    recDB_recCatsUrls = ""
    recCatIds = request.form.getlist("recipeCategories")
    recCatIds.pop(0)

    for recCatId in recCatIds:
        recDB_recCat = ObjectId(recCatId)
        recDB_recCats.append(recDB_recCat)
        recDB_recCatsUrls += mongo.db.recipeCategories.find_one({ "_id": ObjectId(recCatId) })['url']
        recDB_recCatsUrls += " "

    # Remove hidden add/remove value from form entries
    recDB_ingUnits = request.form.getlist("ingredientUnit")
    recDB_ingUnits.pop(0)

    recDB_instructions = request.form.getlist("instructions")
    recDB_instructions.pop(0)

    recDB_notes = request.form.getlist("notes")
    recDB_notes.pop(0)

    user = mongo.db.users.find_one({"username": session["user"]})

    # Define new recipe for Mongo db
    recDB = {
        "name": request.form.get("name").title(),
        "url": recUrl,
        "time": request.form.get("time"),
        "image": request.form.get("image"),
        "ingredientName": recDB_ingNames,
        "ingredientNum": recDB_ingNumsOne,
        "ingredientUnit": recDB_ingUnits,
        "instructions": recDB_instructions,
        "notes": recDB_notes,
        "recipeCategories": recDB_recCats,
        "user": ObjectId(user["_id"]),
        "ingredientTags": recDB_ingUrls,
        "categoryTags": recDB_recCatsUrls,
    }

    mongo.db.recipes.insert_one(recDB)
    flash(recDB["name"] + " has been added to your recipes.", 'success')