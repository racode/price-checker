from flask import Blueprint
__author__ = "esobolie"

item_blueprint = Blueprint("items", __name__)

@item_blueprint.route("/item/<string:name>")
def item_page():
    pass

# @item_blueprint.route("/load")
# def load_item():
#     """
#     Load an item's data using the store and return JSON representation of it
#     :return:
#     """
#     pass
