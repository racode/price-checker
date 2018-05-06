from src.app import app
__author__ = "esobolie"

app.run(debug=app.config["DEBUG"], port=4990)

