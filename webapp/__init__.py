import os
from flask import Flask, request, render_template, send_from_directory
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, current_user
from flask.ext.actions import Manager
from flask.ext.bcrypt import Bcrypt

# app setup
app = Flask(__name__) # main app object

# configuration file
if os.path.isfile('./DEV'): 
	app.config.from_object('config.DebugConfiguration')
else:
	app.config.from_object('config.BaseConfiguration')

login_manager = LoginManager(app) # login manager
manager = Manager(app) # shell actions manager
db = SQLAlchemy(app) # database connection
bcrypt = Bcrypt(app) # hashing function

# users module blueprint
from webapp.users.views import mod as usersModule
app.register_blueprint(usersModule)

# configure module blueprint
from webapp.configure.views import mod as configureModule
app.register_blueprint(configureModule)

# api module blueprint
from webapp.api.views import mod as APIModule
app.register_blueprint(APIModule)

#add our view as the login view
login_manager.login_view = "users.login"

#----------------------------------------
# controllers
#----------------------------------------

@app.route('/favicon.ico')
def favicon():
	return send_from_directory(os.path.join(app.root_path, 'static'), 'img/favicon.ico')


@app.route("/", methods=['GET', 'POST'])
def index():
	return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404


@app.errorhandler(400)
def key_error(e):
	app.logger.warning('Invalid request resulted in KeyError', exc_info=e)
	return render_template('400.html'), 400


@app.errorhandler(500)
def internal_server_error(e):
	app.logger.warning('An unhandled exception is being displayed to the end user', exc_info=e)
	return render_template('generic.html'), 500


@app.errorhandler(Exception)
def unhandled_exception(e):
	app.logger.error('An unhandled exception is being displayed to the end user', exc_info=e)
	return render_template('generic.html'), 500


@app.before_request
def log_entry():
	app.logger.debug("Handling request")


@app.teardown_request
def log_exit(exc):
	app.logger.debug("Finished handling request", exc_info=exc)


#----------------------------------------
# logging
#----------------------------------------

import logging

class ContextualFilter(logging.Filter):
	def filter(self, log_record):
		log_record.url = request.path
		log_record.method = request.method
		log_record.ip = request.environ.get("REMOTE_ADDR")
		log_record.user_id = -1 if current_user.is_anonymous() else current_user.get_id()

		return True

context_provider = ContextualFilter()
app.logger.addFilter(context_provider)
del app.logger.handlers[:]

handler = logging.StreamHandler()

log_format = "%(asctime)s %(levelname)s\t%(user_id)s\t%(ip)s\t%(method)s\t%(url)s\t%(message)s"
formatter = logging.Formatter(log_format)
handler.setFormatter(formatter)

app.logger.addHandler(handler)

from logging import ERROR
from logging.handlers import TimedRotatingFileHandler

# Only set up a file handler if we know where to put the logs
if app.config.get("ERROR_LOG_PATH"):

	# Create one file for each day. Delete logs over 7 days old.
	file_handler = TimedRotatingFileHandler(app.config["ERROR_LOG_PATH"], when="D", backupCount=7)

	# Use a multi-line format for this logger, for easier scanning
	file_formatter = logging.Formatter('''
	Time: %(asctime)s
	Level: %(levelname)s
	Method: %(method)s
	Path: %(url)s
	IP: %(ip)s
	User ID: %(user_id)s

	Message: %(message)s

	---------------------''')

	# Filter out all log messages that are lower than Error.
	file_handler.setLevel(ERROR)

	file_handler.addFormatter(file_formatter)
	app.logger.addHandler(file_handler)