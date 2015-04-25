# pyade

A minimal Python class to use ADE Web API for ADE Planning from [Adesoft](http://www.adesoft.com/).

This is an unofficial development. I am in no way related to this company. Use it at your own risk.

WORK IN PROGRESS

## Usage

You might first define 3 environment variables.

    export ADE_WEB_API_URL="https://server/jsp/webapi"
    export ADE_WEB_API_LOGIN="user_login"
    export ADE_WEB_API_PASSWORD="user_password" 

Than you can run sample using:

    $ python sample/main.py

You can also pass url, login, password as optional parameters for command line interface using:

    $ python sample/main.py --url https://server/jsp/webapi --user user_login --password user_password
