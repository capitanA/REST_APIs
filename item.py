import sqlite3
from flask_jwt import jwt_required
from flask_restful import reqparse, Resource
from flask import jsonify


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price",
                        type=float,
                        required=True,
                        help="This field cannot be left blank!")

    # parser.add_argument("name",
    #                     type=str,
    #                     required=True,
    #                     help="This field cannot be left blank!")

    @jwt_required()
    def get(self, name):

        item = self.find_by_name(name)
        if item:
            return item
        return {"message": "there is no such a item."}

    def find_by_name(self, name):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = connection.execute(query, (name,))
        row = result.fetchone()
        if row:
            return {"item": {"name": row[0], "price": row[1]}}

    def insert_itemn(self, item):

        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "INSERT INTO items VALUES (?,?)"
        cursor.execute(query, (item["name"], item["price"]))
        connection.commit()
        connection.close()

    def update(self, item):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "UPDATE items SET price=? WHERE name=? "
        cursor.execute(query, (item["price"], item["name"]))
        connection.commit()
        connection.close()

    @jwt_required
    def post(self, name):
        if self.find_by_name(name):
            return {"message": f" An item with name, {name} is already exist in database"}, 400
        data_request = Item.parser.parse_args()
        item = {"name": name, "price": data_request["price"]}
        self.insert_itemn(item)

        return {"message": "your item added"}

    @jwt_required()
    def put(self, name):
        data_request = Item.parser.parse_args()
        item = self.find_by_name(name)
        updated_item = {"name": name, "price": data_request["price"]}
        if not item:
            try:
                self.insert_itemn(updated_item)
            except:
                return {"message": "An error has been occurred inserting the item"}
        else:
            try:
                self.update(updated_item)
            except:
                return {"message": "An error has been occurred updating the item!"}
        return updated_item

    @jwt_required()
    def delete(self, name):
        data_request = Item.parser.parse_args()
        item = self.find_by_name(name)
        if item:
            connection = sqlite3.connect("data.db")
            cursor = connection.cursor()
            query = "DELETE FROM items WHERE name=?"
            cursor.execute(query, (name,))
            connection.commit()
            connection.close()
            return {"message": "your item was deleted"}
        return {"message": "there is no such a item."}


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "SELECT * FROM items"
        results = cursor.execute(query)
        connection.commit()
        items = []
        for row in results:
            items.append({"name": row[0], "price": row[1]})

        connection.close()
        return {"items": items}
