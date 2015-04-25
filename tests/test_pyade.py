#!/usr/bin/python
# -*- coding: utf8 -*-

"""
    ADE Web API unit tests

    Copyright (C) 2011-2015 "Sébastien Celles" <s.celles@gmail.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>
"""

from pyade import ADEWebAPI, Config

def test_pyade():
    
    config = Config.create()
    myade = ADEWebAPI(**config)
    #myade.create_list_of_objects(True) # True: create_list_of_objects False: create_list_of_dicts
    connected = myade.connect()
    
    projects = myade.getProjects(detail=4)
    assert len(list(projects))>=1
    # list is necessary with Python 3
    # because without it, it raises TypeError: object of type 'map' has no len()

    project_set = myade.setProject(5) # 2014-2015=>5
    assert project_set

    disconnected = myade.disconnect()
    assert disconnected
