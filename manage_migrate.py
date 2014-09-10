#!/usr/bin/env python
# -*- encoding:utf-8 -*-
# manage_migrate.py

import os

from flask.ext.script import Manager
from flask.ext.migrate import MigrateCommand

from webapp import app, db

# configuration file
if os.path.isfile('./DEV'): 
	app.config.from_object('config.DebugConfiguration')
else:
	app.config.from_object('config.BaseConfiguration')

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
	manager.run()
