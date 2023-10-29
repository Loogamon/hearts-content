from flask_app import app
from flask_app.controllers import pages
from flask_app.controllers import actions

if __name__=="__main__":
	app.run(debug=True)