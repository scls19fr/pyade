#!/usr/bin/python
# -*- coding: utf8 -*-

"""
    ADE Web API

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

import logging
import traceback

import requests
from xml.etree import ElementTree as ET
import time

from exception import ExceptionFactory

def hide_string(s, char_replace='*'):
    return(char_replace*len(s))

class BaseObject(object):
    """Base object class which can be easily initialize using
    keyword parameters
    Attributes can be access like a dict obj['myattribute']"""
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            self.__dict__[key] = value

    def __getitem__(self, key):
        return(self.__dict__[key])

    def __repr__(self):
        return("%s(%s)" % (self.__class__.__name__, repr(self.__dict__)))

class Project(BaseObject):
    pass

class Resource(BaseObject):
    """Base object for resource (Trainee, Room, Instructor...)"""
    pass

class Trainee(Resource):
    pass

class Room(Resource):
    pass

class Instructor(Resource):
    pass

class Activity(BaseObject):
    pass

class Event(BaseObject):
    pass

class Cost(BaseObject):
    pass

class Caracteristic(BaseObject):
    pass

class Date(BaseObject):
    pass

class ObjectFactory(object):
    def create_object(self, typ, **kwargs):
        resource_objects = {
            'resource': Resource,
            'trainee': Trainee,
            'room': Room,
            'instructor': Instructor,
            'project': Project,
            'activity': Activity,
            'event': Event,
            'cost': Cost,
            'caracteristic': Caracteristic,
            'date': Date,
        }
        return(resource_objects[typ](**kwargs))

class ADEWebAPI():
    def __init__(self, url, login, password):
        self.url = url
        self.login = login
        self.password = password
        
        self.sessionId = None
        
        self.logger = logging.getLogger('ADEWebAPI')

        self.factory = ObjectFactory()
        self.exception_factory = ExceptionFactory()

        self.opt_params = {
            'connect': set([]),
            'disconnect': set([]),
            'setProject': set([]),
            'getProjects': set(['detail', 'id']),
            'getResources': set(['tree', 'folders', 'leaves', 'id', 'name', 'category', \
                'type', 'email', 'url', 'size', 'quantity', 'code', 'address1', \
                'address2', 'zipCode', 'state', 'city', 'country', 'telephone', \
                'fax', 'timezone', 'jobCategory', 'manager', 'codeX', 'codeY', \
                'codeZ', 'info', 'detail']),
            'getActivities': set(['tree', 'id', 'name', 'resources', 'type', 'url', \
                'capacity', 'duration', 'repetition', 'code', 'timezone', 'codeX', \
                'codeY', 'codeZ', 'maxSeats', 'seatseLeft', 'info']),
            'getEvents': set(['eventId', 'activities', 'name', 'resources', \
                'weeks', 'days', 'date', 'detail']),
            'getCosts': set(['id', 'name']),
            'getCaracteristics': set(['id', 'name']),
            'getDate': set([])
        }

        self.create_list_of_objects(False)
    
    def create_list_of_objects(self, flag):
        if flag:
            self._create_list_of = self._create_list_of_objects
        else:
            self._create_list_of = self._create_list_of_dicts

    def hide_dict_values(self, d, hidden_keys=['password']):
        """Returns a dictionnary with some hidden values (such as password)
        when a dict is given"""
        d_hidden = d.copy()
        for key in hidden_keys:
            if key in d_hidden.keys():
                d_hidden[key] = hide_string(d_hidden[key])
        return(d_hidden)

    def _send_request(self, func, **params):
        """Send a request"""
        params['function'] = func

        if 'sessionId' not in params.keys():
            if self.sessionId is not None:
                params['sessionId'] = self.sessionId
        
        self.logger.debug("send %s" % self.hide_dict_values(params))
        response = requests.get(self.url, params=params)
        self.logger.debug(response)
        self.logger.debug(response.text)
        element = ET.fromstring(response.text)

        if element.tag=='error':
            self.exception_factory.raise_from_xml(element)

        return(element)
        
    def connect(self):
        """Connect to server"""
        function = 'connect'
        element = self._send_request(function, login=self.login, password=self.password)
        returned_sessionId = element.attrib["id"]
        self.sessionId = returned_sessionId
        return(returned_sessionId is not None)

    def disconnect(self):
        """Disconnect from server"""
        function = 'disconnect'
        element = self._send_request(function)
        returned_sessionId = element.attrib["sessionId"]
        return(returned_sessionId == self.sessionId)

    def _test_opt_params(self, given_params, function):
        """Test if kwargs parameters are in allowed optional parameters
        of a given method"""
        opt_params = self.opt_params[function]
        given_params = set(given_params.keys())
        msg = "One (or many) parameters of '%s' call are not allowed. %s is not in %s" \
            % ('getResources', given_params-opt_params, opt_params)
        assert given_params <= opt_params, msg

    def _create_list_of_dicts(self, category, lst):
        """Returns a list of dict (attributes of XML element)"""
        return(map(lambda elt: elt.attrib, lst))

    def _create_list_of_objects(self, category, lst):
        """Returns a list of object using factory"""
        return(map(lambda elt: self.factory.create_object(category, **elt.attrib), lst))

    #def getProjects(self, detail=None, id=None):
    def getProjects(self, **kwargs):
        """Returns (list of) projects"""
        function = 'getProjects'
        #element = self._send_request(function, detail=detail, id=id)
        element = self._send_request(function, **kwargs)
        lst_projects = element.findall('project')
        lst_projects = self._create_list_of('project', lst_projects)
        return(lst_projects)
                
    def setProject(self, projectId):
        """Set current project"""
        function = 'setProject'
        element = self._send_request(function, projectId=projectId)
        returned_projectId = element.attrib["projectId"]        
        returned_sessionId = element.attrib["sessionId"] 
        return(returned_sessionId == self.sessionId \
            and returned_projectId==str(projectId))

    def getResources(self, **kwargs):
        function = 'getResources'
        self._test_opt_params(kwargs, function)
        element = self._send_request(function, **kwargs)
        if 'category' in kwargs.keys():
            category = kwargs['category']
        else:
            category = 'resource'
        lst_resources = element.findall(category)
        lst_resources = self._create_list_of(category, lst_resources)
        return(lst_resources)

    def getActivities(self, **kwargs):
        function = 'getActivities'
        self._test_opt_params(kwargs, function)
        typ = 'activity'
        element = self._send_request(function, **kwargs)
        lst_activities = element.findall(typ)
        lst_activities = self._create_list_of(typ, lst_activities)
        return(lst_activities)
        
    def getEvents(self, **kwargs):
        function = 'getEvents'
        self._test_opt_params(kwargs, function)
        typ = 'event'
        element = self._send_request(function, **kwargs)
        lst_events = element.findall(typ)
        lst_events = self._create_list_of(typ, lst_events)
        return(lst_events)
        
    def getCosts(self, **kwargs):
        function = 'getCosts'
        self._test_opt_params(kwargs, function)
        element = self._send_request(function, **kwargs)
        typ = 'cost'
        lst = element.findall(typ)
        lst = self._create_list_of(typ, lst)
        return(lst)

    def getCaracteristics(self, **kwargs):
        function = 'getCaracteristics'
        self._test_opt_params(kwargs, function)
        element = self._send_request(function, **kwargs)
        typ = 'caracteristic'
        lst = element.findall(typ)
        lst = self._create_list_of(typ, lst)
        return(lst)
        
    def getDate(self, week, day, slot):
        function = 'getDate'
        #self._test_opt_params(kwargs, function) # no keyword arguments (kwargs)
        element = self._send_request(function, week=week, day=day, slot=slot)
        date = Date(**element.attrib)
        return(date)
