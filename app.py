from flask import Flask
from flask_restful import Api
from config_loader import Config
from routes.events.resources import EventsResource


app = Flask(__name__)
api = Api(app)
app_config = Config()


api.add_resource(EventsResource, "/api/events")


if __name__ == "__main__":
    app.run(debug=app_config.test_flag, port=app_config.backend_port)
