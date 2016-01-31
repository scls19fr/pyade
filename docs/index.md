[![Latest Version](https://img.shields.io/pypi/v/pyade.svg)](https://pypi.python.org/pypi/pyade/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/pyade.svg)](https://pypi.python.org/pypi/pyade/)
[![Wheel format](https://img.shields.io/pypi/wheel/pyade.svg)](https://pypi.python.org/pypi/pyade/)
[![License](https://img.shields.io/pypi/l/pyade.svg)](https://pypi.python.org/pypi/pyade/)
[![Development Status](https://img.shields.io/pypi/status/pyade.svg)](https://pypi.python.org/pypi/pyade/)
[![Downloads monthly](https://img.shields.io/pypi/dm/pyade.svg)](https://pypi.python.org/pypi/pyade/)
[![Requirements Status](https://requires.io/github/scls19fr/pyade/requirements.svg?branch=master)](https://requires.io/github/scls19fr/pyade/requirements/?branch=master)
[![Documentation Status](https://readthedocs.org/projects/pyade/badge/?version=latest)](http://pyade.readthedocs.org/en/latest/)
[![Sourcegraph](https://sourcegraph.com/api/repos/github.com/scls19fr/pyade/.badges/status.png)](https://sourcegraph.com/github.com/scls19fr/pyade)
[![Code Health](https://landscape.io/github/scls19fr/pyade/master/landscape.svg?style=flat)](https://landscape.io/github/scls19fr/pyade/master)
[![Build Status](https://travis-ci.org/scls19fr/pyade.svg)](https://travis-ci.org/scls19fr/pyade)

# pyade

A minimal Python class to use ADE Web API for ADE Planning from [Adesoft](http://www.adesoft.com/).

This is an unofficial development. I am in no way related to this company. Use it at your own risk.

WORK IN PROGRESS

## Dependencies

 * `click` Command Line Interface Creation Kit http://click.pocoo.org/ 
 * `requests` Requests: HTTP for Humans http://www.python-requests.org/
 * `pytz` World Timezone Definitions for Python http://pytz.sourceforge.net/

## Install

```bash
$ pip install pyade
```

## Usage

### Command Line Interface script

You might first define 3 environment variables.

```bash
export ADE_WEB_API_URL="https://server/jsp/webapi"
export ADE_WEB_API_LOGIN="user_login"
export ADE_WEB_API_PASSWORD="user_password" 
```

Than you can run sample using:

```bash
$ python sample/main.py
```

You can also pass url, login, password as optional parameters of command line interface using:

```bash
$ python sample/main.py --url https://server/jsp/webapi --user user_login --password user_password
```

### Interactive usage

Run IPython using:

```bash
$ ipython
```

You can use interactively this class

```python
In [1]: from pyade import ADEWebAPI, Config
```

Import logging module and set level to `logging.DEBUG`

```python
In [2]: import logging
In [3]: logging.basicConfig(level=logging.DEBUG)
```

Get a config (etiher from environment variables)

```python
In [4]: config = Config.create()
```

or passing parameter to `Config.create` method

```python
In [4]: config = Config.create(url='server', login='user_login', password='user_password')
```

You can safely display config in a console, your password will not appear.

```python
In [5]: config
Out[5]:
<Config {'url': 'https://server/jsp/webapi', 'login': 'user_login', 'password': '*********'}>
```

But you can access to any key like a dict. For example:

```python
In [6]: config['url']
Out[6]: 'https://server/jsp/webapi'
```

So caution, your password is not in a safe place, as it's in memory.

Config can be unpacked using `**` operator and use as parameter for `ADEWebAPI` constructor.

```python
In [7]: myade = ADEWebAPI(**config)
```

You can display methods of ADEWebAPI using "." and tab key

```python
In [8]: myade.
myade.connect                 myade.getActivities           myade.getProjects             myade.opt_params
myade.create_list_of_objects  myade.getCaracteristics       myade.getResources            myade.password
myade.disconnect              myade.getCosts                myade.hide_dict_values        myade.sessionId
myade.exception_factory       myade.getDate                 myade.logger                  myade.setProject
myade.factory                 myade.getEvents               myade.login                   myade.url
```

Method signature, docstring, ... can be printed using "?"

```python
In [8]: ?myade.connect
Signature: myade.connect()
Docstring: Connect to server
File:      ~/pyade/pyade/__init__.py
Type:      instancemethod
```

Let's connect to server (using url, login and password saved in `myade` instance of `ADEWebAPI`)

```python
In [9]: myade.connect()
DEBUG:ADEWebAPI:send {'function': 'connect', 'login': 'user_login', 'password': '*********', 'sessionId': '14cef8679e2'}
INFO:requests.packages.urllib3.connectionpool:Starting new HTTPS connection (1): server
DEBUG:requests.packages.urllib3.connectionpool:"GET /jsp/webapi?function=connect&login=user_login&password=user_password&sessionId=14cef8679e2 HTTP/1.1" 200 None
DEBUG:ADEWebAPI:<Response [200]>
DEBUG:ADEWebAPI:<?xml version="1.0" encoding="UTF-8"?>
<session id="14cef878c17"/>

Out[9]: True
```

A list of dict describing projects can be returned using: 

```python
In [10]: myade.getProjects()
DEBUG:ADEWebAPI:send {'function': 'getProjects', 'sessionId': '14cef8679e2'}
INFO:requests.packages.urllib3.connectionpool:Starting new HTTPS connection (1): server
DEBUG:requests.packages.urllib3.connectionpool:"GET /jsp/webapi?function=getProjects&sessionId=14cef8679e2 HTTP/1.1" 200 None
DEBUG:ADEWebAPI:<Response [200]>
DEBUG:ADEWebAPI:<?xml version="1.0" encoding="UTF-8"?>
<projects>
    <project id="6"/>
    <project id="5"/>
</projects>

Out[10]: [{'id': '6'}, {'id': '5'}]
```

You can also use optional parameters such as `detail` to get more details about each project.

```python
In [11]: myade.getProjects(detail=4)
DEBUG:ADEWebAPI:send {'function': 'getProjects', 'sessionId': '14cef8679e2', 'detail': 4}
INFO:requests.packages.urllib3.connectionpool:Starting new HTTPS connection (1): server
DEBUG:requests.packages.urllib3.connectionpool:"GET /jsp/webapi?function=getProjects&sessionId=14cef8679e2&detail=4 HTTP/1.1" 200 None
DEBUG:ADEWebAPI:<Response [200]>
DEBUG:ADEWebAPI:<?xml version="1.0" encoding="UTF-8"?>
<projects>
    <project id="6" name="2015-2016" uid="1428406688761" version="600" loaded="true"/>
    <project id="5" name="2014-2015" uid="1364884711514" version="520" loaded="true"/>
</projects>

Out[11]:
[{'id': '6',
  'loaded': 'true',
  'name': '2015-2016',
  'uid': '1428406688761',
  'version': '600'},
  {'id': '5',
  'loaded': 'true',
  'name': '2014-2015',
  'uid': '1364884711514',
  'version': '520'}]
```

You can set `myade` instance of class `ADEWebAPI` in order methods output list of objects instead of list of dictionaries

```python
In [12]: myade.create_list_of_objects(True)

In [13]: myade.getProjects()
DEBUG:ADEWebAPI:send {'function': 'getProjects', 'sessionId': '14cef8679e2'}
INFO:requests.packages.urllib3.connectionpool:Starting new HTTPS connection (1): server
DEBUG:requests.packages.urllib3.connectionpool:"GET /jsp/webapi?function=getProjects&sessionId=14cef8679e2 HTTP/1.1" 200 None
DEBUG:ADEWebAPI:<Response [200]>
DEBUG:ADEWebAPI:<?xml version="1.0" encoding="UTF-8"?>
<projects>
    <project id="6"/>
    <project id="5"/>
</projects>

Out[13]:
[Project({'id': '6'}),
 Project({'id': '5'})]
```

You need to set current project. You probably won't be able to call most of methods without this.

```python
In [14]: myade.setProject(5)
Out[14]: True
```

...

Don't forget to disconnect from server before quitting.

```python
In [15]: myade.disconnect()
DEBUG:ADEWebAPI:send {'function': 'disconnect', 'sessionId': '14cef8679e2'}
INFO:requests.packages.urllib3.connectionpool:Starting new HTTPS connection (1): server
DEBUG:requests.packages.urllib3.connectionpool:"GET /jsp/webapi?function=disconnect&sessionId=14cef8679e2 HTTP/1.1" 200 None
DEBUG:ADEWebAPI:<Response [200]>
DEBUG:ADEWebAPI:<?xml version="1.0" encoding="UTF-8"?>
<disconnected sessionId="14cef8679e2"/>

Out[15]: True
```

## Development

```bash
$ git clone https://github.com/scls19fr/pyade.git
```
