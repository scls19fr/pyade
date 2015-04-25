#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
An interactive session to run with IPython
copy this code
and paste it in IPython using %paste
"""

import datetime
from pyade import ADEWebAPI, Config
import logging
logging.basicConfig(level=logging.DEBUG)
config = Config.create()
myade = ADEWebAPI(**config)
myade.connect()
myade.setProject(5)
myade.first_date()
myade.week_id(datetime.date.today()) # returns current week_id

# -----

myade.disconnect()