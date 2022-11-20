from flask import Flask, request
from flask_restx import Resource, Api


app = Flask(__name__)
api = Api(app)

makes = {}

@api.route('/<string:make_id>')

class MakeSimple(Resource):
    def get(self, make_id):
            return {make_id: makes[make_id]}

    def put(self, make_id):
        makes[make_id] = request.form["data"]
        return {make_id: makes[make_id]}
      
