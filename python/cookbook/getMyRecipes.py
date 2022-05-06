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


def getMyRecipes():
    recsDB = list(mongo.db.recipes.find())
    user = mongo.db.users.find_one({"_id": ObjectId("624715013b6773d36014fcbc")})
    
    # Get my recipes
    userMyRecsIds = []
    userMyRecsNames = []
    userMyRecsImages = []

    for rec in recsDB:
        if str(rec["user"]) == "624715013b6773d36014fcbc":
            userMyRec_id = rec["_id"]
            userMyRec_name = rec["name"]
            userMyRec_image = rec["image"]

            userMyRecsIds.append(userMyRec_id)
            userMyRecsNames.append(userMyRec_name)
            userMyRecsImages.append(userMyRec_image)

    userMyRecs = zip(userMyRecsIds,
                      userMyRecsNames,
                      userMyRecsImages)

    return userMyRecs