#!/usr/bin/python
# -*- coding: utf8 -*-

"""
    ADE Web API Exceptions

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

from xml.etree import ElementTree as ET

class ExceptionFactory(object):
    def create_from_xml(self, xml_element):
        msg = xml_element.attrib['trace']
        return(Exception(msg))

    def raise_from_xml(self, xml_element):
        exc = self.create_from_xml(xml_element)
        raise(exc)
